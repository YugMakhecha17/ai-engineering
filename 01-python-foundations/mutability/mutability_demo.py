"""Mutability, aliasing and copying: runnable demonstrations.

Provenance: reference implementation written with AI assistance. It does not count
as the repository owner's independent work (see docs/progress-tracker.md).
"""

from __future__ import annotations

import copy
from collections.abc import Sequence


def append_in_place(items: list[int], value: int) -> None:
    """Mutate the caller's list. The caller sees the change through every alias."""
    items.append(value)


def with_appended(items: Sequence[int], value: int) -> list[int]:
    """Return a new list and leave the argument untouched (no side effects)."""
    return [*items, value]


def shallow_copy(matrix: list[list[int]]) -> list[list[int]]:
    """Copy the outer list only. Inner lists are shared with the original."""
    return copy.copy(matrix)


def deep_copy(matrix: list[list[int]]) -> list[list[int]]:
    """Recursively copy every nested object. Nothing is shared with the original."""
    return copy.deepcopy(matrix)


def buggy_collect(item: str, bucket: list[str] = []) -> list[str]:  # noqa: B006
    """BUG ON PURPOSE: the default list is created once, at function definition time."""
    bucket.append(item)
    return bucket


def safe_collect(item: str, bucket: list[str] | None = None) -> list[str]:
    """Fix: use None as the sentinel and create a fresh list per call."""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def grid_aliased(rows: int, cols: int) -> list[list[int]]:
    """BUG ON PURPOSE: `[row] * rows` repeats a reference to ONE row object."""
    return [[0] * cols] * rows


def grid_independent(rows: int, cols: int) -> list[list[int]]:
    """Fix: build a distinct row object on every iteration."""
    return [[0] * cols for _ in range(rows)]


if __name__ == "__main__":
    a = [1, 2, 3]
    b = a
    append_in_place(b, 4)
    print(f"a={a} b={b} same object: {a is b}")
    print(f"buggy: {buggy_collect('x')} then {buggy_collect('y')}")
    print(f"safe:  {safe_collect('x')} then {safe_collect('y')}")
