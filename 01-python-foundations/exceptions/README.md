# Exceptions and input validation

Code: [`request_validation.py`](request_validation.py) · Tests: [`test_request_validation.py`](test_request_validation.py)

## 1. Problem
Malformed input must be rejected with a precise reason at the boundary, not discovered later as an
obscure failure deep inside the system.

## 2. First-principles explanation
When an operation cannot succeed, Python raises an exception that unwinds the call stack until a
matching `except` handles it. Validation turns untrusted data into a trusted, typed object once, so
inner code can assume its invariants.

## 3. Technical details
* Define a small hierarchy: `ValidationError(ValueError)` for bad caller input, `ConfigError` for
  bad configuration. Callers can catch precisely.
* Catch only what you can handle. Swallowing everything hides bugs (`try_validate` handles
  `ValidationError` but lets `AttributeError` from a programming mistake escape).
* `raise New(...) from exc` preserves the original as `__cause__`; `from None` hides it.
* `bool` is a subclass of `int`, so `isinstance(True, int)` is `True`; reject it explicitly.

## 4. Runnable implementation
`validate_request` (prompt, `max_tokens`, `temperature`), `max_tokens_from_env` (error translation
with chaining), `try_validate`.

## 5. Expected behaviour
```python
>>> validate_request({"prompt": "hello", "max_tokens": 16})
InferenceRequest(prompt='hello', max_tokens=16, temperature=1.0)
>>> validate_request({"prompt": "x", "max_tokens": True})
ValidationError: max_tokens must be an integer, got bool
```

## 6. Tests
Twelve parametrised invalid payloads; the bool trap; chaining (`__cause__`); range checks;
non-mapping input is not swallowed.

## 7. Engineering trade-offs
Fail-fast reports one problem per call; collecting all errors is friendlier to API clients but more
code. Exceptions suit exceptional failures; for expected "no result" outcomes a `None` return or
a result type may be clearer. EAFP (try, then handle) avoids check-then-use races; LBYL (check
first) gives clearer messages.

## 8. AI-infrastructure connection
Every serving endpoint validates prompt length, token limits and sampling parameters before work is
queued. Project 02's API layer will use Pydantic for the same job; this module shows the underlying
mechanism.

## 9. Common mistakes
Bare `except:`; catching `Exception` and continuing; losing the original cause; validating the same
field in several places; leaking internal exception text to clients.

## 10. References
* Errors and exceptions: <https://docs.python.org/3/tutorial/errors.html>
* Built-in exceptions: <https://docs.python.org/3/library/exceptions.html>
* PEP 3134, exception chaining: <https://peps.python.org/pep-3134/>
