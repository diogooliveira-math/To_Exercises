# Story 1.2: DB schema & checksum uniqueness

Status: ready-for-dev

## Story

As a maintainer, I want a DB model with a unique checksum index and exercise_checksum_history, so that imports are idempotent and file moves/renames are tracked.

## Acceptance Criteria

1. Given an initialized DB, when SQLModel metadata is created, then exercises table exists with a unique index on (checksum, checksum_algorithm) and exercise_checksum_history table exists.
2. Given a record exists and a new import references the same checksum but different file_path, when apply runs, then the existing record is updated and a history row appended.

## Tasks / Subtasks

- [x] Implement SQLModel models: Exercise, ExerciseChecksumHistory (AC: 1)
  - [x] Add unique index on (checksum, checksum_algorithm)
  - [x] Create migration to add exercise_checksum_history table
- [x] Implement DB upsert logic for apply (AC: 2)
  - [x] On checksum match and different file_path → update existing record and append history row
  - [x] Ensure transactional semantics and tests for rollback on error
- [x] Add tests and fixtures (in-memory SQLite) to validate schema and upsert behavior
  - [x] Unit tests for model definitions and index existence
  - [x] Integration test for apply flow that appends to history


## Dev Notes

- Relevant architecture patterns and constraints:
  - FastAPI + SQLModel
  - SQLite for dev (in-memory for tests)
  - Enable PRAGMA foreign_keys = ON in fixtures
  - Store JSON/metadata fields as TEXT for SQLite compatibility
- Source tree components to touch:
  - src/to_exercises/models.py (or src/to_exercises/db/models.py)
  - src/to_exercises/db/migrations/ (alembic or simple SQL scripts)
  - src/to_exercises/importer.py (apply upsert logic)
  - tests/fixtures.py (engine_in_memory, session)
  - tests/test_db_schema.py, tests/test_apply_upsert.py
- Testing standards summary:
  - Use pytest with in-memory SQLite fixtures
  - Aim for deterministic tests; do not rely on filesystem state

### Project Structure Notes

- Align new modules with existing src/to_exercises package layout
- Prefer SQLModel models colocated with other DB models
- Keep migration scripts in docs or migrations folder consistent with project conventions

### References

- Source: docs/epics.md#Story-1.2
- Source: docs/architecture.md (DB and testing sections)

## Dev Agent Record

### Context Reference

- Extracted from: docs/epics.md (Epic 1, Story 1.2)

### Agent Model Used

Amelia (dev agent)

### Debug Log References

- create-story executed by Amelia on: 2025-12-10

### Completion Notes List

- ✅ Ultimate context engine analysis completed - comprehensive developer guide created
- ✅ Implemented SQLModel models and composite unique index
- ✅ Implemented transactional upsert logic with history append
- ✅ Added unit and integration tests; all tests passing locally (11/11)

### File List

- src/to_exercises/models.py
- src/to_exercises/crud.py
- src/to_exercises/database.py
- src/to_exercises/db_migrations/0001_create_exercise_tables.sql
- tests/test_db_schema.py
- tests/test_apply_upsert.py
- tests/test_apply_upsert_transactional.py
- tests/test_api.py
- docs/sprint-artifacts/1-2-db-schema-checksum-uniqueness.md
- docs/sprint-artifacts/sprint-status.yaml













