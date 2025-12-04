---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - docs/analysis/prd-To_Exercises-2025-12-03.md
  - docs/analysis/product-brief-To_Exercises-2025-12-03.md
  - docs/analysis/session-summary-2025-12-03.md
  - docs/analysis/brainstorming-session-2025-12-02.md
workflowType: 'architecture'
lastStep: 8
project_name: 'To_Exercises'
user_name: 'Diogo'
date: '2025-12-03T00:00:00Z'
status: 'complete'
completedAt: '2025-12-03T00:00:00Z'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Initialization Summary

- Created from template: bmm/workflows/3-solutioning/architecture/architecture-decision-template.md
- stepsCompleted: [1]
- Input documents discovered and loaded: 4 files

## Documents Loaded

- docs/analysis/prd-To_Exercises-2025-12-03.md
- docs/analysis/product-brief-To_Exercises-2025-12-03.md
- docs/analysis/session-summary-2025-12-03.md
- docs/analysis/brainstorming-session-2025-12-02.md

## Notes

These artifacts include the PRD, product brief, session summaries, and brainstorming outputs which will guide architectural decisions. The PRD is present, so we can proceed with architecture work when you confirm.

## Project Context Analysis

### Requirements Overview

Functional Requirements:
- Core CRUD API for Exercise records with query/filter endpoints (tag, difficulty_min, module).
- Idempotent importer with dry‑run anomaly reporting.
- Checksum uniqueness enforced at DB-level and tested.
- Minimal generator CLI that calls the API and produces LaTeX → PDF.
- Automated test suite covering importer and core CRUD flows.

Non-Functional Requirements:
- Maintainability for single-author development; prioritize simplicity and automation.
- Testability and deterministic tests (prefer in-memory SQLite for CI).
- Data integrity and idempotency across importer + DB constraints.
- Minimal operational assumptions (local stack, TeX toolchain required for generation).

Scale & Complexity:
- Primary domain: backend API + file-based content generation.
- Complexity level: low→medium for MVP.
- Estimated components: Domain model, Persistence, API, Importer, Generator, Tests, CI/docs.

Technical Constraints & Dependencies:
- Python, FastAPI, SQLModel, SQLite for dev.
- LaTeX toolchain required for PDF generation.
- Tests and local runs may need PYTHONPATH or package install to resolve imports.
- No project_context.md found (provide path if one exists).

Cross-Cutting Concerns:
- Checksum-based duplicate detection and importer idempotency.
- Parent/child/variant modeling for exercises and file-based canonical keys.
- Test isolation and reproducibility.
- Error reporting, logging and developer ergonomics (simple CLI/commands).

## First Principles Analysis

### Core Truths
- Primary purpose: preserve and make retrievable canonical exercise content (authoritative source = local files + indexed metadata).
- Single-author constraint: solution must be simple, automatable, and low-maintenance.
- Idempotency requirement: importing existing artifacts must be safe to re-run without creating duplicates.
- Developer ergonomics: tests must be deterministic and easy to run locally (avoid heavy infra).
- Generation is a consumer of the canonical data (generator should not own canonical data).

### Stripped Assumptions
- Assumption A: The DB must store LaTeX blobs. → Not necessary for MVP; store file paths and metadata in DB, keep LaTeX on disk.
- Assumption B: Use persistent on-disk SQLite in tests. → Prefer in-memory SQLite for tests to ensure determinism; persist on-disk for local dev.
- Assumption C: Complex generator templates required immediately. → Start with minimal template; iterate after stable data model + importer.

### Immediate Architectural Implications
- Canonical model: DB stores metadata and stable keys (id, checksum, file_path, parent_exercise_id, tags, difficulty). File system remains source of truth for raw LaTeX files.
- Uniqueness strategy: primary duplicate detection by checksum (unique index) + file_path history mapping to handle moves/renames.
- Importer design: dry-run mode that collects a structured report (JSON) and an apply mode that uses transactional DB writes; apply only after operator review.
- API contract: minimal CRUD + query endpoints; API is thin wrapper over domain logic (validation, checksum-based conflict handling).
- Tests & dev UX: pytest fixtures that initialize an in-memory SQLite engine; a reproducible test harness to run importer dry-run against sample fixture data.
- Generator: minimal CLI that calls the API, composes LaTeX template, and invokes local TeX build. Keep generator orthogonal to importer/DB.

