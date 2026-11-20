# 02 · Data structures and algorithms

Implementations, with operation counts, for the structures that scheduling and serving systems are
built from. The aim is to know *why* a structure fits, *when it stops fitting*, and to be able to
prove it with a test.

| Topic | Code | Key question answered with evidence |
|-------|------|--------------------------------------|
| [Lists and arrays](lists-arrays/) | `dynamic_array.py` | Why is `append` O(1) amortised but `insert(0, x)` O(n)? |
| [Sets and hash maps](sets-hashmaps/) | `hash_structures.py` | Dict vs list for finding a request by ID; what happens on collisions? |
| [Queues and deques](queues-deques/) | `fifo_queues.py` | Why `deque` instead of `list.pop(0)` for FIFO? |
| [Heaps and priority queues](heaps-priority-queues/) | `binary_heap.py` | Why a heap for priority scheduling, and why is it not stable by itself? |
| [Complexity analysis](complexity-analysis/) | `searching_sorting.py` | How do you *measure* O(log n) and O(n²) without a stopwatch? |
| [Problem solving](problem-solving/) | `sliding_window.py` | How do you decompose a rate-limiting problem? |

Run this section: `python -m pytest 02-data-structures-algorithms`

**Provenance.** All implementations are AI-assisted reference material and raise no status in the
[progress tracker](../docs/progress-tracker.md). Exercises E-05 (queue) and E-06 (heap scheduling)
are the owner's to complete independently; attempt them before reading these files.

**Method.** Complexity claims are asserted by tests that count comparisons, copies or shifts, so
they hold on any machine. Wall-clock benchmarks live in [`../benchmarks/`](../benchmarks/) and are
labelled as measurements.
