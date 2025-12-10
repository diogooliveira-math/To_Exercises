---
stepsCompleted: [0,1,2,3,4]
inputDocuments:
  - docs/prd.md
  - docs/architecture.md
workflowType: 'epics'
lastStep: 4
project_name: 'To_Exercises'
user_name: 'Diogo'
date: '2025-12-05'
---

# Epics & Stories - To_Exercises (Working Draft)

## Context Validation

- PRD document: docs/prd.md — FOUND and loaded
- Architecture document: docs/architecture.md — FOUND and loaded
- UX Design: none found (optional)

Prerequisites satisfied: PRD and Architecture are present and complete. Proceeding to extract functional requirements and design epics.

## Functional Requirements Inventory (extracted from PRD)

FR1: Core CRUD API for Exercises — endpoints to create, read, update, delete, and list exercises with filters (tag, difficulty, module).

FR2: Idempotent Importer (dry-run + apply) — two-stage importer producing a JSON anomalies report in dry-run and transactional apply that upserts by checksum.

FR3: Checksum uniqueness & history — DB-level uniqueness on checksum and an exercise_checksum_history table to track moves/renames.

FR4: Generator CLI — selects exercises (by IDs or filters), composes LaTeX, and produces PDFs (preview mode available).

FR5: Deterministic Testability & In-memory SQLite fixtures — tests and CI rely on predictable in-memory DB runs.

FR6: Importer anomaly reporting & operator workflow — clear anomalies, conflict handling (409 with conflict_id), and apply only after review.

FR7: Metadata editing & preview — simple metadata editor or CLI preview to ensure content correctness before generation.

FR8: API contract & OpenAPI-driven contract tests — ensure endpoints conform to spec and contract tests run in CI.

FR9: Security & Auth for apply and generator endpoints — token-based auth for mutate/apply operations; dry-run may be looser in dev.

FR10: Generator idempotent output paths and configurable behavior (overwrite/versioning) — ensure reproducible outputs.

---

## Epics Summary

Epic 1 — Foundation & Developer Experience
Epic 2 — Idempotent Importer & Content Management
Epic 3 — Generator & Distribution Experience

---

## FR Coverage Map (high level)

- FR1 → Epic 1, Epic 2 (API surface) - Stories: 1.2, 2.3
- FR2 → Epic 2 - Stories: 2.1, 2.2
- FR3 → Epic 1, Epic 2 - Stories: 1.2, 2.3
- FR4 → Epic 3 - Stories: 3.1, 3.2
- FR5 → Epic 1 - Story: 1.4
- FR6 → Epic 2 - Story: 2.2
- FR7 → Epic 2 / Epic 3 - Story: 2.4, 3.1
- FR8 → Epic 1 / Epic 2 - Story: 1.4, 2.5
- FR9 → Epic 1 / Epic 2 - Story: 1.4, 2.2
- FR10 → Epic 3 - Story: 3.2

---

## Epic 1: Foundation & Developer Experience

User value statement:
- English: Provide a reliable, auditable foundation so a single maintainer can safely import, store, and evolve exercise data.
- Português: Oferecer uma fundação confiável e auditável para que um único mantenedor importe, armazene e evolua dados de exercícios com segurança.

PRD coverage: Core persistence model, checksum uniqueness, importer idempotency, test-first developer UX.

Technical context: FastAPI + SQLModel, SQLite for dev (in-memory for tests), exercise_checksum_history table, unique index on checksum. Packaging fix: src/ layout + pip install -e . to make imports reliable.

Dependencies: None (first epic).

Stories:

### Story 1.1: Project packaging & dev quickstart
As a developer, I want the repository to be installable (editable) and have a clear quickstart, so that tests and local runs resolve imports reliably and onboarding is simple.

Acceptance Criteria:
- Given the repo root, when I run pip install -e . in a dev environment, then imports like to_exercises.* resolve without manual PYTHONPATH fixes.
- Given a newcomer, when they follow the README quickstart, then they can run pytest and start the API locally using the documented commands.

