# Model serving API: design notes (planned)

Everything below is design intent. None of it is built, and each point must be backed by a test before
it is described as a feature.

## Request lifecycle
Reuses project 01's states: `QUEUED → RUNNING → COMPLETED | CANCELLED`, extended at the API layer with
`FAILED` and `TIMED_OUT` (decision pending: these may belong in the scheduler instead).

## Open questions (to be answered with evidence, not opinion)
1. **Where does batching live?** In the scheduler (needs token budgets) or in a backend adapter?
   Decide after project 01 batching exists.
2. **Cancellation semantics.** Project 01 marks a running request cancelled but cannot stop the work.
   Streaming backends can check a cancel flag between tokens; define and test this.
3. **Backpressure.** Reject (429) at a queue limit vs. apply flow control to the client. Reject first;
   it is simpler to reason about and to test.
4. **Concurrency model.** `asyncio` with the backend in a thread pool vs a separate worker process.
   Needs measurements from the systems section.
5. **Streaming format.** Server-sent events vs newline-delimited JSON; check current FastAPI
   documentation when this stage starts, since APIs change.

## Non-goals
Authentication, multi-tenant billing, persistence, multi-node deployment. These belong to later
gateway work (section 07).
