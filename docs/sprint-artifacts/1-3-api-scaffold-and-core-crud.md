---
story_key: 1-3-api-scaffold-and-core-crud
story_id: 1.3
status: done
owner: Diogo
sprint: 1
---

# Story 1.3: API scaffold and core CRUD

Status: done

## Story

As a developer, I want core FastAPI endpoints for exercises (CRUD + list with filters), so that CLI and generator can interact via a stable contract.

## Acceptance Criteria

1. Given the running app, when calling POST/GET/PUT/DELETE endpoints, then responses follow the documented shape and status codes (including 409 for checksum_conflict).
2. Given queries with tag/difficulty_min/module, when list endpoint called, then response includes items, limit, offset, total shape.

## Tasks / Subtasks

- [x] Task 1 (AC: 1.1 packaging prerequisite)
  - [x] Add package layout: create src/to_exercises/__init__.py and module skeleton (models, database, crud, api, importer, generator).
  - [x] Add pyproject.toml with minimal dependencies (fastapi, uvicorn, sqlmodel, typer); ensure editable install works.
  - [x] Document Windows/Unix quickstart in README (pip install -e ., run tests, start API).

- [x] Task 2 (AC: DB schema & checksum uniqueness)
  - [x] Implement SQLModel models: Exercise, ExerciseChecksumHistory.
  - [x] Add unique index on (checksum, checksum_algorithm) and ensure PRAGMA foreign_keys = ON for SQLite tests.
  - [x] Write migration notes / Alembic stub (if used) or create metadata creation helper for tests.
  - [x] Add unit tests verifying unique index and upsert-by-checksum behavior (in-memory SQLite).

- [x] Task 3 (AC: API endpoints and shapes)
  - [x] Scaffold FastAPI app and router: POST /v1/exercises, GET /v1/exercises/{id}, PUT, DELETE, GET /v1/exercises (filters tag,difficulty_min,module,limit,offset).
  - [x] Implement checksum_conflict handling: return 409 payload {"error":"checksum_conflict","message":"Exercise with same checksum exists","conflict_id":<int>}.
  - [x] Add request/response Pydantic/SQLModel schemas that produce OpenAPI automatically.
  - [x] Add contract tests asserting response shapes and 409 behavior.

- [x] Task 4 (AC: tests & CI)
  - [x] Add pytest fixtures: engine_in_memory, session (create/drop metadata) and TestClient dependency overrides.
  - [x] Add tests for list endpoint shape (items, limit, offset, total) and filtering semantics.
  - [x] Add GitHub Actions job: install editable package, run pytest; guard optional LaTeX steps with RUN_LATEX flag.

- [x] Task 5 (AC: docs & developer UX)
  - [x] Update README dev quickstart with explicit commands to run tests and start API locally.
  - [x] Add sample curl/httpie examples for core endpoints in README.
  - [x] Update File List in story with all changed/created files after implementation.

## Dev Notes

- Implementation guardrails (source: docs/architecture.md, docs/prd.md):
  - Stack: Python, FastAPI, SQLModel. Use in-memory SQLite for tests. Production-ready DB is out of scope for this story.
  - Ensure imports resolve via src/ layout and pip install -e . in dev environment (see architecture.md recommended actions).
  - Checksum policy: dedupe by (checksum, checksum_algorithm). On file_path changes append to exercise_checksum_history.
  - Testing: PRAGMA foreign_keys = ON in SQLite fixtures. Use JSON stored as TEXT for tags/metadata in SQLite.
  - API pagination/shape: { "items": [...], "limit": <int>, "offset": <int>, "total": <int> }.

### References

- PRD: docs/prd.md
- Architecture: docs/architecture.md
- Epics/story seeds: docs/epics.md

## Dev Agent Record

### Context Reference
- Sources used: docs/epics.md, docs/prd.md, docs/architecture.md, config: bmm/config.yaml

### Agent Model Used
- Amelia (dev agent) — dev workflow automated (YOLO mode)

### Debug Log References
- create-story workflow: bmm/workflows/4-implementation/create-story/workflow.yaml
- create-story instructions: bmm/workflows/4-implementation/create-story/instructions.xml

### Completion Notes List
- [ ] Tasks created. Implementation to follow via dev-story.

### File List
- src/to_exercises/models.py
- src/to_exercises/database.py
- src/to_exercises/crud.py
- src/to_exercises/api/v1/exercises.py
- src/to_exercises/main.py
- tests/test_api.py
- tests/conftest.py

### Change Log
- Created story 1-3-api-scaffold-and-core-crud.md and marked ready-for-dev in sprint-status.yaml (automated by create-story YOLO run).

---

Saved: automated create-story (YOLO) — comprehensive developer-focused story created.