Technical Notes:
- Add src/to_exercises/__init__.py and adjust pyproject toml / setup to support editable install
- Document Windows and Unix quickstart commands in README

Prerequisites: repository access

---

### Story 1.2: DB schema & checksum uniqueness
As a maintainer, I want a DB model with a unique checksum index and exercise_checksum_history, so that imports are idempotent and file moves/renames are tracked.

Acceptance Criteria:
- Given an initialized DB, when SQLModel metadata is created, then exercises table exists with a unique index on (checksum, checksum_algorithm) and exercise_checksum_history table exists.
- Given a record exists and a new import references the same checksum but different file_path, when apply runs, then the existing record is updated and a history row appended.

Technical Notes:
- Use SQLModel models for Exercise and ExerciseChecksumHistory
- For SQLite tests, store JSON fields as TEXT and enable PRAGMA foreign_keys = ON in fixtures

Prerequisites: Story 1.1 or editable install

---

### Story 1.3: API scaffold and core CRUD
As a developer, I want core FastAPI endpoints for exercises (CRUD + list with filters), so that CLI and generator can interact via a stable contract.

Acceptance Criteria:
- Given the running app, when calling POST/GET/PUT/DELETE endpoints, then responses follow the documented shape and status codes (including 409 for checksum_conflict).
- Given queries with tag/difficulty_min/module, when list endpoint called, then response includes items, limit, offset, total shape.

Technical Notes:
- Implement endpoints: POST /v1/exercises, GET /v1/exercises/{id}, PUT, DELETE, GET list
- Return 409 checksum_conflict payload when appropriate

Prerequisites: Story 1.2

---

### Story 1.4: Testing fixtures, CI and contract test baseline
As a maintainer, I want deterministic in-memory SQLite fixtures and a CI job to run tests and contract checks, so that behaviour is reliable and regressions are caught.

Acceptance Criteria:
- Given the test suite, when run in CI and locally, then tests use an in-memory engine fixture and pass consistently (no environment-specific path hacks required).
- Given an OpenAPI spec, when contract tests run, then endpoints conform to the spec used by generator/importer tests.

Technical Notes:
- Add pytest fixtures (engine_in_memory, session) as described in architecture.md
- Add GitHub Actions job: install editable package and run pytest; conditional LaTeX step behind a flag

Prerequisites: Story 1.1, Story 1.3

---

## Epic 2: Idempotent Importer & Content Management

User value statement:
- English: Let content authors import their exercise files confidently with a dry‑run that surfaces duplicates and anomalies, then apply safely.

PRD coverage: Importer dry-run, anomaly reporting, idempotent apply semantics, checksum conflict handling.

Technical context: Two-stage importer (dry-run JSON report; apply transactional upsert by checksum). Use Typer for CLI; importer writes structured JSON for dry-run and uses DB transactions for apply. Conflict handling returns 409 with conflict_id.

Dependencies: Builds on Epic 1 (DB & API).

Stories:

### Story 2.1: Importer dry-run JSON report
As an operator, I want a read-only dry-run that scans sources and produces a structured JSON anomalies report, so that I can review changes before applying.

Acceptance Criteria:
- Given a folder of exercise files, when dry-run is executed, then a JSON report is produced listing files_scanned, anomalies array (missing metadata, checksum_duplicate, etc.) and stats.
- Given detected duplicates, when dry-run completes, then duplicates include file paths and checksum values.

Technical Notes:
- Implement CLI command: to_exercises.importer dry-run --path PATH -> writes JSON to stdout/file
- JSON schema follows architecture.md example

Prerequisites: Story 1.1, Story 1.2

---

### Story 2.2: Importer apply with transactional upsert and conflict handling
As an operator, I want an apply mode that performs transactional upserts keyed by checksum and returns a clear conflict payload on unsafe collisions, so that data integrity is preserved.

