# 05 · Backend and distributed systems

**Status: one worked example implemented** (`WHERE` vs `GROUP BY`/`HAVING`, in
[databases-postgresql](databases-postgresql/)). Everything else below is **planned**; no code exists
for it yet ([ADR 0003](../docs/decisions/0003-no-empty-directories.md)).

## Prerequisites
Section [04](../04-systems-fundamentals/) (HTTP, concurrency, async) and section 03 (testing, typing).

## Topic map

| Topic | Question to answer with evidence | First planned implementation |
|-------|----------------------------------|------------------------------|
| api-design | REST fundamentals, error contracts | Project 02 API stage (FastAPI + Pydantic) |
| databases-postgresql | Relational modelling; filtering, grouping, aggregation | **Done (worked example)**; exercises E-07 pending |
| transactions-consistency | ACID, isolation levels, anomalies | Two-session demonstration of a lost update and its prevention in PostgreSQL |
| caching | Hit rate vs staleness | LRU cache with tests and a hit-rate measurement |
| queues-stream-processing | Delivery semantics, idempotency | At-least-once consumer with idempotent handling and a duplicate-delivery test |
| docker-deployment | Reproducible deployment | Container for project 02; CI/CD pipeline |
| observability | Logs, metrics, traces | Structured request logs; metrics endpoint (links to project 03) |
| reliability | Timeouts, retries with exponential backoff, backpressure, fault tolerance | Retry helper tested against an injected failing dependency |

Cloud and Kubernetes fundamentals follow Docker; no paid cloud services are required.

## Exit evidence (roadmap phase 3)
Service runs in a container; failure-injection tests for timeouts and retries.

## References (primary)
* PostgreSQL documentation: <https://www.postgresql.org/docs/current/>
* FastAPI: <https://fastapi.tiangolo.com/>
* Docker: <https://docs.docker.com/> · Kubernetes: <https://kubernetes.io/docs/>
