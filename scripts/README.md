# Scripts

| Script | Purpose | Run |
|--------|---------|-----|
| [`check_evidence.py`](check_evidence.py) | Verifies [`docs/claims-register.md`](../docs/claims-register.md): every claim has evidence; cited files and symbols exist; `test:` pointers name real `test_*` functions. Exit code 1 on errors; weak (prose/reference-only) claims are listed as warnings | `python scripts/check_evidence.py` or `make evidence` |
| [`mutation_spot_check.py`](mutation_spot_check.py) | Applies 18 deliberate bugs, one at a time, to a temporary copy of the repository and confirms the tests fail each time ("killed"). A survivor means a test is weaker than it looks. Not part of CI (slow-ish) | `python scripts/mutation_spot_check.py` |

Tests for the scripts: [`test_check_evidence.py`](test_check_evidence.py).
