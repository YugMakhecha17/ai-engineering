# Context managers and resource lifecycle

Code: [`resource_managers.py`](resource_managers.py) · Tests: [`test_resource_managers.py`](test_resource_managers.py)
Diagram: [resource lifecycle](../../docs/architecture/diagrams/resource-lifecycle.md)

## 1. Problem
Resources (files, sockets, locks, GPU buffers) must be released on every path, including exceptions.
Hand-written `try/finally` repeated everywhere gets forgotten.

## 2. First-principles explanation
`with X as r:` calls `X.__enter__()` and binds its result to `r`. When the block ends, however it
ends, `X.__exit__(exc_type, exc, tb)` is called. If `__exit__` returns a true value the exception is
suppressed; otherwise it propagates.

## 3. Technical details
* Class-based (`__enter__`/`__exit__`) or generator-based (`@contextmanager`, with `try/finally`
  around `yield`).
* `ExitStack` manages a variable number of resources and closes them in reverse order, including
  after a partial failure.
* Make `close()` idempotent so cleanup code can call it defensively.
* An explicit lifecycle (`created → open → closed`) turns misuse into a loud error.

## 4. Runnable implementation
`ManagedResource` (records an event log), `timed`, `temporary_setting`, `read_all` (ExitStack).

## 5. Expected behaviour
```python
>>> with ManagedResource("a", log), ManagedResource("b", log): pass
>>> log
['open:a', 'open:b', 'close:b', 'close:a']
```

## 6. Tests (resource-lifecycle tests)
Closed after normal exit; closed and error propagated when the body raises; use-after-close
rejected; idempotent close; no reopen; reverse-order closing; partial-acquisition cleanup;
time recorded even when the body raises; setting restored after an exception.

## 7. Engineering trade-offs
`@contextmanager` is shorter; a class is better when the object needs methods, state or
introspection. Suppressing exceptions in `__exit__` is rarely right and should be explicit.

## 8. AI-infrastructure connection
Connection pools, GPU memory allocations, KV-cache blocks and inference-request slots all need
guaranteed release; a leak under error paths exhausts capacity over time.

## 9. Common mistakes
Forgetting that `__exit__` runs on exceptions; returning `True` from `__exit__` by accident;
raising from `__exit__` and masking the original error; releasing resources in `__del__`.

## 10. References
* `with` statement: <https://docs.python.org/3/reference/compound_stmts.html#the-with-statement>
* `contextlib`: <https://docs.python.org/3/library/contextlib.html>
* PEP 343: <https://peps.python.org/pep-0343/>
