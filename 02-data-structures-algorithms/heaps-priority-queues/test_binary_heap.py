import math
import random

import pytest
from binary_heap import BinaryHeap, HeapEmptyError, StablePriorityQueue


def test_pops_come_out_in_sorted_order() -> None:
    rng = random.Random(1)
    values = [rng.randint(-1000, 1000) for _ in range(500)]
    heap: BinaryHeap[int] = BinaryHeap()
    for v in values:
        heap.push(v)
        assert heap.is_valid()
    assert [heap.pop() for _ in range(len(heap))] == sorted(values)


def test_construction_from_items_heapifies() -> None:
    values = [9, 4, 7, 1, 8, 2]
    heap = BinaryHeap(values)
    assert heap.is_valid()
    assert heap.peek() == 1
    assert [heap.pop() for _ in range(len(values))] == sorted(values)


def test_empty_heap_raises() -> None:
    heap: BinaryHeap[int] = BinaryHeap()
    with pytest.raises(HeapEmptyError):
        heap.pop()
    with pytest.raises(HeapEmptyError):
        heap.peek()


def test_single_element_and_duplicates() -> None:
    heap = BinaryHeap([5])
    assert heap.pop() == 5
    heap = BinaryHeap([2, 2, 2])
    assert [heap.pop() for _ in range(3)] == [2, 2, 2]


def test_invariant_holds_under_interleaved_push_and_pop() -> None:
    rng = random.Random(2)
    heap: BinaryHeap[int] = BinaryHeap()
    reference: list[int] = []
    for _ in range(2_000):
        if reference and rng.random() < 0.4:
            reference.sort()
            assert heap.pop() == reference.pop(0)
        else:
            v = rng.randint(0, 100)
            heap.push(v)
            reference.append(v)
        assert heap.is_valid()


@pytest.mark.parametrize("n", [16, 255, 1024, 5000])
def test_push_costs_at_most_log2_n_comparisons(n: int) -> None:
    rng = random.Random(3)
    heap: BinaryHeap[int] = BinaryHeap()
    for size in range(1, n + 1):
        before = heap.comparisons
        heap.push(rng.random())  # type: ignore[arg-type]
        assert heap.comparisons - before <= math.floor(math.log2(size))


@pytest.mark.parametrize("n", [16, 255, 1024, 5000])
def test_pop_costs_at_most_two_log2_n_comparisons(n: int) -> None:
    rng = random.Random(4)
    heap = BinaryHeap([rng.random() for _ in range(n)])
    while len(heap) > 1:
        before = heap.comparisons
        heap.pop()
        height = math.floor(math.log2(len(heap))) if len(heap) else 0
        assert heap.comparisons - before <= 2 * height


def test_heapify_is_linear_not_n_log_n() -> None:
    rng = random.Random(5)
    n = 100_000
    heap = BinaryHeap([rng.random() for _ in range(n)])
    assert heap.comparisons <= 2 * n  # n pushes would need ~n*log2(n) = 1.7 million


def test_heap_alone_is_not_stable_for_equal_priorities() -> None:
    items = [(1, "A"), (1, "B"), (1, "C"), (1, "D")]
    heap: BinaryHeap[tuple[int, str]] = BinaryHeap(key=lambda e: e[0])
    for item in items:
        heap.push(item)
    order = [heap.pop()[1] for _ in range(4)]
    assert order == ["A", "D", "C", "B"]  # equal keys, but NOT arrival order
    assert order != ["A", "B", "C", "D"]


def test_stable_priority_queue_keeps_arrival_order_within_a_priority() -> None:
    pq: StablePriorityQueue[str] = StablePriorityQueue()
    for label in "ABCD":
        pq.push(1, label)
    pq.push(0, "urgent")
    assert [pq.pop() for _ in range(len(pq))] == ["urgent", "A", "B", "C", "D"]


def test_stable_priority_queue_orders_by_priority_then_arrival() -> None:
    pq: StablePriorityQueue[str] = StablePriorityQueue()
    for priority, label in [(2, "c1"), (1, "b1"), (2, "c2"), (1, "b2"), (0, "a1"), (2, "c3")]:
        pq.push(priority, label)
    assert [pq.pop() for _ in range(6)] == ["a1", "b1", "b2", "c1", "c2", "c3"]
