"""Latency and throughput primitives.

These functions compute statistics from *measurements supplied by the caller*. They never
generate data. Whether a set of numbers came from real hardware or from a simulator is the
responsibility of whoever records them (see benchmarks/methodology.md).

Percentile definition: **nearest-rank** (NIST/Excel-exclusive style "type 1"): the p-th
percentile of n values is the value at rank ceil(p/100 * n) in sorted order. The result is
always an observed value, never an interpolated one, which is the conventional choice for
tail latency (p99 should be a latency that actually happened). Libraries that interpolate
(for example numpy.percentile's default) can report different numbers on small samples.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction


def percentile(values: Sequence[float], p: float) -> float:
    """Nearest-rank percentile, 0 <= p <= 100. Raises ValueError on empty or NaN input."""
    if isinstance(p, bool) or not 0 <= p <= 100:
        raise ValueError(f"p must be between 0 and 100, got {p!r}")
    if not values:
        raise ValueError("cannot compute a percentile of an empty sequence")
    if any(math.isnan(v) for v in values):
        raise ValueError("values must not contain NaN")
    ordered = sorted(values)
    # Exact arithmetic: float 0.07 * 100 == 7.000000000000001, whose ceiling is 8 (wrong).
    # Fraction(str(p)) parses the decimal text exactly, so the ceiling is computed correctly.
    rank = math.ceil(Fraction(str(p)) * len(ordered) / 100)
    return ordered[max(rank, 1) - 1]


@dataclass(frozen=True)
class LatencySummary:
    count: int
    minimum: float
    maximum: float
    mean: float
    p50: float
    p95: float
    p99: float


def summarize(latencies: Sequence[float]) -> LatencySummary:
    if not latencies:
        raise ValueError("cannot summarise an empty sequence")
    if any(v < 0 for v in latencies):
        raise ValueError("latencies must be non-negative")
    return LatencySummary(
        count=len(latencies),
        minimum=min(latencies),
        maximum=max(latencies),
        mean=math.fsum(latencies) / len(latencies),
        p50=percentile(latencies, 50),
        p95=percentile(latencies, 95),
        p99=percentile(latencies, 99),
    )


def throughput(completed: int, duration_seconds: float) -> float:
    """Completed requests (or tokens) per second over a measured wall-clock interval."""
    if completed < 0:
        raise ValueError("completed must be >= 0")
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be > 0")
    return completed / duration_seconds


def time_to_first_token(request_start: float, token_times: Sequence[float]) -> float:
    """Seconds from request start to the first generated token (TTFT)."""
    if not token_times:
        raise ValueError("no tokens were produced")
    if token_times[0] < request_start:
        raise ValueError("first token precedes request start")
    return token_times[0] - request_start


def inter_token_latencies(token_times: Sequence[float]) -> list[float]:
    """Gaps between consecutive tokens (ITL). Empty for fewer than two tokens."""
    gaps = [b - a for a, b in zip(token_times, token_times[1:], strict=False)]
    if any(g < 0 for g in gaps):
        raise ValueError("token timestamps must be non-decreasing")
    return gaps
