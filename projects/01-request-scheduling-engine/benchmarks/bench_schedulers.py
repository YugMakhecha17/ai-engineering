"""Measure submit-all-then-drain throughput for FifoScheduler and PriorityScheduler.

Run from the repository root:
    python projects/01-request-scheduling-engine/benchmarks/bench_schedulers.py

Data kind: MEASURED wall-clock time on the machine recorded in the output file.
Priorities are drawn from a seeded RNG over 10 levels so runs are repeatable.
"""

from __future__ import annotations

import itertools
import random
import sys
from functools import partial
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "benchmarks"))
sys.path.insert(0, str(HERE.parent / "src"))

from bench_common import time_it, write_results  # noqa: E402
from request_scheduler import FifoScheduler, PriorityScheduler, Scheduler  # noqa: E402

SIZES = [1_000, 10_000, 100_000]
REPEATS = 5


def run(scheduler_cls: type[Scheduler], priorities: list[int]) -> None:
    counter = itertools.count()
    scheduler = scheduler_cls(id_factory=lambda: str(next(counter)))
    for p in priorities:
        scheduler.submit("payload", priority=p)
    while len(scheduler):
        scheduler.next_request()


def main() -> None:
    results: list[dict[str, Any]] = []
    for n in SIZES:
        rng = random.Random(0)
        priorities = [rng.randint(0, 9) for _ in range(n)]
        row: dict[str, Any] = {"n": n}
        for name, cls in (("fifo", FifoScheduler), ("priority", PriorityScheduler)):
            timing = time_it(partial(run, cls, priorities), REPEATS)
            timing["us_per_request"] = timing["median_s"] / n * 1e6
            row[name] = timing
        results.append(row)
        fifo, prio = row["fifo"], row["priority"]
        print(
            f"n={n:>7}: fifo {fifo['median_s'] * 1e3:8.1f} ms ({fifo['us_per_request']:.2f} us/req)"
            f" | priority {prio['median_s'] * 1e3:8.1f} ms ({prio['us_per_request']:.2f} us/req)"
        )
    path = write_results(
        "request-scheduler",
        "measured: wall-clock on the recorded machine; not simulated",
        {
            "description": "Submit n requests, then dispatch all n (no cancellations).",
            "priority_levels": 10,
            "seed": 0,
            "results": results,
        },
    )
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