### Recommended Minimal Architecture (MVP)
1. Data layer
   - SQLModel models for Exercise and related entities
   - Unique DB index on checksum (and composite index checksum+file_path for history)
2. Importer
   - Stage 0: dry-run → JSON report (anomalies, duplicates, missing parents)
   - Stage 1: apply → upsert semantics keyed by checksum
   - Transactional writes, idempotent by design
3. API
   - FastAPI endpoints: POST /exercises (create/upsert by checksum), GET /exercises/{id}, PUT /exercises/{id}, DELETE /exercises/{id}, GET /exercises?tag=&difficulty_min=&module=
   - Error responses for checksum collisions with explicit conflict payload
4. Generator
   - CLI that fetches a list of IDs from API, renders minimal LaTeX template, runs pdflatex/latexmk
5. Tests and CI
   - pytest with in-memory SQLite fixtures
   - CI (GitHub Actions) to run tests and optionally run a lightweight LaTeX build (if TeX available)
6. Dev ergonomics
   - Make the repo importable as a package (fix PYTHONPATH issues) so tests and imports resolve reliably
   - Provide a README command: run tests, run importer dry-run, run API, run generator

### Trade-offs and mitigations
- Simplicity vs scale: filesystem + SQLite is simplest; if data grows or multi-user needed, migrate to Postgres later. Mitigation: design schema with portability (avoid SQLite-only types).
- Checksum-only uniqueness may break if file format changes without content change; mitigate by storing checksum algorithm version, file path, and history of checksums.
- Local LaTeX dependency: generator requires TeX toolchain; in CI use a conditional step or a minimal container image.

### Prioritized next actions (concrete)
1. Fix package layout/import resolution so src/to_exercises is importable in tests (small developer friction fix).
2. Add DB model with checksum unique index and tests verifying uniqueness behavior.
3. Implement importer dry-run (JSON report) and run against ExerciseDatabase sample.
4. Scaffold FastAPI endpoints and basic CRUD tests.
5. Implement minimal generator CLI that uses the API and a tiny LaTeX template.
6. Add CI job to run pytest; optionally add LaTeX build step.

## Starter Template Implementation Checklist (refined)

The following concrete refinements fix importability, testing determinism, and provide actionable starter snippets.

1) Project layout and packaging (fix imports)
- Use standard src/ layout and make the project installable editable:
  - repo root:
    - pyproject.toml
    - README.md
    - src/to_exercises/__init__.py
    - src/to_exercises/main.py
    - src/to_exercises/models.py
    - src/to_exercises/database.py
    - src/to_exercises/crud.py
    - src/to_exercises/importer.py
    - src/to_exercises/generator.py
    - tests/
- Rationale: installing the package (pip install -e .) makes imports like to_exercises.main resolve reliably in tests and linters.

2) Minimal pyproject (setuptools) example

```toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "to_exercises"
version = "0.0.0"
description = "To_Exercises service"
authors = [{name = "Diogo"}]
dependencies = [
  "fastapi",
  "uvicorn[standard]",
  "sqlmodel",
  "typer",
]
optional-dependencies = { dev = ["pytest", "httpx", "pytest-asyncio"] }
```

Action: add pyproject.toml and run pip install -e . in dev environment.

3) Import style
- Use absolute imports inside package, e.g.:

```py
from to_exercises.database import get_engine
from to_exercises.models import Exercise
```

- Ensure src/to_exercises/__init__.py exists (even if empty).

4) Testing pattern: in-memory SQLite fixture (pytest)

