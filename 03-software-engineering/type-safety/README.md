# Type safety

Code: [`typed_predictors.py`](typed_predictors.py) · Tests: [`test_typed_predictors.py`](test_typed_predictors.py)

## 1. Problem
Passing the wrong kind of object is found at runtime, possibly in production, possibly only on a rare path.

## 2. First-principles explanation
Annotations (`def f(x: int) -> str`) declare intent. Python **ignores them at runtime**. A static
checker (`mypy`) reads them and reports mismatches before the program runs.

## 3. Technical details
* `Protocol`: structural typing. Anything with a compatible `predict` method is a `Predictor`; no
  inheritance required.
* `Generic[M]` / `TypeVar(bound=...)`: a container that remembers what it holds
  (`ModelRegistry[LinearModel].get()` returns `LinearModel`).
* `@dataclass(frozen=True)`: immutable value objects; assignment raises `AttributeError`.
* `X | None` makes "may be absent" visible so the checker forces handling it.
* Annotations do not validate data. Untrusted input still needs runtime validation
  ([exceptions](../../01-python-foundations/exceptions/)).
* This repository runs `mypy --strict` over all code in CI.

## 4. Runnable implementation
`Predictor`, `LinearModel`, `ConstantModel`, `predict_batch`, `ModelRegistry`, `UnknownModelError`.

## 5. Expected behaviour
```python
>>> LinearModel(weights=(2.0, 3.0), bias=1.0).predict([1.0, 2.0])
9.0
```

## 6. Tests
Predict and feature-count validation; an unrelated class accepted structurally; registry
duplicate/unknown errors; frozen dataclass; **a runtime test showing a `str` is stored in a `float`
field without complaint**; **a subprocess test running `mypy --strict` on a bad call and asserting
that it exits non-zero with an `arg-type` error** (marked `slow`).

## 7. Engineering trade-offs
Strict typing catches a class of bugs early and documents interfaces, at the cost of annotation
effort and occasional `# type: ignore` where Python is too dynamic. Protocols decouple modules but
are checked only statically. Use Pydantic (a later addition) when data must be *validated* at runtime.

## 8. AI-infrastructure connection
`ModelBackend` in project 02 is a `Protocol`: the serving layer depends on the behaviour, so a
simulated model can be replaced by a real inference engine without changing callers.

## 9. Common mistakes
Believing annotations are enforced; `Any` everywhere (it switches checking off); annotating with
concrete types where a `Protocol` or `Sequence` would do; silencing errors with `# type: ignore`
without a comment.

## 10. References
* `typing`: <https://docs.python.org/3/library/typing.html>
* PEP 484: <https://peps.python.org/pep-0484/> · PEP 544 (Protocols): <https://peps.python.org/pep-0544/>
* mypy: <https://mypy.readthedocs.io/>
