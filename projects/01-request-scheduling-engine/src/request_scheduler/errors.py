"""Exception hierarchy. Catch SchedulerError to handle any scheduler failure."""

from __future__ import annotations


class SchedulerError(Exception):
    """Base class for all errors raised by this package."""


class InvalidRequestError(SchedulerError, ValueError):
    """A submission argument is malformed. Also a ValueError for generic handlers."""


class DuplicateRequestError(SchedulerError):
    """A request ID is already known (including IDs of finished or cancelled requests)."""


class UnknownRequestError(SchedulerError):
    """No request with that ID has been submitted."""


class EmptyQueueError(SchedulerError):
    """next_request() was called but no request is waiting."""


class InvalidStateTransitionError(SchedulerError):
    """The requested lifecycle transition is not allowed from the current state."""
