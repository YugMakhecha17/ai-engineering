# Architecture Decision Records

Short records of decisions that shape the repository, so that "why is it like this?" has an
answer other than "it just is". Format: context, decision, consequences. Add a new numbered
file when a decision would be expensive to reverse or likely to be questioned.

| ADR | Decision | Status |
|-----|----------|--------|
| [0001](0001-evidence-rule.md) | Every important technical claim needs evidence | Accepted |
| [0002](0002-minimal-toolchain.md) | Stdlib-only runtime code; pytest, ruff, mypy for development | Accepted |
| [0003](0003-no-empty-directories.md) | Directories exist only when they contain evidence | Accepted |
| [0004](0004-provenance-and-honest-progress.md) | AI-assisted code is labelled and never raises a progress status | Accepted |
