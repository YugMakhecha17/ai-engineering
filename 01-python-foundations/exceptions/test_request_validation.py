import pytest
from request_validation import (
    MAX_PROMPT_CHARS,
    ConfigError,
    InferenceRequest,
    ValidationError,
    max_tokens_from_env,
    try_validate,
    validate_request,
)


def test_valid_payload_returns_typed_request_with_default_temperature() -> None:
    req = validate_request({"prompt": "hello", "max_tokens": 16})
    assert req == InferenceRequest(prompt="hello", max_tokens=16, temperature=1.0)


def test_integer_temperature_is_normalised_to_float() -> None:
    req = validate_request({"prompt": "hi", "max_tokens": 1, "temperature": 0})
    assert req.temperature == 0.0
    assert isinstance(req.temperature, float)


@pytest.mark.parametrize(
    ("payload", "fragment"),
    [
        ({}, "prompt"),
        ({"prompt": "", "max_tokens": 1}, "prompt"),
        ({"prompt": "   ", "max_tokens": 1}, "prompt"),
        ({"prompt": 5, "max_tokens": 1}, "prompt"),
        ({"prompt": "x" * (MAX_PROMPT_CHARS + 1), "max_tokens": 1}, "exceeds"),
        ({"prompt": "x"}, "missing required field"),
        ({"prompt": "x", "max_tokens": "10"}, "integer"),
        ({"prompt": "x", "max_tokens": 1.5}, "integer"),
        ({"prompt": "x", "max_tokens": 0}, "between"),
        ({"prompt": "x", "max_tokens": 10**9}, "between"),
        ({"prompt": "x", "max_tokens": 1, "temperature": 3}, "temperature"),
        ({"prompt": "x", "max_tokens": 1, "temperature": "hot"}, "temperature"),
    ],
)
def test_invalid_payloads_raise_validation_error(payload: dict[str, object], fragment: str) -> None:
    with pytest.raises(ValidationError, match=fragment):
        validate_request(payload)


def test_bool_is_rejected_even_though_it_is_an_int_subclass() -> None:
    assert isinstance(True, int)  # the reason an explicit check is needed
    with pytest.raises(ValidationError, match="integer"):
        validate_request({"prompt": "x", "max_tokens": True})
    with pytest.raises(ValidationError, match="temperature"):
        validate_request({"prompt": "x", "max_tokens": 1, "temperature": True})


def test_validation_error_is_a_value_error() -> None:
    with pytest.raises(ValueError):
        validate_request({})


def test_exception_chaining_preserves_original_cause() -> None:
    with pytest.raises(ConfigError) as info:
        max_tokens_from_env({"MAX_TOKENS": "abc"})
    assert isinstance(info.value.__cause__, ValueError)
    assert "abc" in str(info.value)


def test_env_default_and_range_check() -> None:
    assert max_tokens_from_env({}) == 256
    assert max_tokens_from_env({"MAX_TOKENS": "64"}) == 64
    with pytest.raises(ConfigError, match="between"):
        max_tokens_from_env({"MAX_TOKENS": "0"})


def test_try_validate_handles_bad_input_but_not_programming_errors() -> None:
    request, error = try_validate({"prompt": "", "max_tokens": 1})
    assert request is None
    assert error is not None
    # Passing a non-mapping is a bug in the caller; it must NOT be swallowed as "bad input".
    with pytest.raises(AttributeError):
        try_validate(None)  # type: ignore[arg-type]
