"""Input validation at the API boundary."""

from typing import Any

import pytest
from request_scheduler import FifoScheduler, InvalidRequestError, PriorityScheduler, Scheduler

BOTH = pytest.mark.parametrize("scheduler_cls", [FifoScheduler, PriorityScheduler])


@BOTH
@pytest.mark.parametrize("payload", ["", "   ", "\n\t"])
def test_blank_payloads_are_rejected(scheduler_cls: type[Scheduler], payload: str) -> None:
    with pytest.raises(InvalidRequestError, match="payload"):
        scheduler_cls().submit(payload)


@BOTH
@pytest.mark.parametrize("payload", [None, 5, b"bytes", ["list"]])
def test_non_string_payloads_are_rejected(scheduler_cls: type[Scheduler], payload: Any) -> None:
    with pytest.raises(InvalidRequestError, match="payload"):
        scheduler_cls().submit(payload)


@BOTH
@pytest.mark.parametrize("priority", [1.5, "1", None, True, False])
def test_priority_must_be_a_real_int_not_bool_or_float(
    scheduler_cls: type[Scheduler], priority: Any
) -> None:
    with pytest.raises(InvalidRequestError, match="priority"):
        scheduler_cls().submit("w", priority=priority)


@BOTH
@pytest.mark.parametrize("metadata", ["text", [("a", 1)], 5])
def test_metadata_must_be_a_mapping(scheduler_cls: type[Scheduler], metadata: Any) -> None:
    with pytest.raises(InvalidRequestError, match="mapping"):
        scheduler_cls().submit("w", metadata=metadata)


@BOTH
def test_metadata_keys_must_be_strings(scheduler_cls: type[Scheduler]) -> None:
    bad: Any = {1: "x"}
    with pytest.raises(InvalidRequestError, match="keys"):
        scheduler_cls().submit("w", metadata=bad)


@BOTH
@pytest.mark.parametrize("request_id", ["", 123])
def test_explicit_request_ids_are_validated(
    scheduler_cls: type[Scheduler], request_id: Any
) -> None:
    with pytest.raises(InvalidRequestError, match="request_id"):
        scheduler_cls().submit("w", request_id=request_id)


def test_invalid_request_error_is_a_value_error() -> None:
    with pytest.raises(ValueError):
        FifoScheduler().submit("")
