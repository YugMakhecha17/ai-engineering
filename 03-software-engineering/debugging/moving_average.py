"""Worked debugging example. See README.md for the full session.

The original (deliberately buggy) version is reproduced in the README. This module holds
the corrected implementation; the regression tests pin the behaviour that the bug broke.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)


def moving_average(values: Sequence[float], window: int) -> list[float]:
    """Mean of every contiguous run of `window` values; len(result) == len(values) - window + 1."""
    if window < 1:
        raise ValueError(f"window must be >= 1, got {window}")
    if window > len(values):
        raise ValueError(f"window ({window}) exceeds number of values ({len(values)})")
    result: list[float] = []
    current = sum(values[:window])
    result.append(current / window)
    for i in range(window, len(values)):
        current += values[i] - values[i - window]  # slide: add the newcomer, drop the leaver
        result.append(current / window)
        logger.debug("i=%d current_sum=%s", i, current)
    return result
