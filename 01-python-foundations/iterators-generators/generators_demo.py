"""Iterators, generators and lazy evaluation.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


class Countdown:
    """An *iterator*: it is its own iterator and is exhausted after one pass."""

    def __init__(self, start: int) -> None:
        self._current = start

    def __iter__(self) -> Countdown:
        return self

    def __next__(self) -> int:
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


class CountdownIterable:
    """An *iterable*: every iter() call returns a fresh iterator, so it can be reused."""

    def __init__(self, start: int) -> None:
        self._start = start

    def __iter__(self) -> Iterator[int]:
        return Countdown(self._start)


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield lists of at most `size` items, consuming `items` lazily.

    Validation happens eagerly, at call time. If this function were itself a generator,
    a bad `size` would only raise on the first next(), far from the faulty call.
    """
    if size < 1:
        raise ValueError(f"size must be >= 1, got {size}")
    return _chunked(items, size)


def _chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    chunk: list[T] = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def read_lines(path: Path) -> Generator[str]:
    """Stream a file one line at a time. Memory use is independent of file size.

    The `with` block lives inside the generator, so the file is closed when the
    generator is exhausted, closed, or garbage-collected.
    """
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            yield line.rstrip("\n")


def take(items: Iterable[T], n: int) -> Iterator[T]:
    """Yield the first n items, then stop without consuming one more from `items`."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return
    for index, item in enumerate(items, start=1):
        yield item
        if index == n:
            return


def running_total(values: Iterable[float]) -> Iterator[float]:
    total = 0.0
    for value in values:
        total += value
        yield total


def non_blank(lines: Iterable[str]) -> Iterator[str]:
    return (line for line in lines if line.strip())