Acceptance Criteria:
- Given a dry-run reviewed by the operator, when apply is executed, then DB writes occur in a transaction and either commit fully or rollback on error.
- Given a checksum collision that cannot be safely merged, when apply runs without --force, then the API/CLI returns 409 with a conflict_id and no DB mutation occurs.

Technical Notes:
- Implement apply CLI and POST /v1/import/apply endpoint that accepts apply payload; use DB transaction semantics
- Conflict payload: {"error":"checksum_conflict","message":"Exercise with same checksum exists","conflict_id":123}

Prerequisites: Story 1.2, Story 2.1

---

### Story 2.3: Upsert behavior and checksum history maintenance
As a maintainer, I want apply operations to append to exercise_checksum_history when a record is updated due to moved/renamed files, so that provenance is preserved.

Acceptance Criteria:
- Given an existing exercise with checksum X and file_path A, when apply updates its file_path to B (same checksum), then a row is appended to exercise_checksum_history recording the previous file_path and timestamp.

Technical Notes:
- Append-only history table with recorded_at timestamp; ensure migrations create the table

Prerequisites: Story 1.2

---

### Story 2.4: Metadata editor / preview CLI
As a content author, I want a simple CLI command to preview metadata and edit minimal fields before apply, so that I can fix missing metadata and re-run dry-run/apply.

Acceptance Criteria:
- Given a file with missing metadata, when preview CLI is run, then the tool displays missing fields and allows a small edit flow that outputs a corrected file or patch suggestion.

Technical Notes:
- Fast path: CLI prompts or outputs JSON patch to be applied manually; keep UI minimal

Prerequisites: Story 2.1

---

### Story 2.5: API contract & integration for importer
As an engineer integrating the importer with the API, I want API endpoints and OpenAPI spec coverage for import-related actions, so that generator/clients can rely on stable contracts.

Acceptance Criteria:
- Given the OpenAPI spec generated from FastAPI, when contract tests run, then import-related endpoints conform to the expected shapes and error payloads.

Technical Notes:
- Expose endpoints used by CLI where appropriate; add contract tests referencing generated OpenAPI

Prerequisites: Story 1.3, Story 1.4

---

## Epic 3: Generator & Distribution Experience

User value statement:
- English: Allow instructors and authors to assemble exercise sets and produce consistent, idempotent PDFs via the API and generator CLI.

PRD coverage: Generator CLI, LaTeX template, selection/filter API endpoints, idempotent output handling.

Technical context: Generator is a CLI that queries the API (httpx) for exercise payloads, composes a minimal LaTeX template, and invokes local TeX (if available) to produce PDFs. Preview mode renders a LaTeX snippet or minimal HTML and does not write PDFs.

Dependencies: Requires Epic 1 + Epic 2 (data model + importer).

Stories (detailed):

### Story 3.1: Generator preview and select-by-filters
As an instructor, I want to preview a LaTeX snippet for a selected set of exercises (by IDs or filters), so that I can confirm formatting before producing PDFs.

Acceptance Criteria:
- Given selected IDs or filter params, when generator CLI is run with --preview, then a LaTeX snippet or minimal HTML rendering is produced and no PDF file is written.
- Given preview output, when user inspects it, then content matches canonical data from API (checksums/ids present) and includes a short metadata header per exercise (id, checksum, title/tags).
- Given network or API errors, when preview command runs, then the CLI returns a non-zero exit code with a clear structured error message and no partial files produced.

Technical Notes:
- Implement CLI: `to_exercises.generator preview --ids 1 2 3` and `to_exercises.generator preview --filter tag=alg --limit 50`
- Use `httpx` with retries and sensible timeouts to call GET `/v1/exercises` (support pagination).
- Produce two preview output formats: raw LaTeX snippet (default) and `--format html` for quick visual inspection.
- Include checksum and id annotations in preview to allow traceability.
- Ensure preview mode performs no writes by default; optional `--out` writes a snippet file only if explicitly provided.

