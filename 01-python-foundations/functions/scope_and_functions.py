"""Functions, return values, scope and closures.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence


def normalize(values: Sequence[float]) -> list[float]:
    """Scale values to the range [0, 1]. Pure: no mutation, no hidden state.

    Raises ValueError for empty input. A constant sequence maps to all zeros
    because the range is zero and there is nothing to scale.
    """
    if not values:
        raise ValueError("cannot normalize an empty sequence")
    low, high = min(values), max(values)
    if low == high:
        return [0.0] * len(values)
    return [(v - low) / (high - low) for v in values]


def min_max(values: Sequence[int]) -> tuple[int, int]:
    """Return several values as one tuple; the caller unpacks it."""
    if not values:
        raise ValueError("min_max() requires at least one value")
    return min(values), max(values)


def first_even(values: Sequence[int]) -> int | None:
    """Falling off the end of a function returns None, so the type says so."""
    for v in values:
        if v % 2 == 0:
            return v
    return None


def make_counter(start: int = 0) -> Callable[[], int]:
    """A closure: `count` remembers `current` after make_counter has returned."""
    current = start

    def count() -> int:
        nonlocal current  # without this, `current += 1` would raise UnboundLocalError
        current += 1
        return current

    return count


def late_binding_callbacks() -> list[Callable[[], int]]:
    """BUG ON PURPOSE: closures capture the *variable* i, not its value at creation."""
    return [lambda: i for i in range(3)]


def bound_callbacks() -> list[Callable[[], int]]:
    """Fix: a default argument is evaluated immediately, freezing the current value."""
    callbacks: list[Callable[[], int]] = []
    for i in range(3):

        def callback(i: int = i) -> int:  # the default is evaluated now, freezing i
            return i

        callbacks.append(callback)
    return callbacks


def clamp(value: float, *, low: float = 0.0, high: float = 1.0) -> float:
    """Keyword-only parameters make call sites self-documenting: clamp(x, high=5)."""
    if low > high:
        raise ValueError(f"low ({low}) must not exceed high ({high})")
    return max(low, min(value, high))
