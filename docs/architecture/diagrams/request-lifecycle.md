# Request lifecycle

**Status: implemented** in [`projects/01-request-scheduling-engine`](../../../projects/01-request-scheduling-engine/).
Code: `ALLOWED_TRANSITIONS` in `models.py`. Tests: `test_scheduler_lifecycle.py`.

## States and transitions

```mermaid
stateDiagram-v2
    [*] --> QUEUED: submit()
    QUEUED --> RUNNING: next_request()
    QUEUED --> CANCELLED: cancel()
    RUNNING --> COMPLETED: complete()
    RUNNING --> CANCELLED: cancel()
    COMPLETED --> [*]
    CANCELLED --> [*]
```

Any transition not drawn raises `InvalidStateTransitionError`; terminal states are final.

## Dispatch with lazy deletion

`cancel()` marks the request in the records dict (O(1)) and leaves its queue entry in place.
`next_request()` discards such stale entries as they surface.

```mermaid
sequenceDiagram
    participant C as Caller
    participant S as Scheduler
    participant Q as Ordering structure
    participant R as Records dict

    C->>S: cancel(id)
    S->>R: state = CANCELLED
    Note over Q: stale entry stays in the queue
    C->>S: next_request()
    loop until a live entry is found
        S->>Q: pop next id
        Q-->>S: id
        S->>R: look up state
    end
    S->>R: state = RUNNING
    S-->>C: Request
```