```py
# tests/conftest.py
import pytest
from sqlmodel import SQLModel, create_engine, Session

@pytest.fixture
def engine_in_memory():
    e = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(e)
    yield e
    SQLModel.metadata.drop_all(e)

@pytest.fixture
def session(engine_in_memory):
    with Session(engine_in_memory) as s:
        yield s
```

- Override FastAPI dependency that provides DB session in tests to use this fixture (TestClient dependency override).

5) CLI choice: Typer (recommended)

```py
# src/to_exercises/importer.py
import typer
app = typer.Typer()

@app.command()
def dry_run(path: str):
    """Run importer dry-run and produce JSON report"""
    # implement scanning and reporting

if __name__ == "__main__":
    app()
```

6) Importer dry-run JSON structure (example)

```json
{
  "files_scanned": 123,
  "anomalies": [
    {"file": "path/to.tex", "issue": "missing metadata", "details": {}},
    {"file": "path/dup.tex", "issue": "checksum_duplicate", "checksum": "abc123", "existing": 45}
  ],
  "stats": {"duplicates": 3, "missing_parents": 2}
}
```

7) CI (GitHub Actions) minimal outline

- Workflow steps:
  - actions/checkout@v4
  - actions/setup-python@v4 (python-version)
  - pip install -e .[dev]
  - pytest
  - Optional LaTeX step: run only when RUN_LATEX=true (avoids failures in runners without TeX)

8) Dev quickstart (explicit commands)

Windows:
- python -m venv .venv
- .venv\Scripts\activate

Unix:
- python -m venv .venv
- source .venv/bin/activate

Then:
- pip install -e .
- pip install -r requirements-dev.txt  # if using
- pytest
- uvicorn to_exercises.main:app --reload
- python -m to_exercises.importer --dry-run path/to/ExerciseDatabase
- python -m to_exercises.generator --ids 1 2 3

9) Minimal Git hygiene & linters (optional)
- Add pre-commit with black/isort/ruff (recommended for consistency)

10) Small policy decisions to include in the architecture doc
- Tests must run against in-memory DB by default (CI/dev fixture).
- Importer dry-run is read-only by default and writes only on explicit apply flag.
- Generator CLI must call API (not write directly to DB) to preserve single source-of-truth.

## Data Model Clarifications and Self-Consistency Resolutions

### Exercise schema (sketch)
- id: integer PK
- checksum: text (indexed)
- checksum_algorithm: text
- file_path: text
- parent_exercise_id: integer (nullable FK -> exercises.id)
- tags: JSON stored as TEXT in SQLite; exposed as List[str] in API
- metadata: JSON stored as TEXT in SQLite; exposed as dict in API
- created_at: datetime (UTC ISO 8601)
- updated_at: datetime (UTC ISO 8601)

Notes:
- In SQLite, use TEXT columns and store JSON-serialized strings to preserve cross-DB compatibility. Add helper serializer/deserializer in src/to_exercises/utils.py.
- Implement an exercise_checksum_history table:
  - id: integer
  - exercise_id: integer FK
  - checksum: text
  - file_path: text
  - recorded_at: datetime

### Storage and SQLite notes
- To avoid cross-DB type issues during tests, store arrays/dicts as JSON strings in TEXT columns and deserialize in application layer.
- Tests should set PRAGMA foreign_keys = ON when using SQLite to ensure FK behavior matches Postgres.

### Checksum & Upsert policy
- Primary key for deduplication: (checksum, checksum_algorithm).
- Upsert behavior (apply mode):
  - If checksum exists: update existing record's metadata/file_path and append a row to exercise_checksum_history.
  - If checksum exists but differs in critical fields implying a real duplicate: return 409 with conflict details; CLI may use --force to override and create a new record.
- Conflict response example (409):
```json
{ "error": "checksum_conflict", "message": "Exercise with same checksum exists", "conflict_id": 123 }
```

### Tags & query semantics
- Storage/response: tags are arrays (JSON).
- Query params: support repeated params (?tag=alg&tag=calc) and comma-separated single param for convenience; always normalize to List[str] server-side.

