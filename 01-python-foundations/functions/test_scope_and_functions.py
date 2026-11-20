import pytest
from scope_and_functions import (
    bound_callbacks,
    clamp,
    first_even,
    late_binding_callbacks,
    make_counter,
    min_max,
    normalize,
)


def test_normalize_scales_to_unit_range_without_mutating_input() -> None:
    data = [10.0, 20.0, 30.0]
    assert normalize(data) == [0.0, 0.5, 1.0]
    assert data == [10.0, 20.0, 30.0]


def test_normalize_constant_input_returns_zeros() -> None:
    assert normalize([5.0, 5.0]) == [0.0, 0.0]


def test_normalize_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="empty"):
        normalize([])


def test_multiple_return_values_are_one_tuple() -> None:
    result = min_max([3, 1, 2])
    assert isinstance(result, tuple)
    low, high = result
    assert (low, high) == (1, 3)


def test_function_without_matching_return_yields_none() -> None:
    assert first_even([1, 3, 5]) is None
    assert first_even([1, 4, 6]) == 4


def test_list_sort_returns_none_a_classic_mistake() -> None:
    data = [3, 1, 2]
    assert data.sort() is None  # sorted(data) returns the new list; .sort() mutates
    assert data == [1, 2, 3]


def test_closure_keeps_private_state_between_calls() -> None:
    counter_a = make_counter()
    counter_b = make_counter(start=10)
    assert [counter_a(), counter_a(), counter_a()] == [1, 2, 3]
    assert counter_b() == 11  # independent state per closure


def test_late_binding_closures_all_see_the_final_loop_value() -> None:
    assert [f() for f in late_binding_callbacks()] == [2, 2, 2]


def test_default_argument_binding_captures_each_value() -> None:
    assert [f() for f in bound_callbacks()] == [0, 1, 2]


def test_assigning_to_a_name_makes_it_local_for_the_whole_function() -> None:
    # Executed from a string so that static analysers do not reject the deliberate bug.
    source = "x = 1\ndef f():\n    print(x)\n    x = 2\n"
    namespace: dict[str, object] = {}
    exec(source, namespace)
    f = namespace["f"]
    assert callable(f)
    with pytest.raises(UnboundLocalError):
        f()


def test_keyword_only_arguments_cannot_be_passed_positionally() -> None:
    assert clamp(5, high=3) == 3
    with pytest.raises(TypeError):
        clamp(5, 0, 3)  # type: ignore[call-arg]


def test_clamp_rejects_inverted_bounds() -> None:
    with pytest.raises(ValueError, match="must not exceed"):
        clamp(1, low=2, high=1)
