# Engineering principles

These govern how code and documentation are written here. Each is checkable in review.

## 1. The evidence rule

> Every important technical claim must be supported by an explanation, an implementation,
> a test, or a reliable reference.

Full text, adequacy table and enforcement: [ADR 0001](decisions/0001-evidence-rule.md).
The claims themselves: [claims-register.md](claims-register.md).

## 2. Correctness before cleverness

Start with the simplest implementation that is correct and tested. Add structure only when a test,
a benchmark or a stated requirement demands it. Project 01 is deliberately a single-process
scheduler, not a distributed one.

## 3. Tests specify behaviour, including failure

Each unit has normal, edge and failure cases. A test that restates the implementation or cannot
fail is worse than none. Useful patterns used here:

* **Model-based tests**: compare against a slow, obviously correct reference under seeded random
  operations (`test_scheduler_model_based.py`).
* **Operation counting**: assert comparisons or copies, not wall-clock time
  (`test_binary_heap.py`).
* **Pitfall tests**: demonstrate the bug, then the fix (`test_mutability.py`).
* **Injected dependencies**: clocks, sleeps and ID factories are parameters, so no test sleeps or
  depends on the current time.

## 4. Measure, do not guess

Performance statements come from a benchmark that records its environment and is labelled
**measured** or **simulated**. Simulated numbers are never presented as hardware measurements.
See [benchmarks/methodology.md](../benchmarks/methodology.md).

## 5. State the limits

Every implementation documents what it does not do (unbounded record storage, no persistence,
single process). A trade-off without a stated cost is marketing.

## 6. Validate at boundaries, trust inside

Untrusted input is validated once, where it enters, into a typed object. Internal code then
relies on the invariants. Errors are specific exception types, never bare `Exception` or silent
`None`.

## 7. Types are documentation that a tool checks

`mypy --strict` runs in CI. Protocols describe the seams (`ModelBackend`, `Predictor`,
`FifoQueue`) so implementations can be swapped, for example a simulated backend for a real engine.

## 8. Small, honest scope

No directory without content ([ADR 0003](decisions/0003-no-empty-directories.md)). No dependency
without a reason ([ADR 0002](decisions/0002-minimal-toolchain.md)). No status without evidence
([ADR 0004](decisions/0004-provenance-and-honest-progress.md)).

## 9. Documentation template

Every concept page follows the same ten headings so that pages are comparable and gaps are visible:
Problem · First-principles explanation · Technical details · Implementation · Expected behaviour ·
Tests · Engineering trade-offs · AI-infrastructure connection · Common mistakes · References.
