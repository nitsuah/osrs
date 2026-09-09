"""Tests for runtime health monitoring and stuck-state recovery."""
from unittest.mock import patch

from bot.health import HealthConfig, StuckStateMonitor


class TestStuckStateMonitorFrames:
    """Test stale-OCR-frame detection."""

    def test_not_stuck_initially(self):
        monitor = StuckStateMonitor("test")
        assert monitor.is_stuck() is False

    def test_repeated_identical_frames_trigger_stuck(self):
        config = HealthConfig(stale_frame_limit=3, capture_failure_limit=100, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)

        for _ in range(2):
            monitor.record_frame("same text")
            assert monitor.is_stuck() is False

        monitor.record_frame("same text")
        assert monitor.is_stuck() is True

    def test_changing_frames_do_not_trigger_stuck(self):
        config = HealthConfig(stale_frame_limit=3, capture_failure_limit=100, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)

        for i in range(10):
            monitor.record_frame(f"frame {i}")
            assert monitor.is_stuck() is False

    def test_empty_frames_do_not_count_as_stale(self):
        config = HealthConfig(stale_frame_limit=2, capture_failure_limit=100, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)

        for _ in range(10):
            monitor.record_frame("")
            assert monitor.is_stuck() is False

    def test_activity_resets_stale_frame_count(self):
        config = HealthConfig(stale_frame_limit=3, capture_failure_limit=100, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)

        monitor.record_frame("same text")
        monitor.record_frame("same text")
        monitor.record_activity()
        monitor.record_frame("same text")
        assert monitor.is_stuck() is False


class TestStuckStateMonitorCaptureFailures:
    """Test consecutive-capture-failure detection."""

    def test_repeated_capture_failures_trigger_stuck(self):
        config = HealthConfig(stale_frame_limit=1000, capture_failure_limit=3, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)

        for _ in range(2):
            monitor.record_capture_failure()
            assert monitor.is_stuck() is False

        monitor.record_capture_failure()
        assert monitor.is_stuck() is True

    def test_successful_frame_resets_capture_failures(self):
        config = HealthConfig(stale_frame_limit=1000, capture_failure_limit=3, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)

        monitor.record_capture_failure()
        monitor.record_capture_failure()
        monitor.record_frame("some text")
        monitor.record_capture_failure()
        assert monitor.is_stuck() is False


class TestStuckStateMonitorIdle:
    """Test idle-time detection."""

    def test_idle_beyond_limit_triggers_stuck(self):
        config = HealthConfig(stale_frame_limit=1000, capture_failure_limit=1000, max_idle_seconds=10)

        with patch("bot.health.time.monotonic", side_effect=[0.0, 20.0]):
            monitor = StuckStateMonitor("test", config)  # consumes t=0.0 as the initial activity time
            assert monitor.is_stuck() is True  # consumes t=20.0 while computing idle_seconds()

    def test_recent_activity_is_not_stuck(self):
        config = HealthConfig(stale_frame_limit=1000, capture_failure_limit=1000, max_idle_seconds=10)
        monitor = StuckStateMonitor("test", config)
        monitor.record_activity()
        assert monitor.is_stuck() is False


class TestStuckStateMonitorRecover:
    """Test deterministic recovery behavior."""

    def test_recover_resets_counters(self):
        config = HealthConfig(stale_frame_limit=1, capture_failure_limit=1, max_idle_seconds=1000)
        monitor = StuckStateMonitor("test", config)

        monitor.record_capture_failure()
        assert monitor.is_stuck() is True

        monitor.recover()

        assert monitor.is_stuck() is False
        assert monitor.recovery_count == 1

    def test_recover_increments_recovery_count(self):
        monitor = StuckStateMonitor("test")
        assert monitor.recovery_count == 0
        monitor.recover()
        monitor.recover()
        assert monitor.recovery_count == 2

    @patch("bot.health.logging")
    def test_recover_logs_a_warning(self, mock_logging):
        monitor = StuckStateMonitor("test")
        monitor.recover()
        assert mock_logging.warning.called
