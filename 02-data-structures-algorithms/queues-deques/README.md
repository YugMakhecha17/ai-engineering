# Queues and deques

Code: [`fifo_queues.py`](fifo_queues.py) · Tests: [`test_fifo_queues.py`](test_fifo_queues.py)
Benchmark: [`../../benchmarks/queue_pop_benchmark.py`](../../benchmarks/queue_pop_benchmark.py)
→ [`results/queue-pop.json`](../../benchmarks/results/queue-pop.json)

## 1. Problem
Requests must be served in arrival order (FIFO). A list makes `append` cheap but `pop(0)` expensive.
Why, and what should replace it?

## 2. First-principles explanation
A list stores elements contiguously. Removing the first element leaves a hole at index 0, so every
remaining element is shifted one slot left: n − 1 moves. A deque (double-ended queue) keeps
elements in linked fixed-size blocks and tracks both ends, so removing from the front touches
O(1) memory. A ring buffer achieves the same with one array and two moving indexes that wrap
around using `%`.

## 3. Technical details
| Operation | `list` | `collections.deque` | `RingBufferQueue` |
|-----------|--------|---------------------|-------------------|
| enqueue (append) | O(1) amortised | O(1) | O(1) amortised |
| dequeue (pop front) | **O(n)** | O(1) | O(1) |
| index in the middle | O(1) | O(n) | O(1) (not exposed) |

The ring buffer grows by doubling when full and must *unwrap* the data into logical order when it
does so; a bug there is only visible when growth happens while `head ≠ 0` (tested).

## 4. Runnable implementation
`ListQueue`, `DequeQueue`, `RingBufferQueue` behind one `FifoQueue` protocol.

## 5. Expected behaviour
Measured on the machine in `queue-pop.json` (CPython 3.12.3, **1 CPU, shared sandbox VM**). Wall-clock,
median of 5 runs; absolute numbers are not portable:

| n | `list.pop(0)` | `deque.popleft` | ring buffer (pure Python) |
|---|--------------:|----------------:|--------------------------:|
| 1,000 | 0.05 ms | 0.02 ms | 0.39 ms |
| 10,000 | 100.95 ms | 0.21 ms | 4.19 ms |
| 50,000 | 2,656.79 ms | 1.14 ms | 20.09 ms |

Reading the numbers honestly:
* From 10,000 to 50,000 (5× the items) the list time grew 26×, consistent with O(n²) (predicted 25×).
* From 1,000 to 10,000 it grew about 2,000× where O(n²) predicts 100×. A likely cause is the list
  outgrowing CPU cache so each shift gets slower; **that hypothesis was not tested here.**
* The hand-written ring buffer is about 18× slower than `deque` at 50,000 because it is
  interpreted Python while `deque` is implemented in C. Its purpose is to show the mechanism; use
  `deque` in real code.

## 6. Tests
All three satisfy the same FIFO contract (parametrised): order, interleaving, empty-queue error,
reuse after draining. Ring-buffer specifics: wrap-around without growth, growth while wrapped,
reference release, `peek`. A seeded 3,000-operation comparison with `collections.deque`.
Tests do **not** assert wall-clock speed, because that would be flaky.

## 7. Engineering trade-offs
Use `deque` for FIFO. A list is acceptable only when the queue is tiny or processed in one pass and
discarded. Use a ring buffer when a *fixed capacity* is required (bounded queue, backpressure),
because a full buffer is an explicit, detectable condition. `queue.Queue` adds locking for threads
and is slower in single-threaded code.

## 8. AI-infrastructure connection
Request queues in front of a model server are FIFO or priority queues; a quadratic dequeue turns a
traffic spike into a latency collapse, because the cost per dequeue grows with queue depth, the
exact moment you can least afford it. Bounded ring buffers model admission control.

## 9. Common mistakes
`pop(0)` or `insert(0, x)` on a list in a hot path; unbounded queues that hide overload; forgetting
to clear references in a hand-written buffer; using `queue.Queue` where no threads are involved.

## 10. References
* `collections.deque`: <https://docs.python.org/3/library/collections.html#collections.deque>
* Time complexity table: <https://wiki.python.org/moin/TimeComplexity>
* Benchmark method: [../../benchmarks/methodology.md](../../benchmarks/methodology.md)
