# Resource lifecycle

**Status: implemented** in [`01-python-foundations/context-managers`](../../../01-python-foundations/context-managers/).

```mermaid
stateDiagram-v2
    [*] --> created
    created --> open: __enter__ / open()
    open --> closed: __exit__ / close()
    closed --> closed: close() again (idempotent)
    closed --> [*]
```

`__exit__` runs on normal exit and when the body raises; the exception then propagates.

```mermaid
flowchart TD
    E["with resource as r:"] --> A["__enter__: acquire"]
    A --> B["body runs"]
    B -- "no exception" --> X["__exit__(None, None, None): release"]
    B -- "exception" --> Y["__exit__(exc_type, exc, tb): release"]
    X --> Z["continue after the block"]
    Y --> W["exception propagates (unless __exit__ returns True)"]
```
