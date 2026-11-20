# ML lifecycle and distributed inference

**Status: planned design intent.** Nothing here is implemented. These diagrams record the target
architecture so that earlier sections can be built toward it.

## Training and deployment lifecycle

```mermaid
flowchart LR
    Ingest["Data ingestion"] --> Validate["Data validation"]
    Validate --> Version["Versioned dataset"]
    Version --> Train["Training pipeline"]
    Train --> Track["Experiment tracking"]
    Track --> Registry["Model registry"]
    Registry --> Deploy["Deployment: canary, then full rollout"]
    Deploy --> Monitor["Monitoring: latency, errors, quality"]
    Monitor --> Drift{"Data or concept drift detected?"}
    Drift -- "yes" --> Ingest
    Drift -- "no" --> Monitor
```

## Distributed inference

```mermaid
flowchart TD
    Client["Clients"] --> GW["Model gateway: auth, rate limits, routing"]
    GW --> LB["Load balancer / autoscaler"]
    LB --> R1["Replica 1"]
    LB --> R2["Replica 2"]
    subgraph R1G["Replica: tensor-parallel group"]
        G0["GPU 0: shard of every layer"] <--> G1["GPU 1: shard of every layer"]
    end
    R1 --- R1G
    R2 --- R2G["Another tensor-parallel group"]
    R1G -. "pipeline parallelism: layer groups on separate nodes" .-> R1G
```

Open design questions to resolve with evidence before building: where batching lives (gateway or
replica), how KV-cache memory pressure feeds back into admission control, and how queue depth maps
to autoscaling signals.
