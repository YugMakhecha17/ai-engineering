"""Mutation spot-check: prove that key tests can fail.

For each entry below, the script copies the repository to a temporary directory, applies ONE
deliberate bug to the copy, runs the relevant tests, and reports whether the bug was caught
("killed") or went unnoticed ("SURVIVED"). The real working tree is never modified.

This is not a full mutation-testing tool: the mutations are hand-picked to target the
behaviours that the claims register relies on. A surviving mutant means a claim's test is
weaker than it looks, OR the mutant is behaviourally equivalent to the original.

Known equivalent mutant (deliberately NOT listed): `math.ceil(float(p) * n / 100)` for the
percentile rank. It survived the exactness tests over ~20,000 (p, n) combinations, and
reasoning shows why: multiplying first and dividing second rounds correctly at these small
magnitudes. The naive `p / 100 * n` form, which does break, is listed and killed.

Usage:  python scripts/mutation_spot_check.py
Exit code 1 if any mutant survives.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

P1 = "projects/01-request-scheduling-engine"
DS = "02-data-structures-algorithms"
PY = "01-python-foundations"


@dataclass(frozen=True)
class Mutation:
    name: str
    file: str
    old: str
    new: str
    tests: str  # pytest target that should fail


MUTATIONS = [
    Mutation(
        "priority scheduler loses its stable tie-breaker",
        f"{P1}/src/request_scheduler/scheduler.py",
        "(request.priority, request.sequence, request.request_id)",
        "(request.priority, 0, request.request_id)",
        f"{P1}/tests",
    ),
    Mutation(
        "FIFO scheduler becomes LIFO",
        f"{P1}/src/request_scheduler/scheduler.py",
        "return self._queue.popleft() if self._queue else None",
        "return self._queue.pop() if self._queue else None",
        f"{P1}/tests",
    ),
    Mutation(
        "cancel forgets to decrement the queued count",
        f"{P1}/src/request_scheduler/scheduler.py",
        "        if was_queued:\n            self._queued -= 1",
        "        if was_queued:\n            pass",
        f"{P1}/tests",
    ),
    Mutation(
        "completed requests may be cancelled",
        f"{P1}/src/request_scheduler/models.py",
        "RequestState.COMPLETED: frozenset(),",
        "RequestState.COMPLETED: frozenset({RequestState.CANCELLED}),",
        f"{P1}/tests",
    ),
    Mutation(
        "metadata copied shallowly instead of deeply",
        f"{P1}/src/request_scheduler/scheduler.py",
        "MappingProxyType(copy.deepcopy(dict(metadata)))",
        "MappingProxyType(dict(metadata))",
        f"{P1}/tests",
    ),
    Mutation(
        "dispatch no longer skips cancelled entries",
        f"{P1}/src/request_scheduler/scheduler.py",
        "            if record.state is RequestState.QUEUED:",
        "            if True:",
        f"{P1}/tests",
    ),
    Mutation(
        "heap sift-down ignores the right child",
        f"{DS}/heaps-priority-queues/binary_heap.py",
        "if right < size and self._less(self._data[right], self._data[child]):",
        "if False:",
        f"{DS}/heaps-priority-queues",
    ),
    Mutation(
        "stable priority queue drops its sequence number",
        f"{DS}/heaps-priority-queues/binary_heap.py",
        "self._heap.push((priority, self._counter, item))",
        "self._heap.push((priority, 0, item))",
        f"{DS}/heaps-priority-queues",
    ),
    Mutation(
        "dynamic array grows by a constant instead of geometrically",
        f"{DS}/lists-arrays/dynamic_array.py",
        "[None] * (self.capacity * self._growth)",
        "[None] * (self.capacity + 4)",
        f"{DS}/lists-arrays",
    ),
    Mutation(
        "ring buffer forgets to unwrap on growth",
        f"{DS}/queues-deques/fifo_queues.py",
        "new_buffer[i] = self._buffer[(self._head + i) % self.capacity]",
        "new_buffer[i] = self._buffer[i]",
        f"{DS}/queues-deques",
    ),
    Mutation(
        "hash map never resizes",
        f"{DS}/sets-hashmaps/hash_structures.py",
        "if self.load_factor > self.MAX_LOAD_FACTOR:",
        "if False:",
        f"{DS}/sets-hashmaps",
    ),
    Mutation(
        "binary search probes more than log2(n)",
        f"{DS}/complexity-analysis/searching_sorting.py",
        "        mid = (low + high) // 2\n        probes += 1",
        "        mid = low\n        probes += 1",
        f"{DS}/complexity-analysis",
    ),
    Mutation(
        "rate limiter records rejected requests",
        f"{DS}/problem-solving/sliding_window.py",
        "            return False  # rejected calls are NOT recorded",
        "            self._accepted.append(now)\n            return False  # rejected calls are NOT recorded",  # noqa: E501
        f"{DS}/problem-solving",
    ),
    Mutation(
        "percentile uses the naive float form p / 100 * n",
        "projects/03-inference-observability/src/inference_observability/metrics.py",
        "math.ceil(Fraction(str(p)) * len(ordered) / 100)",
        "math.ceil(p / 100 * len(ordered))",
        "projects/03-inference-observability/tests",
    ),
    Mutation(
        "context manager only closes on success",
        f"{PY}/context-managers/resource_managers.py",
        "        self.close()  # runs on success AND on exceptions",
        "        if exc_type is None:\n            self.close()",
        f"{PY}/context-managers",
    ),
    Mutation(
        "validation accepts bool as an integer",
        f"{PY}/exceptions/request_validation.py",
        "if isinstance(value, bool) or not isinstance(value, int):",
        "if not isinstance(value, int):",
        f"{PY}/exceptions",
    ),
    Mutation(
        "chunked validates lazily instead of eagerly",
        f"{PY}/iterators-generators/generators_demo.py",
        '    if size < 1:\n        raise ValueError(f"size must be >= 1, got {size}")\n    return _chunked(items, size)',  # noqa: E501
        "    return _chunked(items, size)",
        f"{PY}/iterators-generators",
    ),
    Mutation(
        "WHERE-before-GROUP-BY query loses its WHERE",
        "05-backend-distributed-systems/databases-postgresql/where_vs_group_by.py",
        "\"WHERE status = 'ok' GROUP BY model ORDER BY model\"",
        '"GROUP BY model ORDER BY model"',
        "05-backend-distributed-systems/databases-postgresql",
    ),
]

IGNORE = shutil.ignore_patterns(
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "*.egg-info",
)


def run_mutation(mutation: Mutation) -> bool:
    """Return True if the mutant was killed (tests failed), False if it survived."""
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "repo"
        shutil.copytree(ROOT, copy, ignore=IGNORE)
        target = copy / mutation.file
        text = target.read_text(encoding="utf-8")
        if text.count(mutation.old) != 1:
            raise SystemExit(
                f"mutation '{mutation.name}': expected exactly one match in {mutation.file}, "
                f"found {text.count(mutation.old)}. Update the mutation."
            )
        target.write_text(text.replace(mutation.old, mutation.new), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-x",
                "-q",
                "-p",
                "no:cacheprovider",
                "-m",
                "not slow",
                mutation.tests,
            ],
            cwd=copy,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode != 0


def main() -> int:
    survivors = []
    for mutation in MUTATIONS:
        killed = run_mutation(mutation)
        print(f"{'killed  ' if killed else 'SURVIVED'}  {mutation.name}")
        if not killed:
            survivors.append(mutation.name)
    print(f"\n{len(MUTATIONS) - len(survivors)}/{len(MUTATIONS)} mutants killed")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
