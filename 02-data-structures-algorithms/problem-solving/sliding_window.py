"""Worked problem: allow at most N requests per rolling time window.

Decomposition (see README): state -> invariant -> operation -> edge cases -> complexity.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

import time
from collections import deque
from collections.abc import Callable


class SlidingWindowRateLimiter:
    """Sliding-window-log limiter.

    State: a deque of the timestamps of *accepted* requests, oldest first.
    Invariant: after eviction, every stored timestamp is within the last `window` seconds
    and there are never more than `limit` of them. Memory is therefore O(limit).
    """

    def __init__(
        self,
        limit: int,
        window_seconds: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self._limit = limit
        self._window = window_seconds
        self._clock = clock
        self._accepted: deque[float] = deque()

    def _evict(self, now: float) -> None:
        # Each timestamp is appended once and removed once: O(1) amortised per call.
        while self._accepted and self._accepted[0] <= now - self._window:
            self._accepted.popleft()

    def allow(self) -> bool:
        now = self._clock()
        self._evict(now)
        if len(self._accepted) >= self._limit:
            return False  # rejected calls are NOT recorded, so retrying never extends the block
        self._accepted.append(now)
        return True

    @property
    def current_count(self) -> int:
        self._evict(self._clock())
        return len(self._accepted)

    def retry_after(self) -> float:
        """Seconds until a request would be accepted (0.0 if one would be accepted now)."""
        now = self._clock()
        self._evict(now)
        if len(self._accepted) < self._limit:
            return 0.0
        return self._accepted[0] + self._window - now
