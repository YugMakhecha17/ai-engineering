# Common development commands. On Windows without `make`, run the underlying
# commands directly: they are listed in CONTRIBUTING.md.

PYTHON ?= python
SOURCES := 01-python-foundations 02-data-structures-algorithms 03-software-engineering \
           05-backend-distributed-systems projects scripts benchmarks

.PHONY: help install test lint format typecheck evidence check clean

help:
	@echo "install    install dev dependencies (pytest, ruff, mypy)"
	@echo "test       run the test suite"
	@echo "lint       ruff lint + format check"
	@echo "format     apply ruff formatting and safe fixes"
	@echo "typecheck  run mypy (strict)"
	@echo "evidence   verify docs/claims-register.md against the repository"
	@echo "check      lint + typecheck + evidence + test (what CI runs)"

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

format:
	$(PYTHON) -m ruff check --fix .
	$(PYTHON) -m ruff format .

typecheck:
	$(PYTHON) -m mypy $(SOURCES)

evidence:
	$(PYTHON) scripts/check_evidence.py

check: lint typecheck evidence test

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for pat in ('.pytest_cache','.mypy_cache','.ruff_cache','**/__pycache__') for p in pathlib.Path('.').glob(pat)]"
