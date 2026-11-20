"""Shared helpers for benchmark scripts: environment capture, timing, result files."""

from __future__ import annotations

import json
import os
import platform
import statistics
import sys
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def environment() -> dict[str, Any]:
    """Everything needed to judge whether two result files are comparable."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
        "cpu_count": os.cpu_count(),
        "gpu": "not used",
    }


def time_it(fn: Callable[[], object], repeats: int) -> dict[str, float]:
    """Run fn `repeats` times (after one untimed warm-up) and report wall-clock seconds."""
    fn()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return {
        "median_s": statistics.median(samples),
        "min_s": min(samples),
        "max_s": max(samples),
        "repeats": float(repeats),
    }


def write_results(name: str, label: str, payload: dict[str, Any]) -> Path:
    """Write a JSON result file. `label` must say whether data is measured or simulated."""
    RESULTS_DIR.mkdir(exist_ok=True)
    document = {
        "benchmark": name,
        "data_kind": label,
        "recorded_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "command": " ".join(sys.argv),
        "environment": environment(),
        **payload,
    }
    path = RESULTS_DIR / f"{name}.json"
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return path
