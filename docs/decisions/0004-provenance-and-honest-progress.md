# ADR 0004: AI-assisted code is labelled and never raises a progress status

**Status:** Accepted

**Context.** The repository doubles as a portfolio, and the owner's coding proficiency is still
being developed. Reference implementations in this repository were written with AI assistance.
Presenting them as independently demonstrated skill would be misleading to readers and
counter-productive to learning.

**Decision.**

1. Every AI-assisted source file carries a `Provenance:` line in its module docstring.
2. `docs/progress-tracker.md` records *independent* work separately from reference
   implementations. A reference implementation never changes a concept's status.
3. A concept becomes **Independently implemented** only after the owner submits their own code
   (under `<topic>/exercises/`) and it is reviewed. **Mastered** additionally requires explaining,
   testing, modifying and applying the concept to an unfamiliar problem.
4. Owner-written code is added alongside the references, not over them, so the history shows the
   progression.

**Consequences.** The tracker will look modest at first. That is intended: every upgrade
afterwards is real.
