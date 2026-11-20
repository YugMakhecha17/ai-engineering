"""FIFO and priority request schedulers sharing one lifecycle implementation.

Design
------
* ``_records`` (a dict) maps request ID -> (request, state): O(1) lookup by ID.
* Subclasses supply only the *ordering* structure: ``_push`` and ``_pop_id``.
* Cancellation uses **lazy deletion**: the request is marked CANCELLED in ``_records`` in
  O(1) and its stale entry stays in the queue until it surfaces at the front, where
  ``next_request`` discards it. Removing from the middle of a heap or deque would be O(n).
* Trade-off: stale entries occupy memory until popped (see ``physical_size``), and
  ``_records`` is never pruned (see README, "Known limitations").

Complexity (n = live queued requests; amortised figures count each stale entry once)
    submit          FIFO O(1)       Priority O(log n)
    next_request    FIFO O(1)*      Priority O(log n)*     (* amortised over cancellations)
    cancel          O(1)
    complete        O(1)
    get_state/get_request  O(1)
"""

from __future__ import annotations

import copy
import heapq
import itertools
import time
import uuid
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from .errors import (
    DuplicateRequestError,
    EmptyQueueError,
    InvalidRequestError,
    InvalidStateTransitionError,
    UnknownRequestError,
)
from .models import ALLOWED_TRANSITIONS, Request, RequestState


@dataclass
class _Record:
    request: Request
    state: RequestState


class Scheduler(ABC):
    def __init__(
        self,
        *,
        clock: Callable[[], float] = time.monotonic,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._clock = clock
        self._id_factory: Callable[[], str] = id_factory or (lambda: uuid.uuid4().hex)
        self._records: dict[str, _Record] = {}
        self._sequence = itertools.count()
        self._queued = 0

    # ------------------------------------------------------------ ordering hooks
    @abstractmethod
    def _push(self, request: Request) -> None:
        """Add the request to the ordering structure."""

    @abstractmethod
    def _pop_id(self) -> str | None:
        """Remove and return the ID that the policy says is next, or None if empty.

        May return IDs of requests that were cancelled while queued; the caller skips those.
        """

    @property
    @abstractmethod
    def physical_size(self) -> int:
        """Entries held by the ordering structure, including stale (cancelled) ones."""

    # ------------------------------------------------------------ public API
    def submit(
        self,
        payload: str,
        *,
        priority: int = 0,
        metadata: Mapping[str, Any] | None = None,
        request_id: str | None = None,
    ) -> Request:
        """Validate, record and enqueue a request. Raises InvalidRequestError or
        DuplicateRequestError; on any error the scheduler is left unchanged."""
        if not isinstance(payload, str) or not payload.strip():
            raise InvalidRequestError("payload must be a non-empty string")
        if isinstance(priority, bool) or not isinstance(priority, int):
            raise InvalidRequestError(f"priority must be an int, got {type(priority).__name__}")
        frozen_metadata = self._freeze_metadata(metadata)
        rid = request_id if request_id is not None else self._id_factory()
        if not isinstance(rid, str) or not rid:
            raise InvalidRequestError("request_id must be a non-empty string")
        if rid in self._records:
            raise DuplicateRequestError(f"request_id already exists: {rid!r}")

        request = Request(
            request_id=rid,
            payload=payload,
            priority=priority,
            submitted_at=self._clock(),
            sequence=next(self._sequence),
            metadata=frozen_metadata,
        )
        self._records[rid] = _Record(request, RequestState.QUEUED)
        self._push(request)
        self._queued += 1
        return request

    def next_request(self) -> Request:
        """Dispatch the next live request (QUEUED -> RUNNING). Raises EmptyQueueError."""
        while True:
            rid = self._pop_id()
            if rid is None:
                raise EmptyQueueError("no queued requests")
            record = self._records[rid]
            if record.state is RequestState.QUEUED:
                record.state = RequestState.RUNNING
                self._queued -= 1
                return record.request
            # Stale entry for a request cancelled while queued: discard and keep looking.

    def complete(self, request_id: str) -> None:
        """RUNNING -> COMPLETED."""
        self._transition(self._record(request_id), RequestState.COMPLETED)

    def cancel(self, request_id: str) -> None:
        """QUEUED or RUNNING -> CANCELLED. O(1): queued entries are removed lazily."""
        record = self._record(request_id)
        was_queued = record.state is RequestState.QUEUED
        self._transition(record, RequestState.CANCELLED)
        if was_queued:
            self._queued -= 1

    def get_state(self, request_id: str) -> RequestState:
        return self._record(request_id).state

    def get_request(self, request_id: str) -> Request:
        return self._record(request_id).request

    def __len__(self) -> int:
        """Number of requests waiting in the queue (excludes running and finished ones)."""
        return self._queued

    def __contains__(self, request_id: object) -> bool:
        return request_id in self._records

    # ------------------------------------------------------------ internals
    def _record(self, request_id: str) -> _Record:
        try:
            return self._records[request_id]
        except KeyError:
            raise UnknownRequestError(f"unknown request_id: {request_id!r}") from None

    @staticmethod
    def _transition(record: _Record, target: RequestState) -> None:
        if target not in ALLOWED_TRANSITIONS[record.state]:
            raise InvalidStateTransitionError(
                f"cannot move request {record.request.request_id!r} "
                f"from {record.state.value} to {target.value}"
            )
        record.state = target

    @staticmethod
    def _freeze_metadata(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
        if metadata is None:
            return MappingProxyType({})
        if not isinstance(metadata, Mapping):
            raise InvalidRequestError("metadata must be a mapping")
        if not all(isinstance(key, str) for key in metadata):
            raise InvalidRequestError("metadata keys must be strings")
        # deepcopy: a shallow copy would still share nested lists/dicts with the caller.
        return MappingProxyType(copy.deepcopy(dict(metadata)))


class FifoScheduler(Scheduler):
    """First-come, first-served. `priority` is recorded but does not affect order."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._queue: deque[str] = deque()

    def _push(self, request: Request) -> None:
        self._queue.append(request.request_id)

    def _pop_id(self) -> str | None:
        return self._queue.popleft() if self._queue else None

    @property
    def physical_size(self) -> int:
        return len(self._queue)


class PriorityScheduler(Scheduler):
    """Lowest priority number first; equal priorities are served in arrival order.

    Heap entries are (priority, sequence, id). `sequence` is unique and increasing, so two
    entries never compare equal on the first two fields: ties are broken by arrival order
    and the (possibly incomparable) third field is never consulted.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._heap: list[tuple[int, int, str]] = []

    def _push(self, request: Request) -> None:
        heapq.heappush(self._heap, (request.priority, request.sequence, request.request_id))

    def _pop_id(self) -> str | None:
        return heapq.heappop(self._heap)[2] if self._heap else None

    @property
    def physical_size(self) -> int:
        return len(self._heap)
