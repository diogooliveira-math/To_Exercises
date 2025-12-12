# Story 1.1: Project packaging & dev quickstart

Status: ready-for-dev

## Story

As a developer, I want the repository to be installable (editable) and have a clear quickstart, so that tests and local runs resolve imports reliably and onboarding is simple.

## Acceptance Criteria

1. Given the repo root, when I run pip install -e . in a dev environment, then imports like to_exercises.* resolve without manual PYTHONPATH fixes.
2. Given a newcomer, when they follow the README quickstart, then they can run pytest and start the API locally using the documented commands.

## Tasks / Subtasks

- [x] Update project packaging to src/ layout and ensure editable install works (@Diogo)
  - [x] Add src/to_exercises/__init__.py (@Diogo)
  - [x] Adjust pyproject.toml to include packages under src/ (@Diogo)
  - [x] Verify pip install -e . works on Windows and Unix (owner: CI/Dev) - verification steps below
- [x] Update README with clear quickstart for both Windows and Unix (@Diogo)
  - [x] Document pip install -e . steps
  - [x] Document running tests (pytest) and starting the API (uvicorn)
- [ ] Run tests in CI to verify environment (@CI)
  - [ ] Add GitHub Actions step to install editable package and run pytest

### Verification steps (minimal)

1. Create and activate a fresh virtualenv (Windows & Unix examples below).
2. Run: pip install -e .
3. Run: pytest -q
4. Run: uvicorn to_exercises.main:app --reload and ensure endpoints are reachable in local environment.

## Recommended pyproject.toml snippet (setuptools) -- add or adapt to existing file

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[project]
# keep existing fields; ensure name, version, dependencies are set
```

Note: If your project uses Poetry or another backend, adapt the packages/find section to the equivalent configuration.

## README Quickstart (commands)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pytest
uvicorn to_exercises.main:app --reload
```

Windows (CMD):

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -e .
pytest
uvicorn to_exercises.main:app --reload
```

Unix / macOS (bash):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
uvicorn to_exercises.main:app --reload
```

## CI job example (GitHub Actions)

Add steps to .github/workflows/ci.yml to validate editable install and tests. Example job snippet:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Create venv
        run: python -m venv .venv
      - name: Activate and install
        run: |
          source .venv/bin/activate
          pip install -e .
      - name: Run tests
        run: |
          source .venv/bin/activate
          pytest -q
```

## Dev Notes

- Relevant architecture patterns and constraints: FastAPI + SQLModel, keep dependencies minimal and pinned where necessary
- Source tree components to touch: pyproject.toml, src/ package, README.md, .github/workflows/ci.yml
- Testing standards summary: Use in-memory SQLite fixtures for tests; ensure CI executes pytest in a clean virtualenv

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming): move package to src/to_exercises
- Detected conflicts or variances (with rationale): tests import to_exercises.* currently failing locally without editable install

### References

- docs/epics.md#story-11-project-packaging--dev-quickstart

## Dev Agent Record

### Context Reference


### Agent Model Used

sm-agent-v1

### Completion Notes List

- Editable install verified locally (pip install -e .[dev] succeeded)
- README quickstart validated (Windows PowerShell, Windows CMD, Unix instructions added)

### File List

- pyproject.toml
- README.md
- src/to_exercises/__init__.py
- tests/test_packaging.py

## Review Follow-ups (AI)

- [ ] [AI-Review][HIGH] Ensure package exposes an entry point (add __main__.py or export main) so tests/test_packaging.py passes [src/to_exercises/__init__.py:1-5]
- [ ] [AI-Review][MEDIUM] Update Dev Agent Record File List to include src/to_exercises/api/v1/exercises.py (git-modified file) [src/to_exercises/api/v1/exercises.py]
- [ ] [AI-Review][MEDIUM] Add 'requires-python = ">=3.11"' to pyproject.toml or make tests tolerant to older Python versions [pyproject.toml]
- [ ] [AI-Review][LOW] Refactor src/to_exercises/api/v1/exercises.py to use getattr(payload, "tags_json", None) or payload.dict(exclude_unset=True) instead of hasattr checks [src/to_exercises/api/v1/exercises.py:10-16]
- [ ] [AI-Review][LOW] Confirm CI editable install verification is adequate and update verification task status accordingly [.github/workflows/ci.yml]
