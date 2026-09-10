"""Runtime health monitoring and deterministic stuck-state recovery.

Long-running automation loops (`bot.skills.fishing.Fish`,
`bot.skills.thieving.Theft`) can silently stall without raising an
exception: screen capture can fail repeatedly (client minimized, display
locked), OCR can keep returning the same stale chat frame forever, or the
loop can simply go a long time without performing a real action. None of
those conditions crash the process, so without an explicit health check the
bot just spins quietly and does nothing useful.

`StuckStateMonitor` gives callers a single decision point -- `is_stuck()`
-- backed by three independent signals, plus a deterministic `recover()`
action so every loop doesn't need to invent its own recovery/backoff logic.
"""

import logging
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class HealthConfig:
    """Thresholds that decide when a loop is considered stuck."""

    stale_frame_limit: int = 20
    """Consecutive identical (non-empty) OCR chat frames before we call it stale."""

    capture_failure_limit: int = 10
    """Consecutive failed screen captures before we call it stuck."""

    max_idle_seconds: float = 300.0
    """Seconds without a recorded real action before we call it stuck."""


class StuckStateMonitor:
    """Tracks a single loop's health and decides when recovery is needed."""

    def __init__(self, name: str, config: Optional[HealthConfig] = None) -> None:
        self.name = name
        self.config = config or HealthConfig()
        self._last_chat_text: Optional[str] = None
        self._stale_frame_count = 0
        self._capture_failure_count = 0
        self._last_activity = time.monotonic()
        self._recovery_count = 0

    def record_capture_failure(self) -> None:
        """Record a failed `capture_screen()`/OCR call."""
        self._capture_failure_count += 1

    def record_frame(self, chat_text: str) -> None:
        """Record an observed OCR chat frame and update staleness tracking.

        Only non-empty frames count toward staleness; an empty chat region
        is the normal "nothing happening" case and shouldn't trip recovery.
        A frame counts as the first of a possible run of duplicates as soon
        as it's observed (count starts at 1, not 0), matching
        `record_capture_failure`'s plain-increment semantics -- so
        `stale_frame_limit` consecutive identical frames is exactly that many
        `record_frame` calls, not one more.
        """
        self._capture_failure_count = 0
        if not chat_text:
            self._stale_frame_count = 0
        elif chat_text == self._last_chat_text:
            self._stale_frame_count += 1
        else:
            self._stale_frame_count = 1
        self._last_chat_text = chat_text

    def record_activity(self) -> None:
        """Record that the loop performed a real action (click, response, etc.)."""
        self._last_activity = time.monotonic()
        self._stale_frame_count = 0

    def idle_seconds(self) -> float:
        return time.monotonic() - self._last_activity

    def is_stuck(self) -> bool:
        return (
            self._stale_frame_count >= self.config.stale_frame_limit
            or self._capture_failure_count >= self.config.capture_failure_limit
            or self.idle_seconds() >= self.config.max_idle_seconds
        )

    def recover(self) -> None:
        """Perform deterministic recovery: log a checkpoint and reset counters.

        This guarantees the monitor's own state doesn't stay latched in a
        "stuck" condition forever; callers remain free to layer loop-specific
        corrective action (e.g. re-clicking the compass) on top, but even if
        they don't, the monitor will keep evaluating fresh state afterward.
        """
        self._recovery_count += 1
        logging.warning(
            "[%s] Stuck-state recovery #%d triggered "
            "(stale_frames=%d, capture_failures=%d, idle=%.1fs)",
            self.name,
            self._recovery_count,
            self._stale_frame_count,
            self._capture_failure_count,
            self.idle_seconds(),
        )
        self._stale_frame_count = 0
        self._capture_failure_count = 0
        self._last_activity = time.monotonic()

    @property
    def recovery_count(self) -> int:
        return self._recovery_count

    @property
    def stale_frame_count(self) -> int:
        """Consecutive identical (non-empty) OCR chat frames observed so far."""
        return self._stale_frame_count

    @property
    def capture_failure_count(self) -> int:
        """Consecutive failed `capture_screen()`/OCR calls observed so far."""
        return self._capture_failure_count