### List endpoint shape (standardized)
- List endpoints MUST return:
```json
{ "items": [...], "limit": 50, "offset": 0, "total": 123 }
```
- This is enforced via contract tests.

### Datetime handling
- All datetimes use ISO 8601 strings in UTC. Use Pydantic/SQLModel validators to enforce serialization.

### Importer dry-run vs apply (clarified)
- Dry-run: read-only; produce structured JSON report with anomalies & stats.
- Apply:
  - Runs in a transaction.
  - Uses upsert semantics keyed by checksum/checksum_algorithm.
  - Updates existing records and appends to checksum history when file_path changes.
  - Returns 409 with conflict payload when automatic merging is unsafe.

### Auth & test overrides
- Provide a TestClient fixture that overrides auth dependency to accept a pre-shared test token.
- DEV_ALLOW_NO_AUTH must be opt‑in and default to false.

### LaTeX file handling
- Store canonical file_path in DB and record path changes in exercise_checksum_history (append-only).
- Importer should detect moved files by checksum and update the DB record's file_path accordingly.

### Packaging & importability
- Prioritize adding pyproject.toml and src/ layout. Add developer quickstart to README with pip install -e . to fix current import errors.

### Tests & CI notes
- Ensure tests use in-memory SQLite with PRAGMA foreign_keys = ON; include a Postgres smoke test in CI as optional future step.

### Short ADR suggestion
- Create docs/adr/0001-checksum-policy.md capturing the checksum/upsert policy and history table. (Created.)

## API Decisions

Chosen pattern: REST + OpenAPI + API contract tests

Rationale:
- REST is simple and well-suited for CLI and generator interactions.
- FastAPI provides automatic OpenAPI schema generation from Pydantic/SQLModel models.
- Contract tests ensure server and clients (CLI/generator) remain in sync and prevent regressions.

API surface (core endpoints):
- POST /v1/exercises
- GET /v1/exercises/{id}
- PUT /v1/exercises/{id}
- DELETE /v1/exercises/{id}
- GET /v1/exercises?tag=&difficulty_min=&module=&limit=&offset=&checksum=

Filter semantics:
- tag: comma-separated list OR repeated param (e.g., ?tag=alg&tag=calc)
- difficulty_min: integer
- module: string
- checksum: exact match
- Pagination: limit (default 50, max 250), offset (default 0)

Error format (example):
```json
{ "error": "checksum_conflict", "message": "Exercise with same checksum exists", "conflict_id": 123 }
```

Contract testing approach:
- Use a schema-validation tool (Schemathesis or openapi-core) to validate endpoints against the generated OpenAPI spec.
- Include contract tests in pytest suite that assert conformant responses and behavior (e.g., duplicate creation yields 409 with the specified error payload).
- Run contract tests in CI as part of the pytest job.

Client integration:
- Generator and importer CLI will use httpx and Pydantic models for request/response handling.
- Optionally generate a typed client later from the OpenAPI spec.

Docs & developer UX:
- Expose OpenAPI UI at /docs and Redoc at /redoc in development.
- Add sample curl/httpie examples in README showing Authorization header usage and common flows (create, query, generate).

## Completion Summary

Architecture workflow complete. Key artifacts created and saved:

- docs/architecture.md (this file) — updated with completion frontmatter
- docs/adr/0001-checksum-policy.md — checksum & upsert ADR

Final state:
- Workflow: architecture — COMPLETE
- Steps completed: 1..8
- Document location: docs/architecture.md

Implementation guidance (next immediate steps):
1. Run pip install -e . in your dev environment to make src/ imports resolvable.
2. Implement exercise_checksum_history and update CRUD upsert behavior to append history rows.
3. Add TestClient fixtures that override DB dependency to use in-memory engine for deterministic tests.
4. Implement importer dry-run JSON report and add CLI with Typer.

Would you like me to (pick one):
- start implementing the code fixes now (I)
- run through the Generate Project Context workflow and create project_context.md (Y)
- finish here and handoff for manual implementation (N)

(End of file)
