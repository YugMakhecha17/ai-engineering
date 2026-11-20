"""Request and lifecycle-state models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any


class RequestState(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    @property
    def is_terminal(self) -> bool:
        return self in (RequestState.COMPLETED, RequestState.CANCELLED)


# The complete lifecycle. Anything not listed here is rejected.
ALLOWED_TRANSITIONS: dict[RequestState, frozenset[RequestState]] = {
    RequestState.QUEUED: frozenset({RequestState.RUNNING, RequestState.CANCELLED}),
    RequestState.RUNNING: frozenset({RequestState.COMPLETED, RequestState.CANCELLED}),
    RequestState.COMPLETED: frozenset(),
    RequestState.CANCELLED: frozenset(),
}


@dataclass(frozen=True)
class Request:
    """An immutable description of work. Lifecycle state is tracked by the scheduler.

    `priority`: lower numbers are served first (0 is more urgent than 5).
    `sequence`: strictly increasing arrival number; the tie-breaker that makes ordering stable.
    `metadata`: a read-only, deep-copied snapshot, so later changes to the caller's dict
    cannot alter a queued request.
    """

    request_id: str
    payload: str
    priority: int
    submitted_at: float
    sequence: int
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}), compare=False)
