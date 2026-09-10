"""Deterministic runtime checkpoint logging for long-running loops.

`fishing.Fish()` and `thieving.Theft()` can run unattended for hours. When
something eventually goes wrong -- the bot gets banned, the client crashes,
the loop silently stalls -- the only troubleshooting signal today is
whatever `logging.info`/`logging.warning` calls happened to fire right
before the failure, scattered across an undifferentiated log stream.

`CheckpointLogger` gives each loop a single, cheap call-site (`checkpoint()`)
that periodically emits one structured log line summarizing loop state
(elapsed runtime, last action taken, idle time, and the current
`StuckStateMonitor` counters), plus a small ring buffer of recent actions
that `summarize_failure()` dumps when an unhandled exception ends the loop.
This is pure bookkeeping -- it doesn't change control flow or automation
behavior, so it doesn't require live-game verification to be useful.
"""

import logging
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional, Tuple

from bot.health import StuckStateMonitor


@dataclass
class CheckpointConfig:
    """Tuning knobs for how often/how much `CheckpointLogger` records."""

    interval_seconds: float = 60.0
    """Minimum time between periodic checkpoint log lines."""

    action_history_size: int = 10
    """How many recent actions to retain for the failure summary."""


class CheckpointLogger:
    """Periodic state logging plus a failure-time summary for one loop."""

    def __init__(self, name: str, config: Optional[CheckpointConfig] = None) -> None:
        self.name = name
        self.config = config or CheckpointConfig()
        self._start = time.monotonic()
        self._last_checkpoint = self._start
        self._last_action: Optional[str] = None
        self._last_action_at: Optional[float] = None
        self._action_history: Deque[Tuple[float, str]] = deque(
            maxlen=self.config.action_history_size
        )

    def record_action(self, action: str) -> None:
        """Record that the loop just took `action` (e.g. "fish_from_spot").

        Cheap and side-effect free besides bookkeeping -- callers can call
        this right alongside `StuckStateMonitor.record_activity()`.
        """
        now = time.monotonic()
        self._last_action = action
        self._last_action_at = now
        self._action_history.append((now, action))

    def _state_snapshot(self, monitor: Optional[StuckStateMonitor]) -> dict:
        now = time.monotonic()
        snapshot = {
            "loop": self.name,
            "elapsed_seconds": round(now - self._start, 1),
            "last_action": self._last_action,
            "seconds_since_last_action": (
                round(now - self._last_action_at, 1)
                if self._last_action_at is not None
                else None
            ),
        }
        if monitor is not None:
            snapshot.update(
                {
                    "idle_seconds": round(monitor.idle_seconds(), 1),
                    "stale_frame_count": monitor.stale_frame_count,
                    "capture_failure_count": monitor.capture_failure_count,
                    "recovery_count": monitor.recovery_count,
                }
            )
        return snapshot

    def checkpoint(
        self, monitor: Optional[StuckStateMonitor] = None, force: bool = False
    ) -> bool:
        """Log a periodic checkpoint if `interval_seconds` has elapsed.

        Returns True if a checkpoint was actually logged (useful for tests
        and for callers that want to know without duplicating the timing
        logic). `force=True` bypasses the interval check.
        """
        now = time.monotonic()
        if not force and (now - self._last_checkpoint) < self.config.interval_seconds:
            return False

        self._last_checkpoint = now
        snapshot = self._state_snapshot(monitor)
        logging.info("[%s] checkpoint: %s", self.name, snapshot)
        return True

    def summarize_failure(
        self, exc: BaseException, monitor: Optional[StuckStateMonitor] = None
    ) -> None:
        """Log a diagnostic summary when the loop is about to die.

        Call this from the loop's outermost `except` block, before
        re-raising, so the last-known-good state and recent action history
        survive in the log even though the process is about to exit.
        """
        snapshot = self._state_snapshot(monitor)
        history = [
            (round(t - self._start, 1), action) for t, action in self._action_history
        ]
        logging.error(
            "[%s] loop failed after %.1fs: %s: %s | last_state=%s | recent_actions=%s",
            self.name,
            time.monotonic() - self._start,
            type(exc).__name__,
            exc,
            snapshot,
            history,
        )
