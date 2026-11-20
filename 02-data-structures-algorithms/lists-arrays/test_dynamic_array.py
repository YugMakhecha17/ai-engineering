import random

import pytest
from dynamic_array import DynamicArray


def test_append_and_index_including_negative_indices() -> None:
    arr: DynamicArray[int] = DynamicArray()
    for i in range(10):
        arr.append(i * 10)
    assert len(arr) == 10
    assert arr[0] == 0
    assert arr[9] == 90
    assert arr[-1] == 90
    assert arr[-10] == 0


def test_out_of_range_access_raises_index_error() -> None:
    arr: DynamicArray[int] = DynamicArray()
    arr.append(1)
    for bad in (1, -2, 100):
        with pytest.raises(IndexError):
            arr[bad]
    with pytest.raises(IndexError):
        arr[5] = 0


def test_capacity_grows_geometrically() -> None:
    arr: DynamicArray[int] = DynamicArray(initial_capacity=4)
    capacities = set()
    for i in range(100):
        arr.append(i)
        capacities.add(arr.capacity)
    assert capacities == {4, 8, 16, 32, 64, 128}


@pytest.mark.parametrize("n", [10, 1_000, 100_000])
def test_append_is_amortised_constant_total_copies_are_linear(n: int) -> None:
    arr: DynamicArray[int] = DynamicArray()
    for i in range(n):
        arr.append(i)
    # Doubling copies 4 + 8 + 16 + ... < 2n elements in total, so each append costs
    # O(1) amortised even though an individual append may copy O(n) elements.
    assert arr.element_copies < 2 * n


def test_insert_at_front_shifts_every_element_but_append_shifts_none() -> None:
    arr: DynamicArray[int] = DynamicArray()
    for i in range(100):
        arr.append(i)
    assert arr.element_shifts == 0
    arr.insert(0, -1)
    assert arr.element_shifts == 100  # O(n)
    assert arr[0] == -1
    assert arr[1] == 0


def test_pop_from_end_is_cheap_pop_from_front_is_linear() -> None:
    arr: DynamicArray[int] = DynamicArray()
    for i in range(50):
        arr.append(i)
    assert arr.pop() == 49
    assert arr.element_shifts == 0
    assert arr.pop(0) == 0
    assert arr.element_shifts == 48
    assert len(arr) == 48


def test_slot_is_cleared_after_pop_so_no_stale_reference_is_retained() -> None:
    arr: DynamicArray[object] = DynamicArray()
    arr.append(object())
    arr.pop()
    assert arr._buffer[0] is None


def test_behaviour_matches_python_list_under_random_operations() -> None:
    rng = random.Random(1234)
    mine: DynamicArray[int] = DynamicArray()
    reference: list[int] = []
    for step in range(2_000):
        op = rng.choice(["append", "insert", "pop", "set"])
        if op == "append" or not reference:
            mine.append(step)
            reference.append(step)
        elif op == "insert":
            index = rng.randint(0, len(reference))
            mine.insert(index, step)
            reference.insert(index, step)
        elif op == "pop":
            index = rng.randrange(len(reference))
            assert mine.pop(index) == reference.pop(index)
        else:
            index = rng.randrange(len(reference))
            mine[index] = step
            reference[index] = step
        assert len(mine) == len(reference)
    assert [mine[i] for i in range(len(mine))] == reference


def test_invalid_construction_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        DynamicArray(initial_capacity=0)
    with pytest.raises(ValueError, match="growth_factor"):
        DynamicArray(growth_factor=1)
