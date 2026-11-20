import random
from collections.abc import Iterator

import pytest
from hash_structures import (
    ChainedHashMap,
    duplicates,
    find_by_id_linear,
    has_duplicates,
    index_by_id,
)


def test_has_duplicates_basic_cases() -> None:
    assert has_duplicates([1, 2, 3, 1])
    assert not has_duplicates([1, 2, 3])
    assert not has_duplicates([])


def test_has_duplicates_stops_early_on_infinite_input() -> None:
    def forever() -> Iterator[int]:
        yield 1
        yield 1
        while True:
            yield 2

    assert has_duplicates(forever())  # would hang if it materialised the input


def test_duplicates_reports_each_repeated_value_once_in_order() -> None:
    assert duplicates([1, 2, 1, 3, 2, 1, 1]) == [1, 2]


def test_unhashable_items_are_rejected_by_set_based_detection() -> None:
    with pytest.raises(TypeError, match="unhashable"):
        has_duplicates([[1], [1]])  # type: ignore[type-var]


def test_dict_index_and_linear_scan_agree() -> None:
    records = [(f"req-{i}", f"value-{i}") for i in range(100)]
    index = index_by_id(records)
    for rid in ("req-0", "req-57", "req-99", "missing"):
        assert index.get(rid) == find_by_id_linear(records, rid)


def test_chained_map_put_get_overwrite_delete() -> None:
    m: ChainedHashMap[str, int] = ChainedHashMap()
    m.put("a", 1)
    m.put("b", 2)
    m.put("a", 10)  # overwrite, not a duplicate entry
    assert len(m) == 2
    assert m.get("a") == 10
    assert m.get("zzz") is None
    assert m.get("zzz", 0) == 0
    assert "b" in m
    m.delete("b")
    assert "b" not in m
    assert len(m) == 1
    with pytest.raises(KeyError):
        m.delete("b")


def test_resizing_keeps_load_factor_bounded_and_preserves_all_entries() -> None:
    m: ChainedHashMap[int, int] = ChainedHashMap(initial_buckets=2)
    for i in range(1_000):
        m.put(i, i * i)
        assert m.load_factor <= ChainedHashMap.MAX_LOAD_FACTOR
    assert m.resizes > 0
    assert len(m) == 1_000
    assert all(m.get(i) == i * i for i in range(1_000))


class Collider:
    """Distinct keys with identical hashes: the worst case for a hash table."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return 42

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Collider) and other.name == self.name


def test_correct_under_total_collision_but_chains_degrade_to_linear() -> None:
    m: ChainedHashMap[Collider, int] = ChainedHashMap()
    for i in range(50):
        m.put(Collider(f"k{i}"), i)
    assert all(m.get(Collider(f"k{i}")) == i for i in range(50))
    assert m.longest_chain == 50  # every key landed in one bucket: lookups are O(n)


def test_equal_hash_and_equality_define_key_identity_like_dict() -> None:
    m: ChainedHashMap[object, str] = ChainedHashMap()
    m.put(1, "int")
    m.put(True, "bool")  # 1 == True and hash(1) == hash(True): the same key
    m.put(1.0, "float")
    assert len(m) == 1
    assert m.get(1) == "float"
    d: dict[object, str] = {}
    d[1] = "int"
    d[True] = "bool"
    d[1.0] = "float"
    assert len(d) == 1


def test_unhashable_key_raises_type_error() -> None:
    m: ChainedHashMap[object, int] = ChainedHashMap()
    with pytest.raises(TypeError, match="unhashable"):
        m.put([1, 2], 1)


def test_behaviour_matches_dict_under_random_operations() -> None:
    rng = random.Random(99)
    mine: ChainedHashMap[int, int] = ChainedHashMap(initial_buckets=1)
    reference: dict[int, int] = {}
    for step in range(5_000):
        key = rng.randint(0, 200)
        op = rng.choice(["put", "get", "delete"])
        if op == "put":
            mine.put(key, step)
            reference[key] = step
        elif op == "get":
            assert mine.get(key) == reference.get(key)
        elif key in reference:
            mine.delete(key)
            del reference[key]
        else:
            with pytest.raises(KeyError):
                mine.delete(key)
        assert len(mine) == len(reference)
    assert dict(mine.items()) == reference
