# Functions, scope and closures

Code: [`scope_and_functions.py`](scope_and_functions.py) · Tests: [`test_scope_and_functions.py`](test_scope_and_functions.py)

## 1. Problem
Functions that mutate arguments, depend on hidden globals or return inconsistent types are hard to
test and reason about.

## 2. First-principles explanation
A function takes arguments, runs, and returns one object (`None` if no `return` executes).
"Multiple return values" is one tuple. Names are resolved by scope: Local, Enclosing, Global,
Built-in (LEGB). A function that assigns to a name anywhere in its body treats that name as local
for the *entire* body.

## 3. Technical details
* Pure function: output depends only on arguments; no side effects. Easiest to test.
* Closure: an inner function keeps its enclosing variables alive; `nonlocal` lets it rebind them.
* Closures capture the **variable**, not its value at creation (late binding).
* Keyword-only parameters (after `*`) force self-documenting call sites.

## 4. Runnable implementation
`normalize` (pure), `min_max` (tuple return), `first_even` (`int | None`), `make_counter`
(closure), `late_binding_callbacks`/`bound_callbacks`, `clamp` (keyword-only).

## 5. Expected behaviour
```python
>>> normalize([10.0, 20.0, 30.0])
[0.0, 0.5, 1.0]
>>> c = make_counter(); [c(), c(), c()]
[1, 2, 3]
>>> [f() for f in late_binding_callbacks()]
[2, 2, 2]
>>> [f() for f in bound_callbacks()]
[0, 1, 2]
```

## 6. Tests
Purity (input unchanged), empty-input failure, `None` returns, `list.sort()` returning `None`,
independent closure state, late-binding bug and fix, `UnboundLocalError` (executed from a string so
linters do not reject the deliberate bug), keyword-only enforcement.

## 7. Engineering trade-offs
Pure functions are testable and composable but may copy data; stateful closures are compact but
hide state that a small class would make explicit. Prefer a class once there are several pieces of
state or methods.

## 8. AI-infrastructure connection
Injected clocks, ID factories and sleep functions in this repository are plain callables passed as
arguments, which keeps schedulers and backends deterministic under test.

## 9. Common mistakes
Forgetting `return`; using `nonlocal` where `global` is meant; closures in loops; using the result
of a mutating method (`sort`, `append`) as if it returned the list.

## 10. References
* Scopes and namespaces: <https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces>
* Naming and binding: <https://docs.python.org/3/reference/executionmodel.html#naming-and-binding>