Prerequisites: Story 1.3, Story 2.1

---

### Story 3.2: Idempotent PDF generation and output handling
As an instructor, I want generated PDFs to be idempotent and configurable (overwrite or versioning), so that repeated runs do not cause accidental duplication.

Acceptance Criteria:
- Given a generation run with specified output path, when run multiple times with same inputs and default mode, then output either overwrites deterministically or writes a deterministic versioned filename when `--version` is used.
- Given `--version` mode, when generation completes, then filename includes a stable checksum-derived suffix so identical inputs map to identical filenames across runs.
- Given no TeX toolchain available, when generation is requested, then the CLI fails gracefully with a clear structured error and a non-zero exit code; if `--preview` was used previously, CLI suggests the preview command as fallback.
- Given concurrent runs writing to the same output path, when lock-enabled mode is active (`--lock`), then only one run proceeds and others exit with a clear message or retry per `--retry` policy.

Technical Notes:
- Default behavior: overwrite output file. `--version` produces filename like `<base>-<sha256(IDs+options)>.pdf`.
- Detect TeX availability (e.g., `which pdflatex` or `pdflatex --version`) and fail with helpful message if missing.
- Use atomic file write pattern: write to temp file then move/replace to final path to avoid partial files.
- Optional file lock via `filelock` library for `--lock` behavior; expose `--retry N --retry-delay S` for retries.
- Provide verbose `--dry-run` mode that shows planned filenames without invoking TeX.

Prerequisites: Story 1.3, Story 2.1

---

### Story 3.3: Generator integration tests
As an engineer, I want tests that exercise generator end-to-end (API + template) in CI using mocked or sample data, so that generation remains reliable.

Acceptance Criteria:
- Given sample fixture data and TestClient, when generator tests run, then preview and minimal generation paths validate output structure and do not require a local TeX binary in CI unless RUN_LATEX=true.
- Given mocked TeX invocation in CI, when generator integration test runs, then it verifies template rendering and final file write behavior (atomic rename, correct filename) without calling real TeX.
- Given generator preview output, when compared to expected snippet fixtures, then diffs are within acceptable ranges (exact checksums for IDs and structure).

Technical Notes:
- Add unit tests for template rendering (string-based), CLI parsing, and HTTP interactions (use `respx` to mock httpx calls).
- Add integration test that runs generator with TestClient overriding API base URL to local test server and mocks external TeX calls (monkeypatch subprocess calls or use a shim script).
- Guard real TeX invocation in CI with `RUN_LATEX` environment variable.

Prerequisites: Story 1.4, Story 3.1

---

## FR Coverage Matrix

- FR1: Covered by Epic 1 (stories 1.2,1.3) and Epic 2 (2.3)
- FR2: Covered by Epic 2 (2.1,2.2)
- FR3: Covered by Epic 1 (1.2) and Epic 2 (2.3)
- FR4: Covered by Epic 3 (3.1,3.2)
- FR5: Covered by Epic 1 (1.4)
- FR6: Covered by Epic 2 (2.2)
- FR7: Covered by Epic 2 (2.4) and Epic 3 (3.1)
- FR8: Covered by Epic 1 (1.4) and Epic 2 (2.5)
- FR9: Covered by Epic 1 (1.4) and Epic 2 (2.2)
- FR10: Covered by Epic 3 (3.2)

---

## Summary

- Epic count: 3 (Foundation, Importer, Generator)
- Story count (initial seeds): 11 stories across epics

**Next recommended actions:**
- Pick a story to expand into an implementation plan (I recommend `Story 1.1: Project packaging & dev quickstart` to remove import errors and enable running tests).
- I can generate `create-story` output for any story to produce checklist tasks and code changes.


---

Checkpoint — Epic 3 detailed stories: saved to `docs/epics.md`

━━━━━━━━━━━━━━━━━━━━━━━

Saved: step 4
