# Debugging

Code: [`moving_average.py`](moving_average.py) · Tests: [`test_moving_average.py`](test_moving_average.py)

## 1. Problem
Something returns the wrong result. Guessing wastes hours; a method finds the cause and leaves a
test behind so it cannot return.

## 2. First-principles explanation
Debugging is hypothesis testing. Make the failure reproducible, shrink it, form a hypothesis about
which line is wrong, observe the real values, fix the cause, then lock the fix in with a test.

## 3. Technical details: the method
1. **Reproduce** with the smallest input that fails.
2. **Read** the traceback bottom-up; the last frame is where it failed, not necessarily where it went wrong.
3. **Hypothesise** before touching code.
4. **Observe**: `breakpoint()` / `python -m pdb script.py` / `pytest --pdb` (stop at first failure),
   or the `logging` module at DEBUG level. Prefer `logging` to `print`: levels, timestamps, and it
   can stay in the code.
5. **Fix the cause**, not the symptom.
6. **Add a regression test** that fails on the old code.

Useful commands: `pytest -x` (stop at first failure), `pytest --lf` (rerun last failures),
`pytest -k name`, `pytest -vv`, in `pdb`: `n` next, `s` step, `c` continue, `p expr`, `l` list, `q` quit.

## 4. Runnable implementation: a worked (staged) example
The following bug was **written on purpose for teaching**; it is not a defect found in real code.

```python
def moving_average(values, window):
    result = []
    current = sum(values[:window])
    result.append(current / window)
    for i in range(window, len(values) - 1):  # BUG: off by one
        current += values[i] - values[i - window]
        result.append(current / window)
    return result
```
Symptom: `moving_average([10, 20, 30, 40], 2)` returns `[15.0, 25.0]`; expected `[15.0, 25.0, 35.0]`.

* Reproduce and shrink: four values, window 2.
* Hypothesis: output is one short, so the loop stops one iteration early.
* Observe: `len(result)` is 2; expected `len(values) − window + 1 = 3`. The loop bound `len(values) - 1`
  excludes the final index.
* Fix: `range(window, len(values))`.
* Regression test: `test_regression_last_window_is_included`.
* Cross-check: `test_matches_naive_recomputation` compares against a slow, obviously correct version
  for every window size.

## 5. Expected behaviour
```python
>>> moving_average([10, 20, 30, 40], 2)
[15.0, 25.0, 35.0]
```

## 6. Tests
Basic, regression, window extremes, naive cross-check, invalid windows, debug logging via `caplog`.

## 7. Engineering trade-offs
Interactive debuggers are best for state you cannot predict; logging for production and for bugs that
only appear in long runs; assertions for invariants you believe always hold. Heavy logging costs time
and can leak data.

## 8. AI-infrastructure connection
Tail-latency spikes, stuck requests and memory growth are usually found by logs and metrics rather
than a debugger. Request IDs in every log line (project 01 assigns them) make a single request
traceable end to end.

## 9. Common mistakes
Changing several things at once; "fixing" without reproducing; deleting the failing test; leaving
`print` calls behind; swallowing the exception that holds the clue.

## 10. References
* `pdb`: <https://docs.python.org/3/library/pdb.html>
* `logging`: <https://docs.python.org/3/library/logging.html>
* pytest debugging options: <https://docs.pytest.org/en/stable/how-to/failures.html>
