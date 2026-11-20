"""A dynamic array built on a fixed-capacity buffer, with instrumentation.

CPython's `list` is already a dynamic array. This module re-implements the idea so
that the cost model (amortised O(1) append, O(n) insert-at-front) can be *measured*
by counting element copies and shifts rather than just asserted.

Python has no raw fixed-size arrays; a pre-sized list is used purely as a stand-in
for a block of contiguous memory of fixed capacity.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class DynamicArray(Generic[T]):
    def __init__(self, initial_capacity: int = 4, growth_factor: int = 2) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        if growth_factor < 2:
            raise ValueError(
                "growth_factor must be >= 2 (geometric growth is what makes append O(1) amortised)"
            )
        self._buffer: list[T | None] = [None] * initial_capacity
        self._size = 0
        self._growth = growth_factor
        self.resizes = 0
        self.element_copies = 0  # elements copied while resizing
        self.element_shifts = 0  # elements moved by insert/pop at an arbitrary index

    @property
    def capacity(self) -> int:
        return len(self._buffer)

    def __len__(self) -> int:
        return self._size

    def _index(self, index: int) -> int:
        if not -self._size <= index < self._size:
            raise IndexError(f"index {index} out of range for size {self._size}")
        return index + self._size if index < 0 else index

    def __getitem__(self, index: int) -> T:
        value = self._buffer[self._index(index)]
        return value  # type: ignore[return-value]  # slots below _size always hold a T

    def __setitem__(self, index: int, value: T) -> None:
        self._buffer[self._index(index)] = value

    def _grow(self) -> None:
        new_buffer: list[T | None] = [None] * (self.capacity * self._growth)
        for i in range(self._size):
            new_buffer[i] = self._buffer[i]
        self.element_copies += self._size
        self.resizes += 1
        self._buffer = new_buffer

    def append(self, value: T) -> None:
        if self._size == self.capacity:
            self._grow()
        self._buffer[self._size] = value
        self._size += 1

    def insert(self, index: int, value: T) -> None:
        """Insert before `index`. Shifts every later element: O(n - index)."""
        if not 0 <= index <= self._size:
            raise IndexError(f"insert index {index} out of range for size {self._size}")
        if self._size == self.capacity:
            self._grow()
        for i in range(self._size, index, -1):
            self._buffer[i] = self._buffer[i - 1]
            self.element_shifts += 1
        self._buffer[index] = value
        self._size += 1

    def pop(self, index: int = -1) -> T:
        """Remove and return an element. O(1) at the end, O(n - index) elsewhere."""
        position = self._index(index)
        value = self._buffer[position]
        for i in range(position, self._size - 1):
            self._buffer[i] = self._buffer[i + 1]
            self.element_shifts += 1
        self._size -= 1
        self._buffer[self._size] = None  # drop the reference so the object can be collected
        return value  # type: ignore[return-value]
