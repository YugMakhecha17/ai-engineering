# Heaps and priority queues

Code: [`binary_heap.py`](binary_heap.py) · Tests: [`test_binary_heap.py`](test_binary_heap.py)
Used in: [project 01](../../projects/01-request-scheduling-engine/) (`PriorityScheduler`, via `heapq`)

## 1. Problem
Always serve the most urgent request next, while new requests keep arriving. Re-sorting a list on
every arrival is O(n log n); scanning for the minimum on every dispatch is O(n).

## 2. First-principles explanation
A **binary min-heap** stores items in an array arranged as a complete binary tree where each parent
≤ its children. The minimum is always at index 0. Inserting appends at the end and swaps upward
while smaller than the parent (**sift-up**). Removing the minimum moves the last item to the root
and swaps it downward with its smaller child (**sift-down**). A complete tree with n nodes has height
⌊log₂ n⌋, so both operations are O(log n).

## 3. Technical details
* Parent of `i` is `(i−1)//2`; children are `2i+1`, `2i+2`.
* `peek` O(1); `push` O(log n); `pop` O(log n); building from n items with Floyd's `heapify` O(n).
* **Counted bounds (asserted by tests):** push ≤ ⌊log₂ n⌋ comparisons; pop ≤ 2⌊log₂ n⌋; heapify
  ≤ 2n.
* A heap orders only parent-vs-child; siblings are unordered, so it cannot do range queries or
  efficient arbitrary delete.
* **Not stable.** With equal priorities, order is not arrival order. Pushing A, B, C, D with equal keys
  pops A, D, C, B (asserted by a test).

## 4. Runnable implementation
`BinaryHeap` (with a comparison counter and optional `key`) and `StablePriorityQueue`, which pushes
`(priority, sequence, item)` so every key is unique.

## 5. Expected behaviour
```python
>>> pq = StablePriorityQueue()
>>> for label in "ABCD": pq.push(1, label)
>>> pq.push(0, "urgent")
>>> [pq.pop() for _ in range(len(pq))]
['urgent', 'A', 'B', 'C', 'D']
```

## 6. Tests
Sorted output vs `sorted`; invariant after every operation; empty-heap errors; duplicates;
interleaved push/pop against a reference; comparison-count bounds at n = 16…5,000; linear
heapify; the instability demonstration; stable queue ordering.

## 7. Engineering trade-offs and limitations
| Need | Structure |
|------|-----------|
| Next-most-urgent, many arrivals | Heap |
| Strict arrival order | Deque |
| Few distinct priority levels | One FIFO per level (O(1), naturally stable, simple fairness) |
| Cancel or re-prioritise arbitrary items | Heap with lazy deletion, or an indexed heap |
| Range or ordered iteration | Balanced tree / sorted container |

Limitations of priority scheduling itself, regardless of structure: **starvation** (a steady stream
of urgent requests can postpone low-priority ones forever; mitigations are priority ageing or
weighted fair queueing), and priority inversion when a low-priority holder blocks a high one.
Neither is solved in this repository yet.

## 8. AI-infrastructure connection
Schedulers choose which request enters the next batch; priority and deadline-aware ordering is
common. Project 01's `PriorityScheduler` applies this heap with the sequence tie-breaker.

## 9. Common mistakes
Assuming a heap is sorted or stable; comparing non-comparable payloads when priorities tie (the
sequence number prevents this); mutating an item's priority while it is in the heap.

## 10. References
* `heapq`, including the priority-queue implementation notes (sequence tie-breaker, lazy removal):
  <https://docs.python.org/3/library/heapq.html>
* Time complexity table: <https://wiki.python.org/moin/TimeComplexity>
