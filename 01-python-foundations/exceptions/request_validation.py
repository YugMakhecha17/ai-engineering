"""Exception handling and input validation for an inference-request payload.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

MAX_PROMPT_CHARS = 10_000
MAX_TOKENS_LIMIT = 4096


class ValidationError(ValueError):
    """The payload is malformed. Subclasses ValueError so generic handlers still work."""


class ConfigError(Exception):
    """Configuration is unusable. Distinct from ValidationError: the caller's input is fine."""


@dataclass(frozen=True)
class InferenceRequest:
    prompt: str
    max_tokens: int
    temperature: float


def _require_int(raw: Mapping[str, Any], key: str, low: int, high: int) -> int:
    if key not in raw:
        raise ValidationError(f"missing required field: {key!r}")
    value = raw[key]
    # bool is a subclass of int in Python: True would otherwise pass as max_tokens=1.
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{key} must be an integer, got {type(value).__name__}")
    if not low <= value <= high:
        raise ValidationError(f"{key} must be between {low} and {high}, got {value}")
    return value


def validate_request(raw: Mapping[str, Any]) -> InferenceRequest:
    """Validate untrusted input at the boundary and return a typed, trusted object.

    Fails fast with the first problem found. Everything downstream can then assume
    the invariants hold and does not need to re-check them.
    """
    prompt = raw.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValidationError("prompt must be a non-empty string")
    if len(prompt) > MAX_PROMPT_CHARS:
        raise ValidationError(f"prompt exceeds {MAX_PROMPT_CHARS} characters")

    max_tokens = _require_int(raw, "max_tokens", 1, MAX_TOKENS_LIMIT)

    temperature = raw.get("temperature", 1.0)
    if isinstance(temperature, bool) or not isinstance(temperature, int | float):
        raise ValidationError("temperature must be a number")
    if not 0.0 <= temperature <= 2.0:
        raise ValidationError(f"temperature must be between 0 and 2, got {temperature}")

    return InferenceRequest(prompt=prompt, max_tokens=max_tokens, temperature=float(temperature))


def max_tokens_from_env(env: Mapping[str, str], default: int = 256) -> int:
    """Translate a low-level error into a domain error, preserving the original cause."""
    raw = env.get("MAX_TOKENS")
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigError(f"MAX_TOKENS must be an integer, got {raw!r}") from exc
    if not 1 <= value <= MAX_TOKENS_LIMIT:
        raise ConfigError(f"MAX_TOKENS must be between 1 and {MAX_TOKENS_LIMIT}, got {value}")
    return value


def try_validate(raw: Mapping[str, Any]) -> tuple[InferenceRequest | None, str | None]:
    """Catch only the exception you can handle. A TypeError here would be a bug, not bad input."""
    try:
        return validate_request(raw), None
    except ValidationError as exc:
        return None, str(exc)
