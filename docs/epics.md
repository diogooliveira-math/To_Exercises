# To_Exercises - Epic Breakdown

**Author:** Diogo
**Date:** 2025-12-04

---

## Overview

This document provides the complete epic and story breakdown for To_Exercises, decomposing the requirements from the PRD into implementable stories.

**Living Document Notice:** This is the initial version. It will be updated as we refine technical and UX details.

Epics Summary:
- Epic 1: Foundation & Developer Experience — Deliver a reproducible dev environment, DB schema, and CI to enable reliable development.
- Epic 2: Importer & Content Management — Provide deterministic import with dry‑run and anomaly reports to create canonical exercise data.
- Epic 3: API & CRUD — Expose endpoints to manage exercises and support generator integration.
- Epic 4: Generator & Preview — Provide generator CLI and preview mode for PDF generation workflows.

---

## Functional Requirements Inventory

- FR1: Importer dry‑run and anomaly reporting
- FR2: Deterministic upsert behavior by checksum
- FR3: API endpoints for CRUD and listing
- FR4: Generator preview mode
- FR5: Developer quickstart and reproducible tests

---

## FR Coverage Map

- FR1 → Epic 2
- FR2 → Epic 2
- FR3 → Epic 3
- FR4 → Epic 4
- FR5 → Epic 1

---

## Epic 1: Foundation & Developer Experience

User Value: Provide a reliable, auditable foundation so a single maintainer can safely import, store, and evolve exercise data.

PRD Coverage: Core persistence model, checksum uniqueness, importer idempotency, test-first developer UX.

Technical Context:
- FastAPI + SQLModel, SQLite for dev; design portable to Postgres
- In-memory SQLite fixtures for tests

Dependencies: None (foundation epic)

Stories:

### Story 1.1: Dev environment and CI setup
As a maintainer, I want a reproducible dev environment and CI that runs tests so that development is deterministic and onboarding is trivial.

Acceptance Criteria:
- README dev quickstart exists
- CI runs pytest on push
- In-memory test fixture present

Technical Notes:
- Add GitHub Actions job: install deps, run pytest
- Provide dockerfile for dev and CI (optional)

### Story 1.2: DB schema and migrations
As a developer, I want a clear DB schema and migration strategy so that data model changes are manageable.

Acceptance Criteria:
- SQLModel models are present and create_all works
- Document checksum uniqueness recommendation

Technical Notes:
- Consider Alembic for migrations in future

---

## Epic 2: Importer & Content Management

User Value: Let content authors import files confidently with a dry‑run that surfaces anomalies and a transactional apply.

PRD Coverage: Importer dry‑run, anomaly reporting, idempotent apply semantics, checksum conflict handling.

Technical Context:
- Upsert-by-checksum strategy implemented in crud.upsert_by_checksum

Stories:

### Story 2.1: Importer dry-run report
As a content author, I want a dry‑run that lists duplicates and anomalies so that I can fix issues before applying.

Acceptance Criteria:
- Dry‑run outputs JSON anomaly report with file paths and checksums
- CLI command: import --dry-run outputs report

Technical Notes:
- Implement dry-run mode that does not mutate DB; use checksum comparisons against current DB state

### Story 2.2: Import apply with transactional upsert
As an operator, I want apply mode to be transactional and avoid duplicates so that production data integrity is preserved.

Acceptance Criteria:
- Apply mode uses DB transactions and returns 409 on conflict with conflict_id
- ExerciseChecksumHistory entries created on new and changed file paths

Technical Notes:
- Enforce uniqueness constraint on (checksum, checksum_algorithm) in migration

---

## Epic 3: API & CRUD

User Value: Provide programmatic access to canonical exercise data for integrations and the generator.

PRD Coverage: CRUD endpoints and list/search capabilities

Stories:

### Story 3.1: Basic CRUD endpoints
As an integrator, I want POST/GET/PUT/DELETE endpoints to manage exercises so that other tools can interact with the canonical dataset.

Acceptance Criteria:
- POST /v1/exercises upsert-by-checksum works
- GET endpoints return expected response models
- Contract tests exist

Technical Notes:
- Use FastAPI automatic OpenAPI; ensure response models match SQLModel schemas

---

## Epic 4: Generator & Preview

User Value: Allow authors to preview and generate PDFs from canonical exercise sets.

PRD Coverage: Generator CLI and preview

Stories:

### Story 4.1: Generator preview mode
As an author, I want a preview mode that renders a LaTeX snippet or HTML so that I can verify output before building a PDF.

Acceptance Criteria:
- generator preview command renders sample LaTeX or HTML without invoking pdflatex
- Preview includes selected exercise metadata

Technical Notes:
- Implement preview flag; keep generator decoupled from API for integration tests

---

## FR Coverage Matrix

- FR1 → Story 2.1
- FR2 → Story 2.2
- FR3 → Story 3.1
- FR4 → Story 4.1
- FR5 → Story 1.1

---

## Summary

This initial epic breakdown maps PRD items to epics and stories with technical guidance. Next: generate individual story implementation plans or proceed to sprint planning.

Saved: docs/epics.md
