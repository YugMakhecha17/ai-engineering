# FIFO and priority scheduling

**Status: implemented** in project 01 (`FifoScheduler`, `PriorityScheduler`).

## FIFO

```mermaid
flowchart LR
    A["submit(a)"] --> Q["deque of ids: a, b, c"]
    B["submit(b)"] --> Q
    C["submit(c)"] --> Q
    Q -- "popleft()" --> N["next_request() returns a"]
```

## Priority with stable ties

Heap entries are `(priority, sequence, request_id)`. `sequence` increases with every submission,
so equal priorities compare by arrival order and the heap never has to compare IDs.

```mermaid
flowchart TD
    S["submit(payload, priority=p)"] --> K["entry = (p, sequence, id)"]
    K --> H[("min-heap ordered by (priority, sequence)")]
    N["next_request()"] --> P["heappop()"]
    H --> P
    P --> D{"state of id is QUEUED?"}
    D -- "yes" --> R["mark RUNNING, return request"]
    D -- "no: cancelled earlier" --> P
```

Example with lower number = more urgent:

| Submitted (in order) | Priority | Heap key | Dispatch order |
|----------------------|----------|----------|----------------|
| batch job            | 5        | (5, 0)   | 3rd |
| interactive A        | 0        | (0, 1)   | 1st |
| interactive B        | 0        | (0, 2)   | 2nd |
| background           | 9        | (9, 3)   | 4th |
