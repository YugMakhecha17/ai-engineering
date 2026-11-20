# Git workflows

Status: documented practice, applied in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## 1. Problem
History should explain *why* the code is the way it is, and a mistake should be cheap to undo.

## 2. First-principles explanation
A commit is an immutable snapshot with a parent pointer; a branch is a movable label on a commit.
Small, single-purpose commits make history readable, bisectable and revertable.

## 3. Technical details: practice used here
* Branch per change (`feature/...`, `fix/...`); `main` always passes CI.
* Commit message: imperative summary ≤ 72 characters, blank line, then *why*. Example:
  `Add lazy cancellation to schedulers` / body explaining the O(1) cancel trade-off.
* Commit rhythm for new behaviour: failing test, passing code, refactor; separate commits where practical.
* A claim and its evidence land in the **same** commit (the register row, the test, the code).
* Never commit secrets, caches, model weights or data ([.gitignore](../../.gitignore)).
* Review checklist: [engineering-principles](../engineering-principles/README.md#code-review-checklist).

Useful commands: `git status`, `git diff --staged`, `git log --oneline --graph`, `git switch -c name`,
`git restore --staged file`, `git bisect` (find the commit that introduced a bug), `git revert <sha>`
(undo safely on shared branches).

## 4–6. Implementation, behaviour, tests
Not executable. CI enforces the mechanical parts (lint, types, tests, evidence register).

## 7. Engineering trade-offs
Squash-merge gives a tidy `main` but loses the red-green rhythm; merge commits keep it. Rebase keeps a
linear history but rewrites commits; never rebase shared branches.

## 8. AI-infrastructure connection
Reproducibility of models and experiments depends on versioning code, configuration and data together
(section 06, planned).

## 9. Common mistakes
Large mixed commits; "fix" messages with no reason; force-pushing shared branches; committing
generated files.

## 10. References
* Pro Git book: <https://git-scm.com/book>
* Git documentation: <https://git-scm.com/docs>
