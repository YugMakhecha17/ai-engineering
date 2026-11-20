# ADR 0003: Directories exist only when they contain evidence

**Status:** Accepted. Deviates from the originally proposed tree.

**Context.** The proposed layout listed about forty topic directories across sections 04–07.
Git does not track empty directories, so each would need a placeholder file, and a tree full of
placeholders signals progress that has not happened.

**Decision.** Sections 01–03 and the three projects have topic directories because they contain
implementations and tests. Sections 04–07 have a single `README.md` each containing the topic map,
prerequisites, and the first planned implementation per topic. A topic directory is created in the
same commit as its first tested implementation. Project 02 and 03 contain only the directories
that hold something (`src/`, `tests/`, `docs/`).

**Consequences.** The directory layout is a record of what exists; the READMEs are a record of
what is planned. `docs/project-status.md` states which is which.
