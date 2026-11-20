# Engineering principles in practice

The repository-wide principles are in [docs/engineering-principles.md](../../docs/engineering-principles.md).
This page shows them in actual code, so each point can be checked rather than believed.

## Separation of concerns, cohesion, coupling: project 01

| Concern | Where | Why separate |
|---------|-------|--------------|
| Data and states | `models.py` (`Request`, `RequestState`, `ALLOWED_TRANSITIONS`) | Pure data; no behaviour to test through a queue |
| Lifecycle, validation, record keeping | `Scheduler` base class | One place enforces "who may move to which state" |
| Ordering policy | `FifoScheduler`, `PriorityScheduler` implement only `_push`/`_pop_id` | A new policy (deadline, fair share) adds ~10 lines and inherits all lifecycle tests |
| Errors | `errors.py` hierarchy | Callers catch `SchedulerError` or one specific type |

High cohesion: the transition table lives next to the states it governs. Low coupling: schedulers
depend on a clock and ID factory passed in as plain callables, not on `time` or `uuid` directly, so
tests control both.

## Clean code, concretely
* Names state intent: `next_request`, `physical_size`, `ALLOWED_TRANSITIONS`.
* Functions do one thing: `_freeze_metadata` only copies and freezes.
* No magic numbers: `MAX_PROMPT_CHARS`, `MAX_LOAD_FACTOR`.
* Comments explain *why* (e.g. why `ms` precedes `m` in a regex), not what.
* Reuse by composition and small functions, not by copy-paste: both schedulers share `submit`.

## Error handling
Specific exception types; validation at the boundary; the original cause preserved with `raise ... from`;
a failed `submit` leaves no trace (`test_failed_submit_leaves_no_trace`).

## Logging
Use the `logging` module with a module-level `logger = logging.getLogger(__name__)`, never `print`, in
library code. Include identifiers (request ID) in messages. DEBUG for development detail, INFO for
lifecycle events, WARNING for recoverable anomalies, ERROR for failures. Example:
`moving_average.py`, tested with `caplog`.

## Code review checklist
- [ ] Does every new important claim have evidence, with a row in the claims register?
- [ ] Is there a failing-case test, not only the happy path?
- [ ] Could the test fail if the code were wrong?
- [ ] Are limits and trade-offs stated?
- [ ] Are side effects (time, randomness, I/O) injectable?
- [ ] Do lint, `mypy --strict` and the evidence check pass?
- [ ] Is any AI-assisted code labelled and the progress tracker left honest?

## References
* PEP 8: <https://peps.python.org/pep-0008/>
* `logging` HOWTO: <https://docs.python.org/3/howto/logging.html>
