"""Tests for deterministic runtime checkpoint logging."""
from unittest.mock import patch

from bot.checkpoint import CheckpointConfig, CheckpointLogger
from bot.health import HealthConfig, StuckStateMonitor


class FakeClock:
    """A controllable stand-in for `time.monotonic()`."""

    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


class TestCheckpointTiming:
    """Test the periodic-interval gating in `checkpoint()`."""

    def test_no_checkpoint_before_interval_elapses(self):
        clock = FakeClock()
        with patch("bot.checkpoint.time.monotonic", new=clock):
            logger = CheckpointLogger("test", CheckpointConfig(interval_seconds=60))
            clock.advance(30)
            assert logger.checkpoint() is False

    def test_checkpoint_fires_once_interval_elapses(self):
        clock = FakeClock()
        with patch("bot.checkpoint.time.monotonic", new=clock):
            logger = CheckpointLogger("test", CheckpointConfig(interval_seconds=60))
            clock.advance(61)
            assert logger.checkpoint() is True

    def test_checkpoint_resets_timer_after_firing(self):
        clock = FakeClock()
        with patch("bot.checkpoint.time.monotonic", new=clock):
            logger = CheckpointLogger("test", CheckpointConfig(interval_seconds=60))
            clock.advance(61)
            assert logger.checkpoint() is True
            clock.advance(10)
            assert logger.checkpoint() is False
            clock.advance(51)
            assert logger.checkpoint() is True

    def test_force_bypasses_interval(self):
        clock = FakeClock()
        with patch("bot.checkpoint.time.monotonic", new=clock):
            logger = CheckpointLogger("test", CheckpointConfig(interval_seconds=60))
            assert logger.checkpoint(force=True) is True

    @patch("bot.checkpoint.logging")
    def test_checkpoint_logs_at_info_level(self, mock_logging):
        logger = CheckpointLogger("test")
        logger.checkpoint(force=True)
        assert mock_logging.info.called


class TestCheckpointActionTracking:
    """Test `record_action()` bookkeeping and history capping."""

    def test_record_action_updates_last_action(self):
        logger = CheckpointLogger("test")
        logger.record_action("fish_from_spot")
        snapshot = logger._state_snapshot(monitor=None)
        assert snapshot["last_action"] == "fish_from_spot"
        assert snapshot["seconds_since_last_action"] is not None

    def test_no_action_recorded_yet(self):
        logger = CheckpointLogger("test")
        snapshot = logger._state_snapshot(monitor=None)
        assert snapshot["last_action"] is None
        assert snapshot["seconds_since_last_action"] is None

    def test_action_history_caps_at_configured_size(self):
        logger = CheckpointLogger("test", CheckpointConfig(action_history_size=3))
        for i in range(10):
            logger.record_action(f"action-{i}")
        assert len(logger._action_history) == 3
        recorded = [action for _, action in logger._action_history]
        assert recorded == ["action-7", "action-8", "action-9"]


class TestCheckpointSnapshotWithMonitor:
    """Test that the snapshot pulls in `StuckStateMonitor` counters."""

    def test_snapshot_includes_monitor_state(self):
        config = HealthConfig(stale_frame_limit=5, capture_failure_limit=5, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)
        monitor.record_frame("same")
        monitor.record_frame("same")

        logger = CheckpointLogger("test")
        snapshot = logger._state_snapshot(monitor)

        assert snapshot["stale_frame_count"] == 2
        assert snapshot["capture_failure_count"] == 0
        assert snapshot["recovery_count"] == 0
        assert "idle_seconds" in snapshot

    def test_snapshot_without_monitor_omits_monitor_keys(self):
        logger = CheckpointLogger("test")
        snapshot = logger._state_snapshot(monitor=None)
        assert "stale_frame_count" not in snapshot
        assert "idle_seconds" not in snapshot


class TestCheckpointFailureSummary:
    """Test the failure-time diagnostic dump."""

    @patch("bot.checkpoint.logging")
    def test_summarize_failure_logs_at_error_level(self, mock_logging):
        logger = CheckpointLogger("test")
        logger.record_action("fish_from_spot")
        logger.summarize_failure(ValueError("boom"))
        assert mock_logging.error.called

    @patch("bot.checkpoint.logging")
    def test_summarize_failure_includes_exception_details(self, mock_logging):
        logger = CheckpointLogger("test")
        logger.summarize_failure(RuntimeError("capture device gone"))

        args = mock_logging.error.call_args[0]
        assert "RuntimeError" in args
        assert str(RuntimeError("capture device gone")) in [str(a) for a in args]

    @patch("bot.checkpoint.logging")
    def test_summarize_failure_includes_monitor_state(self, mock_logging):
        monitor = StuckStateMonitor("test")
        monitor.record_capture_failure()
        logger = CheckpointLogger("test")

        logger.summarize_failure(ValueError("boom"), monitor)

        # The formatted snapshot dict (last positional %s arg before recent_actions)
        # should reflect the monitor's capture-failure count.
        args = mock_logging.error.call_args[0]
        snapshot_arg = args[-2]
        assert snapshot_arg["capture_failure_count"] == 1
