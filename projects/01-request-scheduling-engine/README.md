# Project 01 · Request scheduling engine

A single-process Python scheduler that accepts requests, orders them by policy (FIFO or priority),
dispatches them, and tracks each through an explicit lifecycle. It exists to demonstrate data
structures, algorithms, state management and failure handling on the problem that sits at the front
of every model server.

**Status: initial version implemented and verified** (see "Verification"). Not distributed, not
thread-safe, not persistent. It does not yet batch.

## Quick start
```bash
# from the repository root, after `pip install -e ".[dev]"`
python projects/01-request-scheduling-engine/examples/basic_usage.py
python -m pytest projects/01-request-scheduling-engine
python projects/01-request-scheduling-engine/benchmarks/bench_schedulers.py
```

```python
from request_scheduler import PriorityScheduler

s = PriorityScheduler()
s.submit("interactive", priority=0)
s.submit("batch job", priority=5)
req = s.next_request()  # QUEUED -> RUNNING: returns the priority-0 request
s.complete(req.request_id)  # RUNNING -> COMPLETED
```

Output of the example (asserted by `test_example_runs_and_prints_the_documented_output`):
```text
== FIFO ==
req-1: summarise report
req-2: translate memo
req-3: classify ticket
== Priority (lower number = more urgent) ==
queued after cancel: 4
req-2 (p=0): interactive A
req-3 (p=0): interactive B
req-1 (p=5): batch job
req-5 (p=9): background
```

## Features implemented
Request creation with generated or caller-supplied IDs · metadata (deep-copied, read-only) · FIFO
scheduling (`deque`) · priority scheduling (`heapq`, lower number first) · stable ordering for
equal priorities · dictionary-based tracking by ID · completion and cancellation with an enforced state
machine · input validation · specific exception types · injected clock and ID factory.

## Architecture
Details and class diagram: [docs/architecture.md](docs/architecture.md).
Lifecycle and dispatch diagrams: [request-lifecycle](../../docs/architecture/diagrams/request-lifecycle.md),
[scheduling](../../docs/architecture/diagrams/scheduling.md).

* `Scheduler` (base class) owns the records dict, validation and the state machine.
* `FifoScheduler` and `PriorityScheduler` supply only the ordering structure.
* Cancellation is **lazy**: O(1) mark, discard when the entry reaches the front.

## Complexity (n = live queued requests)
| Operation | FIFO | Priority | Evidence |
|-----------|------|----------|----------|
| `submit` | O(1) | O(log n) | `heapq` documented cost; heap bounds asserted for the hand-written heap in section 02 |
| `next_request` | O(1) amortised | O(log n) amortised | Amortised over skipped cancelled entries; each stale entry is skipped once |
| `cancel`, `complete`, `get_state`, `get_request` | O(1) | O(1) | dict lookup; `test_lazy_deletion_leaves_stale_entries_until_they_surface` |
| memory | O(requests ever submitted) | same | records are never pruned (limitation below) |

## Verification
| Claim | Evidence |
|-------|----------|
| Equal priorities are served in arrival order | `test_equal_priorities_are_served_in_arrival_order` (2–100 jobs) and interleaved case |
| Both schedulers match a brute-force reference | `test_scheduler_matches_brute_force_reference`: 10 seeded runs × 3,000 random operations |
| Cancelled requests are never dispatched; stale entries purged on the next dispatch | `test_cancelled_queued_request_is_never_dispatched`, `test_lazy_deletion_...` |
| Terminal states are final; invalid transitions rejected and change nothing | `test_terminal_states_are_final`, `test_cannot_complete_a_request_that_never_started` |
| A rejected `submit` leaves the scheduler unchanged | `test_failed_submit_leaves_no_trace` |
| Metadata cannot be altered after submission | `test_metadata_is_a_deep_read_only_snapshot` |
| IDs are never reused | `test_duplicate_ids_are_rejected_even_after_the_request_finished` |

The full list with pointers is in the [claims register](../../docs/claims-register.md).

## Benchmarks (measured, not simulated)
`benchmarks/bench_schedulers.py` submits n requests then dispatches all of them (no cancellations).
Result file: [`benchmarks/results/request-scheduler.json`](../../benchmarks/results/request-scheduler.json).
Environment: CPython 3.12.3, Linux x86-64, **1 CPU in a shared sandbox VM**, no GPU; median of 5 runs.

| n | FIFO (µs/request) | Priority (µs/request) |
|---|------------------:|----------------------:|
| 1,000 | 1.70 | 2.05 |
| 10,000 | 1.88 | 2.69 |
| 100,000 | 2.60 | 5.72 |

Interpretation, with limits: priority costs more per request than FIFO and the gap widens with n,
which is consistent with O(log n) vs O(1), but three sizes on one noisy shared machine do not
*prove* a growth rate; the operation-count tests do that for the heap. FIFO per-request time also
rises with n, so costs other than the queue (record creation, dict growth, memory effects) matter and
were not separated here. Repeat on your own hardware before quoting any figure.

## Known limitations
1. **Unbounded records**: `_records` keeps every request ever submitted. A long-running service needs
   pruning of finished requests; naive pruning would break the duplicate-ID guarantee and can confuse
   stale queue entries with a re-used ID, so it needs sequence-checked entries. Not built.
2. **Lazy deletion holds memory** until stale entries surface (`physical_size`); a heap of mostly
   cancelled entries is wasteful. Compaction is not implemented.
3. **No starvation protection**: a stream of priority-0 requests can postpone priority-9 ones
   indefinitely. Priority ageing or per-priority FIFOs with weighted service would address it. Not built.
4. **Not thread-safe**; **no persistence**; **no expiry**; **no queue limit** (so no backpressure).
5. FIFO ignores `priority` by design.
6. Running requests that are cancelled are only *marked*; nothing stops the work (cooperative
   cancellation is the caller's job).

## Roadmap (progressive features)
| Order | Feature | Success evidence |
|-------|---------|------------------|
| 1 | Queue limit with `QueueFullError` | Test for rejection at capacity and recovery |
| 2 | Request expiry (deadline) | Fake-clock test: expired request never dispatched |
| 3 | Batching: `next_batch(max_batch_size)` | Order preserved; size never exceeded; empty-queue behaviour |
| 4 | Token-budget constraint on a batch | Budget never exceeded; documented policy when the next request does not fit |
| 5 | Fairness: priority ageing | Test that a low-priority request is eventually served under sustained load |
| 6 | Benchmarks of the above | Measured, environment recorded |

These are also natural exercises for the owner to implement independently.

## Questions this project can answer (and the evidence)
* *Why a heap rather than sorting on every arrival?* O(log n) per operation vs O(n log n); counted in
  `test_binary_heap.py`; this project uses it.
* *Why is a heap alone not enough for stable ordering?* It reorders equal keys (A, D, C, B in
  `test_heap_alone_is_not_stable_for_equal_priorities`); the sequence tie-breaker fixes it.
* *How do you cancel something in the middle of a queue cheaply?* Lazy deletion; cost and memory
  trade-off documented and tested.
* *How do you know it is correct?* Model-based test against a brute-force reference.
* *What would break it at scale?* The limitations above, in order of severity: unbounded records, no
  backpressure, starvation.
