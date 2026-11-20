"""A binary min-heap with comparison counting, plus a stable priority queue built on it.

The comparison counter turns the claim "push and pop are O(log n)" into something a
test can assert exactly, independent of machine speed.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class HeapEmptyError(Exception):
    """pop or peek on an empty heap."""


class BinaryHeap(Generic[T]):
    """Array-backed min-heap. For index i: parent = (i-1)//2, children = 2i+1 and 2i+2.

    Invariant: every node's key is <= its children's keys. Only the root's position
    is guaranteed (it is the minimum); siblings are NOT ordered relative to each other.
    """

    def __init__(self, items: Iterable[T] = (), *, key: Callable[[T], Any] | None = None) -> None:
        self._key: Callable[[T], Any] = key if key is not None else (lambda x: x)
        self._data: list[T] = list(items)
        self.comparisons = 0
        self._heapify()  # Floyd's bottom-up construction: O(n)

    def __len__(self) -> int:
        return len(self._data)

    def _less(self, a: T, b: T) -> bool:
        self.comparisons += 1
        return bool(self._key(a) < self._key(b))

    def push(self, item: T) -> None:
        """O(log n): append at the end, then sift up while smaller than the parent."""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def peek(self) -> T:
        if not self._data:
            raise HeapEmptyError("peek on empty heap")
        return self._data[0]

    def pop(self) -> T:
        """O(log n): remove the root, move the last item to the root, sift it down."""
        if not self._data:
            raise HeapEmptyError("pop on empty heap")
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return root

    def _sift_up(self, index: int) -> None:
        item = self._data[index]
        while index > 0:
            parent = (index - 1) // 2
            if not self._less(item, self._data[parent]):
                break
            self._data[index] = self._data[parent]
            index = parent
        self._data[index] = item

    def _sift_down(self, index: int) -> None:
        size = len(self._data)
        item = self._data[index]
        while True:
            child = 2 * index + 1
            if child >= size:
                break
            right = child + 1
            if right < size and self._less(self._data[right], self._data[child]):
                child = right
            if not self._less(self._data[child], item):
                break
            self._data[index] = self._data[child]
            index = child
        self._data[index] = item

    def _heapify(self) -> None:
        for index in range(len(self._data) // 2 - 1, -1, -1):
            self._sift_down(index)

    def is_valid(self) -> bool:
        """Check the heap invariant without touching the comparison counter."""
        keys = [self._key(x) for x in self._data]
        return all(keys[(i - 1) // 2] <= keys[i] for i in range(1, len(keys)))


class StablePriorityQueue(Generic[T]):
    """Priority queue where equal priorities leave in insertion (FIFO) order.

    A heap alone is not stable. Appending a strictly increasing sequence number to the
    sort key makes every key unique, so ties are broken by arrival order. This is the
    same technique recommended in the heapq documentation and used in project 01.
    """

    def __init__(self) -> None:
        self._heap: BinaryHeap[tuple[int, int, T]] = BinaryHeap(key=lambda e: (e[0], e[1]))
        self._counter = 0

    def __len__(self) -> int:
        return len(self._heap)

    def push(self, priority: int, item: T) -> None:
        self._heap.push((priority, self._counter, item))
        self._counter += 1

    def pop(self) -> T:
        return self._heap.pop()[2]
