"""Searching and sorting with operation counts, so complexity can be measured exactly.

Provenance: reference implementation written with AI assistance (see docs/progress-tracker.md).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T", int, float, str)


@dataclass(frozen=True)
class SearchResult:
    index: int | None  # None when the target is absent
    probes: int  # number of elements examined


def linear_search(items: Sequence[T], target: T) -> SearchResult:
    """O(n): examines elements one by one. Works on unsorted data."""
    for i, value in enumerate(items):
        if value == target:
            return SearchResult(i, i + 1)
    return SearchResult(None, len(items))


def binary_search(sorted_items: Sequence[T], target: T) -> SearchResult:
    """O(log n): halves the candidate range per probe. Requires sorted input."""
    low, high = 0, len(sorted_items) - 1
    probes = 0
    while low <= high:
        mid = (low + high) // 2
        probes += 1
        value = sorted_items[mid]
        if value == target:
            return SearchResult(mid, probes)
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return SearchResult(None, probes)


def insertion_sort(items: Sequence[T]) -> tuple[list[T], int]:
    """O(n^2) worst case, O(n) on already-sorted input. Returns (sorted list, comparisons)."""
    result = list(items)
    comparisons = 0
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if result[j] > current:
                result[j + 1] = result[j]
                j -= 1
            else:
                break
        result[j + 1] = current
    return result, comparisons


def merge_sort(items: Sequence[T]) -> tuple[list[T], int]:
    """O(n log n) in every case, O(n) extra space. Returns (sorted list, comparisons)."""
    if len(items) <= 1:
        return list(items), 0
    mid = len(items) // 2
    left, left_cmp = merge_sort(items[:mid])
    right, right_cmp = merge_sort(items[mid:])
    merged: list[T] = []
    comparisons = left_cmp + right_cmp
    i = j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if right[j] < left[i]:  # strict: equal items keep left-first order => stable sort
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, comparisons
