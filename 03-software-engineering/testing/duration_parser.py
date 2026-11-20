"""parse_duration("1h30m") -> 5400.0: a worked test-driven-development example.

The tests in test_duration_parser.py were written in the order described in the README
(red -> green -> refactor); the implementation below is the end state.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

import re

_UNIT_SECONDS = {"h": 3600.0, "m": 60.0, "s": 1.0, "ms": 0.001}
_WHOLE = re.compile(r"(?:\d+(?:ms|h|m|s))+")
_PART = re.compile(r"(\d+)(ms|h|m|s)")  # 'ms' listed first so '5ms' is not read as '5m' + 's'


def parse_duration(text: str) -> float:
    """Convert strings such as '90s', '1h30m' or '250ms' to seconds.

    Rules: one or more <integer><unit> parts; units h, m, s, ms; each unit at most once;
    no whitespace, signs or decimals. Anything else raises ValueError.
    """
    if not isinstance(text, str):
        raise TypeError(f"duration must be a string, got {type(text).__name__}")
    if _WHOLE.fullmatch(text) is None:
        raise ValueError(f"invalid duration: {text!r}")
    parts = _PART.findall(text)
    units = [unit for _, unit in parts]
    if len(units) != len(set(units)):
        raise ValueError(f"duplicate unit in duration: {text!r}")
    return sum(int(number) * _UNIT_SECONDS[unit] for number, unit in parts)
