# Testing strategy and test-driven development

Code: [`duration_parser.py`](duration_parser.py) · Tests: [`test_duration_parser.py`](test_duration_parser.py)

## 1. Problem
Code that "seems to work" breaks on the inputs nobody tried. Tests turn expectations into a
specification the machine can check on every change.

## 2. First-principles explanation
A test calls code with a chosen input and asserts the observable result. A useful suite covers
**normal** cases, **edge** cases (empty, boundary, duplicate), and **failure** cases (the correct
error is raised). A test is only valuable if it would **fail** when the code is wrong.

## 3. Technical details: strategy used in this repository
| Level | Purpose | Example here |
|-------|---------|--------------|
| Unit | One function or class, no I/O | `test_duration_parser.py` |
| Property / model-based | Compare with a slow reference on random seeded input | `test_scheduler_model_based.py` |
| Operation counting | Assert complexity bounds deterministically | `test_binary_heap.py` |
| Pitfall | Demonstrate a bug and its fix | `test_mutability.py` |
| Subprocess / contract | Run the real entry point | `test_modules_packages.py`, `test_example_output.py` |
| Static | Types rejected before running | `test_mypy_rejects_what_runtime_accepts` |

Conventions: `pytest`; `parametrize` for tables of cases; `tmp_path` for files; injected clocks and
sleeps (never `time.sleep` in tests); fixed random seeds; no network.

## 4. Runnable implementation: TDD worked example
`parse_duration("1h30m") → 5400.0`. The test file is ordered as the work was done:

1. **Red** `test_single_unit` fails (no function). **Green** the simplest code passes.
2. Parametrise all units; adding a case is one line.
3. Compound values in any order.
4. A bug surfaced while writing step 2: is `5ms` milliseconds or `5m` + `5s`? A test pins the decision
   and the regex lists `ms` before `m`.
5. Failure cases specified explicitly (`""`, `"5"`, `"1.5h"`, `" 5s"`, `"5S"`…).
6. **Refactor** with the tests as a safety net.

(The commit history of a new feature should show this rhythm: failing test, passing code, refactor.)

## 5. Expected behaviour
```python
>>> parse_duration("1h30m")
5400.0
>>> parse_duration("250ms")
0.25
>>> parse_duration("1m2m")
ValueError: duplicate unit in duration: '1m2m'
```

## 6. Tests
See the file. Run `python -m pytest 03-software-engineering/testing -v` to see each case by name.

## 7. Engineering trade-offs
Over-mocking makes tests pass while the real integration is broken; no mocking makes tests slow and
flaky. Prefer injected fakes for time and randomness, real objects otherwise. TDD is strongest for
well-specified logic (parsers, schedulers) and weaker for exploratory work; write a test the moment
the behaviour is understood.

## 8. AI-infrastructure connection
Serving correctness rests on timeouts, retries, batching limits and quotas, all of which parse
configuration and depend on time. Deterministic clocks make failure-injection tests possible.

## 9. Common mistakes
Assertions that cannot fail (`assert x or True`; one was written and removed while building this
repository); testing implementation details instead of behaviour; sleeping in tests; shared state
between tests; no failure cases.

## 10. References
* pytest: <https://docs.pytest.org/>
* `unittest` (standard library): <https://docs.python.org/3/library/unittest.html>
* Exercise: write your own tests for a module *before* opening the existing ones (E-08).
