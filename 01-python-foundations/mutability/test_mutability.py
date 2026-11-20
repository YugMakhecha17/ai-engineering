import copy

from mutability_demo import (
    append_in_place,
    buggy_collect,
    deep_copy,
    grid_aliased,
    grid_independent,
    safe_collect,
    shallow_copy,
    with_appended,
)


def test_alias_shares_identity_and_mutation_is_visible_through_both_names() -> None:
    a = [1, 2, 3]
    b = a
    append_in_place(b, 4)
    assert a is b
    assert a == [1, 2, 3, 4]


def test_equal_lists_are_not_the_same_object() -> None:
    a = [1, 2]
    b = [1, 2]
    assert a == b
    assert a is not b


def test_non_mutating_function_leaves_argument_unchanged() -> None:
    original = [1, 2]
    result = with_appended(original, 3)
    assert original == [1, 2]
    assert result == [1, 2, 3]
    assert result is not original


def test_shallow_copy_shares_nested_lists() -> None:
    original = [[1, 2], [3, 4]]
    copied = shallow_copy(original)
    assert copied is not original
    assert copied[0] is original[0]
    copied[0].append(99)
    assert original[0] == [1, 2, 99]  # the mutation leaked into the original


def test_deep_copy_isolates_nested_lists() -> None:
    original = [[1, 2], [3, 4]]
    copied = deep_copy(original)
    assert copied == original
    assert copied[0] is not original[0]
    copied[0].append(99)
    assert original[0] == [1, 2]


def test_mutable_default_argument_persists_across_calls() -> None:
    buggy_collect.__defaults__[0].clear()  # type: ignore[index]  # reset shared state
    assert buggy_collect("x") == ["x"]
    assert buggy_collect("y") == ["x", "y"]  # state leaked between unrelated calls


def test_none_sentinel_gives_each_call_a_fresh_list() -> None:
    assert safe_collect("x") == ["x"]
    assert safe_collect("y") == ["y"]


def test_multiplied_rows_are_one_object() -> None:
    grid = grid_aliased(3, 2)
    grid[0][0] = 1
    assert grid == [[1, 0], [1, 0], [1, 0]]
    assert grid[0] is grid[1] is grid[2]


def test_comprehension_rows_are_independent() -> None:
    grid = grid_independent(3, 2)
    grid[0][0] = 1
    assert grid == [[1, 0], [0, 0], [0, 0]]


def test_tuple_is_immutable_but_may_contain_mutable_objects() -> None:
    t = ([1], 2)
    t[0].append(5)
    assert t == ([1, 5], 2)


def test_augmented_assignment_mutates_list_but_rebinds_tuple() -> None:
    lst = [1]
    alias = lst
    lst += [2]  # list.__iadd__ extends in place
    assert alias == [1, 2]

    tup: tuple[int, ...] = (1,)
    tup_alias = tup
    tup += (2,)  # tuples have no in-place add: a new tuple is bound to `tup`
    assert tup_alias == (1,)
    assert tup == (1, 2)


def test_deepcopy_preserves_shared_references_within_the_copy() -> None:
    shared = [1]
    original = [shared, shared]
    copied = copy.deepcopy(original)
    assert copied[0] is copied[1]  # internal sharing is preserved (memo dict)
    assert copied[0] is not shared
