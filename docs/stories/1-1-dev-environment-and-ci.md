# Story 1.1 — Dev environment and CI setup

As a maintainer, I want a reproducible dev environment and CI that runs tests so that development is deterministic and onboarding is trivial.

Acceptance Criteria (BDD):
- Given a new checkout, when I follow the README quickstart, then I can create a virtualenv, install dev dependencies, run the test suite, and run the app locally.
- Given a committed change, when CI runs on the branch, then pytest executes and returns non-zero on failing tests.
- Given the CI pipeline, when run on push to main, then the pipeline completes the test job and reports pass/fail status to the PR.

Technical Implementation Notes:
- Provide precise quickstart commands in README: venv creation, activation, install, db init command, run command.
- Add GitHub Actions workflow: job installs deps, runs pytest, optional LaTeX sample build gated by RUN_LATEX env var.
- Provide a Dockerfile for development that installs deps and exposes uvicorn; optional docker-compose for local stacks.
- Ensure tests use in-memory SQLite fixture (see tests/conftest.py).

Test Checklist:
- [ ] README quickstart commands validated on a clean machine
- [ ] GitHub Actions workflow added at .github/workflows/ci.yml and validated on a branch
- [ ] Dockerfile builds and runs the app in dev mode
- [ ] pytest runs and passes on CI

Definition of Done:
- All acceptance criteria met
- CI pipeline passing on main for tests
- PR demonstrating these changes merged into main

Prerequisites: None (foundation task)

Saved: docs/stories/1-1-dev-environment-and-ci.md
