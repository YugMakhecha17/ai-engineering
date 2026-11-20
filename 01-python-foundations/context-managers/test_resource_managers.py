import pytest
from resource_managers import (
    ManagedResource,
    ResourceClosedError,
    read_all,
    temporary_setting,
    timed,
)


def test_resource_is_open_inside_and_closed_after_the_block() -> None:
    res = ManagedResource("db")
    assert res.state == "created"
    with res as r:
        assert r is res
        assert res.state == "open"
        assert r.read() == "data from db"
    assert res.state == "closed"
    assert res.events == ["open:db", "close:db"]


def test_resource_is_closed_when_the_body_raises_and_the_error_propagates() -> None:
    res = ManagedResource("db")
    with pytest.raises(ZeroDivisionError), res:
        1 / 0  # noqa: B018
    assert res.state == "closed"
    assert res.events == ["open:db", "close:db"]


def test_using_a_closed_resource_fails_loudly() -> None:
    with ManagedResource("db") as res:
        pass
    with pytest.raises(ResourceClosedError):
        res.read()


def test_close_is_idempotent() -> None:
    res = ManagedResource("db")
    with res:
        pass
    res.close()
    res.close()
    assert res.events.count("close:db") == 1


def test_resources_cannot_be_reopened() -> None:
    res = ManagedResource("db")
    with res:
        pass
    with pytest.raises(RuntimeError, match="cannot open"), res:
        pass


def test_nested_with_closes_in_reverse_order() -> None:
    log: list[str] = []
    with ManagedResource("a", log), ManagedResource("b", log):
        pass
    assert log == ["open:a", "open:b", "close:b", "close:a"]


def test_exit_stack_closes_everything_opened_in_reverse_order() -> None:
    log: list[str] = []
    assert read_all(["a", "b", "c"], log) == ["data from a", "data from b", "data from c"]
    assert log == ["open:a", "open:b", "open:c", "close:c", "close:b", "close:a"]


def test_exit_stack_cleans_up_partial_acquisition_on_failure() -> None:
    log: list[str] = []
    with pytest.raises(RuntimeError, match="cannot open b"):
        read_all(["a", "b", "c"], log, fail_on="b")
    assert log == ["open:a", "close:a"]  # 'a' was opened, so 'a' was closed


def test_timed_records_duration_with_an_injected_clock() -> None:
    ticks = iter([10.0, 12.5])
    sink: dict[str, float] = {}
    with timed("step", sink, clock=lambda: next(ticks)):
        pass
    assert sink == {"step": 2.5}


def test_timed_records_duration_even_when_the_body_raises() -> None:
    ticks = iter([0.0, 1.0])
    sink: dict[str, float] = {}
    with pytest.raises(ValueError), timed("step", sink, clock=lambda: next(ticks)):
        raise ValueError("boom")
    assert sink == {"step": 1.0}


def test_temporary_setting_restores_existing_and_removes_new_keys() -> None:
    config = {"debug": False}
    with temporary_setting(config, "debug", True), temporary_setting(config, "mode", "fast"):
        assert config == {"debug": True, "mode": "fast"}
    assert config == {"debug": False}


def test_temporary_setting_restores_state_after_an_exception() -> None:
    config = {"debug": False}
    with pytest.raises(RuntimeError), temporary_setting(config, "debug", True):
        raise RuntimeError("fail")
    assert config == {"debug": False}
