"""Measure draining a FIFO queue: list.pop(0) vs collections.deque.popleft vs ring buffer.

Run from the repository root:  python benchmarks/queue_pop_benchmark.py
Data kind: MEASURED wall-clock time on the machine recorded in the output file.
"""

from __future__ import annotations

import sys
from collections import deque
from functools import partial
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "02-data-structures-algorithms" / "queues-deques"))

from bench_common import time_it, write_results  # noqa: E402
from fifo_queues import RingBufferQueue  # noqa: E402

SIZES = [1_000, 10_000, 50_000]
REPEATS = 5


def drain_list(n: int) -> None:
    items = list(range(n))
    while items:
        items.pop(0)


def drain_deque(n: int) -> None:
    items = deque(range(n))
    while items:
        items.popleft()


def drain_ring(n: int) -> None:
    queue: RingBufferQueue[int] = RingBufferQueue()
    for i in range(n):
        queue.enqueue(i)
    while len(queue):
        queue.dequeue()


def main() -> None:
    candidates = (
        ("list_pop0", drain_list),
        ("deque_popleft", drain_deque),
        ("ring_buffer", drain_ring),
    )
    results: list[dict[str, Any]] = []
    for n in SIZES:
        row: dict[str, Any] = {"n": n}
        for name, fn in candidates:
            row[name] = time_it(partial(fn, n), REPEATS)
        results.append(row)
        ms = {name: row[name]["median_s"] * 1e3 for name, _ in candidates}
        print(
            f"n={n:>7}: list.pop(0) {ms['list_pop0']:9.2f} ms | "
            f"deque {ms['deque_popleft']:8.2f} ms | ring {ms['ring_buffer']:8.2f} ms"
        )
    path = write_results(
        "queue-pop",
        "measured: wall-clock on the recorded machine; not simulated",
        {
            "description": "Drain n items from a FIFO queue (build + n removals).",
            "results": results,
        },
    )
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
