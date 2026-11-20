# Progress tracker

An honest record of what the repository **owner** has demonstrated, kept separate from what the
repository **contains**. Reference implementations in this repository were written with AI
assistance; they are study material and do not change any status below
([ADR 0004](decisions/0004-provenance-and-honest-progress.md)).

## Status definitions

| # | Status | Meaning | What moves a concept to it |
|---|--------|---------|-----------------------------|
| 1 | **Introduced** | Seen or discussed; may rely on notes | Appears in a session |
| 2 | **Conceptually understood** | Can explain it in own words and predict simple behaviour without notes | Explain-back review (spoken or written) |
| 3 | **Guided implementation** | Implemented with hints or with a reference at hand | Submitted code produced with guidance |
| 4 | **Independently implemented** | Implemented from a specification, without looking at a solution | Submitted code **and** its own tests, reviewed |
| 5 | **Mastered** | Can explain, test, modify, and apply it to an unfamiliar problem | Reviewed modification task and an unfamiliar-problem task |

Rules: no skipping levels; no promotion on the basis of reference code in this repository;
demotion is allowed if a later review shows a gap.

## Baseline (conservative)

The owner reports that earlier topics were covered through discussion and guided examples and that
not all assigned exercises were submitted. No independent submission has been reviewed, so every
concept starts at **Introduced**. The Python items are candidates for promotion to level 2 after a
short explain-back review.

| Area | Concept | Status | Independent work reviewed | Reference material in repo (does not raise status) |
|------|---------|--------|---------------------------|----------------------------------------------------|
| Python | List mutability and references | Introduced | None | [mutability](../01-python-foundations/mutability/) |
| Python | Set-based duplicate detection | Introduced | None | [sets-hashmaps](../02-data-structures-algorithms/sets-hashmaps/) |
| Python | Functions and return values | Introduced | None | [functions](../01-python-foundations/functions/) |
| Python | Exceptions and input validation | Introduced | None | [exceptions](../01-python-foundations/exceptions/) |
| Python | Dictionaries and hash maps | Introduced | None | [sets-hashmaps](../02-data-structures-algorithms/sets-hashmaps/) |
| Python | Iterators and generators | Introduced | None | [iterators-generators](../01-python-foundations/iterators-generators/) |
| Python | Context managers | Introduced | None | [context-managers](../01-python-foundations/context-managers/) |
| Python | Modules, packages, imports | Introduced | None | [modules-packages](../01-python-foundations/modules-packages/) |
| CS | Basic data structures | Introduced | None | [02-data-structures-algorithms](../02-data-structures-algorithms/) |
| CS | FIFO queues and deques | Introduced | None | [queues-deques](../02-data-structures-algorithms/queues-deques/) |
| CS | Heaps and priority scheduling | Introduced | None | [heaps-priority-queues](../02-data-structures-algorithms/heaps-priority-queues/) |
| CS | Time and space complexity | Introduced | None | [complexity-analysis](../02-data-structures-algorithms/complexity-analysis/) |
| CS | Basic probability reasoning | Introduced | None | not yet covered |
| ML | Overfitting and generalisation | Introduced | None | not yet covered |
| SQL | Filtering and aggregation | Introduced; known confusion between row filtering (`WHERE`) and group aggregation (`GROUP BY`/`HAVING`) | None | [databases-postgresql](../05-backend-distributed-systems/databases-postgresql/) |

Everything else in the roadmap (testing discipline, concurrency, networking, PostgreSQL, ML
infrastructure, inference serving, GPUs) is **not started** and is not listed until it is.

## Unresolved exercises

These are learning tasks. None is evidence of a skill until submitted and reviewed.
Attempt each **before** reading the corresponding reference implementation in this repository.
Submit to `<topic-directory>/exercises/<name>.py` with your own `test_<name>.py`.

| ID | Exercise | Acceptance criteria | Status if accepted |
|----|----------|---------------------|--------------------|
| E-01 | **Independent generator implementation**: write `chunked(iterable, size)` and a lazy `read_lines(path)` | Works on an infinite source; file closed on early `close()`; own tests include `size < 1` and an empty input | Independently implemented (Iterators and generators) |
| E-02 | **Context manager implementation**: a class-based and a `@contextmanager` version of a resource that records open/close | Closed on success **and** on exception; exception still propagates; close is idempotent | Independently implemented (Context managers) |
| E-03 | **Resource lifecycle tests**: tests for E-02 | A test per path: normal exit, exception in body, use-after-close, double close | Part of E-02 acceptance |
| E-04 | **Independent function implementation**: `normalize`-style pure function, a closure counter, a keyword-only parameter | No mutation of arguments; correct `nonlocal`; failure cases tested | Independently implemented (Functions) |
| E-05 | **Queue implementation**: FIFO queue with `enqueue`, `dequeue`, `__len__`, `QueueEmptyError`, no `list.pop(0)` | Passes your own tests, including interleaved operations and empty-queue failure; one-paragraph explanation of its complexity | Independently implemented (FIFO queues) |
| E-06 | **Heap-based scheduling**: scheduler with priorities and FIFO order within a priority, using `heapq` | Equal-priority test; cancellation test; written complexity of each operation | Independently implemented (Heaps and priority scheduling) |
| E-07 | **SQL filtering and grouping**: five queries on a table you design, mixing `WHERE`, `GROUP BY` and `HAVING`; each with a sentence stating which rows each clause sees | Results verified by a test or by hand-computed expected output; the `WHERE`-vs-`HAVING` distinction explained correctly | Conceptually understood → Guided or Independently implemented, depending on assistance |
| E-08 | **Independent project tests**: write the test suite for a small module *before* looking at the existing tests | Normal, edge and failure cases; at least one test that fails when the implementation is deliberately broken | Contributes to level 4 for the module under test |

## Review log

| Date | Item | Outcome |
|------|------|---------|
| 2026-11-19 | Repository created; baseline set | All concepts Introduced; no independent work submitted |
