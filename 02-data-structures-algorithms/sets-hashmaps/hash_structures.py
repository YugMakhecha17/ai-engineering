"""Hash sets and hash maps: usage patterns and a from-scratch hash map.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Iterator, Sequence
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
T = TypeVar("T", bound=Hashable)


def has_duplicates(items: Iterable[T]) -> bool:
    """O(n) expected time using a set; stops at the first repeat."""
    seen: set[T] = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False


def duplicates(items: Iterable[T]) -> list[T]:
    """Each repeated value once, ordered by the position of its second occurrence."""
    seen: set[T] = set()
    reported: set[T] = set()
    result: list[T] = []
    for item in items:
        if item in seen and item not in reported:
            reported.add(item)
            result.append(item)
        seen.add(item)
    return result


def find_by_id_linear(records: Sequence[tuple[str, str]], request_id: str) -> str | None:
    """O(n) per lookup: scans the sequence. Fine for a handful of records, poor beyond that."""
    for rid, value in records:
        if rid == request_id:
            return value
    return None


def index_by_id(records: Iterable[tuple[str, str]]) -> dict[str, str]:
    """Pay O(n) once to build the index; every later lookup is O(1) expected."""
    return dict(records)


class ChainedHashMap(Generic[K, V]):
    """Hash map with separate chaining, load-factor-driven resizing and collision stats.

    Illustrates how `dict` achieves expected O(1) lookups. CPython's dict uses open
    addressing and a compact layout instead; the trade-offs differ but the principle
    (hash -> bucket -> equality check) is the same.
    """

    MAX_LOAD_FACTOR = 0.75

    def __init__(self, initial_buckets: int = 8) -> None:
        if initial_buckets < 1:
            raise ValueError("initial_buckets must be >= 1")
        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(initial_buckets)]
        self._size = 0
        self.resizes = 0

    def __len__(self) -> int:
        return self._size

    @property
    def load_factor(self) -> float:
        return self._size / len(self._buckets)

    @property
    def longest_chain(self) -> int:
        return max(len(b) for b in self._buckets)

    def _bucket(self, key: K) -> list[tuple[K, V]]:
        return self._buckets[hash(key) % len(self._buckets)]  # TypeError for unhashable keys

    def put(self, key: K, value: V) -> None:
        bucket = self._bucket(key)
        for i, (existing, _) in enumerate(bucket):
            if existing == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self.load_factor > self.MAX_LOAD_FACTOR:
            self._resize()

    def get(self, key: K, default: V | None = None) -> V | None:
        for existing, value in self._bucket(key):
            if existing == key:
                return value
        return default

    def __contains__(self, key: K) -> bool:
        return any(existing == key for existing, _ in self._bucket(key))

    def delete(self, key: K) -> None:
        bucket = self._bucket(key)
        for i, (existing, _) in enumerate(bucket):
            if existing == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def items(self) -> Iterator[tuple[K, V]]:
        for bucket in self._buckets:
            yield from bucket

    def _resize(self) -> None:
        old_items = list(self.items())
        self._buckets = [[] for _ in range(len(self._buckets) * 2)]
        self.resizes += 1
        for key, value in old_items:
            self._bucket(key).append((key, value))  # rehash: bucket index depends on table size
