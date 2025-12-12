# Story 1.1: Project packaging & dev quickstart

Status: Ready for Review

## Story

As a developer, I want the repository to be installable (editable) and have a clear quickstart, so that tests and local runs resolve imports reliably and onboarding is simple.

## Acceptance Criteria

1. Given the repo root, when I run pip install -e . in a dev environment, then imports like to_exercises.* resolve without manual PYTHONPATH fixes.
2. Given a newcomer, when they follow the README quickstart, then they can run pytest and start the API locally using the documented commands.

## Tasks / Subtasks

- [x] Add src layout and __init__.py for package discovery
- [x] Update pyproject.toml to support editable install
- [x] Document Windows and Unix quickstart commands in README
- [x] Add CI job step to install editable package and run tests

### Review Follow-ups (AI)

- [x] [AI-Review][MEDIUM] README.md modified and quickstart validated; listed in File List [README.md]
- [x] [AI-Review][MEDIUM] docs/epics.md modified but not listed in Dev Agent Record → File List [docs/epics.md]
- [x] [AI-Review][MEDIUM] docs/bmm-workflow-status.yaml modified but not listed in Dev Agent Record → File List [docs/bmm-workflow-status.yaml]
- [x] [AI-Review][MEDIUM] Verify no database artifacts committed (test.db, dev.db); .gitignore updated and local files removed [./test.db, ./dev.db]
- [x] [AI-Review][LOW] Migrate FastAPI startup event to lifespan handler to address deprecation warning [src/to_exercises/main.py]
- [x] [AI-Review][LOW] Ensure CI workflow includes editable install and pytest run; created .github/workflows/ci.yml

## Dev Notes

- Ensure src/to_exercises/__init__.py exists
- Use pip install -e . in CI step before running pytest
- Windows-specific note: use PowerShell command variations or npm scripts if needed

### Project Structure Notes

- Use src/ layout; tests should import to_exercises.* directly
- Ensure packaging metadata (pyproject.toml) lists packages correctly

### References

- Source: pyproject.toml
- Source: README.md

## Dev Agent Record

### Context Reference

- docs/epics.md#Story-1.1

### Agent Model Used

- gpt-4o-mini (simulated)

### Completion Notes List

- Added src layout and package init: src/to_exercises/__init__.py
- Fixed pyproject.toml packaging configuration for editable install (setuptools package discovery)
- Wrote packaging unit tests: tests/test_packaging.py, tests/test_pyproject.py
- Added tests fixture and test DB overrides in tests/conftest.py
- Ensured DB models are imported so metadata creates tables for tests
- Ran full test suite; all tests pass locally after fixes
- ✅ Resolved review finding [MEDIUM]: docs/epics.md added to File List
- ✅ Resolved review finding [LOW]: migrated startup event to lifespan handler in src/to_exercises/main.py

### File List

- src/
- pyproject.toml
- README.md
- docs/epics.md
- docs/bmm-workflow-status.yaml
- tests/test_packaging.py
- tests/test_pyproject.py
- tests/test_readme_quickstart.py
- tests/conftest.py
- docs/sprint-artifacts/sprint-status.yaml (updated status)
- docs/bmm-workflow-status.yaml
