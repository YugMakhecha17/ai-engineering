# Model serving and inference request flow

**Status: planned design intent.** Only the `ModelBackend` boundary exists in code
(`projects/02-model-serving-api/src/model_serving/backend.py`) together with the scheduler from
project 01. The API, admission control, batching and streaming layers do not exist yet.

## Serving architecture

```mermaid
flowchart LR
    Client["Client"] --> API["HTTP API: validate, assign request id"]
    API --> Adm{"Admission control: queue full or rate limited?"}
    Adm -- "reject" --> Err["Structured error: 429 or 503"]
    Adm -- "accept" --> Sched["Scheduler (project 01)"]
    Sched --> Batch["Batcher"]
    Batch --> Backend["ModelBackend: simulated or real engine"]
    Backend --> Stream["Token stream"]
    Stream --> Client
    API -. "timings and counters" .-> Metrics["Metrics (project 03)"]
    Sched -. "queue wait" .-> Metrics
    Backend -. "TTFT, tokens per second" .-> Metrics
```

## Inference request flow: prefill then decode

An autoregressive model processes the whole prompt once (prefill), then generates one token per
step (decode), reusing cached attention keys and values (KV cache) from earlier steps.

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant S as Scheduler
    participant M as Model backend

    C->>A: POST generate (prompt, max_tokens)
    A->>S: submit(request)
    S->>M: dispatch
    M->>M: prefill (process prompt, fill KV cache)
    M-->>C: first token (time to first token)
    loop each decode step until stop or max_tokens
        M->>M: decode one token using KV cache
        M-->>C: next token (inter-token latency)
    end
    M->>S: complete(request)
```

References: Orca (iteration-level scheduling) and vLLM / PagedAttention (KV-cache memory
management); see [07-ai-infrastructure](../../../07-ai-infrastructure/README.md).
