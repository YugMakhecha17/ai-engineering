"""Three FIFO queue implementations behind one interface.

* ListQueue        - the naive version: list.pop(0), O(n) per dequeue.
* DequeQueue       - collections.deque: O(1) at both ends.
* RingBufferQueue  - a circular buffer: the idea inside deque-like structures, built by hand.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections import deque
from typing import Generic, Protocol, TypeVar

T = TypeVar("T")


class QueueEmptyError(Exception):
    """Dequeue or peek on an empty queue."""


class FifoQueue(Protocol[T]):
    def enqueue(self, item: T) -> None: ...
    def dequeue(self) -> T: ...
    def __len__(self) -> int: ...


class ListQueue(Generic[T]):
    """pop(0) shifts every remaining element one slot left: O(n) per dequeue."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if not self._items:
            raise QueueEmptyError("dequeue from empty queue")
        return self._items.pop(0)

    def __len__(self) -> int:
        return len(self._items)


class DequeQueue(Generic[T]):
    """deque is a doubly-linked list of fixed-size blocks: O(1) append and popleft."""

    def __init__(self) -> None:
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if not self._items:
            raise QueueEmptyError("dequeue from empty queue")
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)


class RingBufferQueue(Generic[T]):
    """Circular buffer: `head` chases `tail` around a fixed array, wrapping with modulo.

    Enqueue and dequeue are O(1) (enqueue is amortised O(1) because the buffer
    doubles when full). No element is ever shifted.
    """

    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        self._buffer: list[T | None] = [None] * initial_capacity
        self._head = 0
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._buffer)

    def __len__(self) -> int:
        return self._size

    def enqueue(self, item: T) -> None:
        if self._size == self.capacity:
            self._grow()
        tail = (self._head + self._size) % self.capacity
        self._buffer[tail] = item
        self._size += 1

    def dequeue(self) -> T:
        if self._size == 0:
            raise QueueEmptyError("dequeue from empty queue")
        item = self._buffer[self._head]
        self._buffer[self._head] = None  # release the reference
        self._head = (self._head + 1) % self.capacity
        self._size -= 1
        return item  # type: ignore[return-value]

    def peek(self) -> T:
        if self._size == 0:
            raise QueueEmptyError("peek on empty queue")
        return self._buffer[self._head]  # type: ignore[return-value]

    def _grow(self) -> None:
        # Unwrap into logical order: the old head may sit in the middle of the array.
        new_buffer: list[T | None] = [None] * (self.capacity * 2)
        for i in range(self._size):
            new_buffer[i] = self._buffer[(self._head + i) % self.capacity]
        self._buffer = new_buffer
        self._head = 0
