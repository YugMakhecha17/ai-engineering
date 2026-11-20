import pytest
from duration_parser import parse_duration


# Step 1 (red -> green): the simplest behaviour.
def test_single_unit() -> None:
    assert parse_duration("90s") == 90.0


# Step 2: each unit, parametrised so that adding a case is one line.
@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        ("1s", 1.0),
        ("2m", 120.0),
        ("3h", 10800.0),
        ("250ms", 0.25),
        ("0s", 0.0),
        ("007s", 7.0),
    ],
)
def test_each_unit(text: str, seconds: float) -> None:
    assert parse_duration(text) == pytest.approx(seconds)


# Step 3: compound values, in any order.
@pytest.mark.parametrize(
    ("text", "seconds"),
    [("1h30m", 5400.0), ("1m30s", 90.0), ("1h1m1s", 3661.0), ("30m1h", 5400.0), ("1s500ms", 1.5)],
)
def test_compound_values(text: str, seconds: float) -> None:
    assert parse_duration(text) == pytest.approx(seconds)


# Step 4: the 'ms' vs 'm' + 's' ambiguity found while writing step 2.
def test_ms_is_milliseconds_not_minutes_plus_seconds() -> None:
    assert parse_duration("5ms") == pytest.approx(0.005)
    assert parse_duration("5m5s") == 305.0


# Step 5: failure cases are specified, not left to chance.
@pytest.mark.parametrize(
    "bad",
    ["", "s", "5", "5x", "-5s", "1.5h", " 5s", "5s ", "1h 30m", "5S", "h5", "5s5"],
)
def test_malformed_input_raises_value_error(bad: str) -> None:
    with pytest.raises(ValueError, match="invalid duration"):
        parse_duration(bad)


def test_repeated_unit_is_rejected_rather_than_silently_summed() -> None:
    with pytest.raises(ValueError, match="duplicate unit"):
        parse_duration("1m2m")


def test_non_string_input_is_a_type_error() -> None:
    with pytest.raises(TypeError):
        parse_duration(90)  # type: ignore[arg-type]
