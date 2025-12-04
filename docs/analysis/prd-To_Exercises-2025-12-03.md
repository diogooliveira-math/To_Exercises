---
stepsCompleted: []
inputDocuments:
  - docs/analysis/product-brief-To_Exercises-2025-12-03.md
workflowType: 'prd'
lastStep: 0
project_name: 'To_Exercises'
user_name: 'Diogo'
date: '2025-12-03'
---

# Product Requirements Document - To_Exercises

**Author:** Diogo
**Date:** 2025-12-03


## Introduction

This PRD expands the Product Brief into actionable requirements for the MVP focused on core CRUD, importer, TDD scaffolding, and a FastAPI-based service with a generator CLI.

## Scope

MVP scope (as agreed):
- Persistent SQLite store with hierarchical model (Discipline, Module, Concept, ExerciseType, Exercise) and metadata.
- FastAPI CRUD service exposing endpoints for exercises and filters.
- Idempotent importer for ExerciseDatabase.
- Test-first development, automated tests for importer and CRUD flows.
- Minimal generator CLI that calls the FastAPI API with exercise IDs and produces a LaTeX PDF.

## Goals & Success Criteria
- Importer dry-run with anomalies report; re-running importer causes no duplicates.
- CRUD API passes functional TDD tests (create/read/update/delete flows).
- Generator produces a valid PDF for sample data using API-provided exercise payloads.

## Proposed MVP API Contract (initial)

- GET /exercises/{id} → returns exercise object
- POST /exercises → create exercise
- PUT /exercises/{id} → update exercise
- DELETE /exercises/{id} → delete exercise
- GET /exercises?tag=x&difficulty_min=1&module=... → query


## Next steps
1. Scaffold FastAPI project with models + SQLite + Alembic (optional) and tests.
2. Implement importer as a modular script invoked via CLI that can call service or write directly to DB (prefer via service to centralize logic).
3. Create minimal LaTeX template and generator CLI that calls API for exercises by ID.
4. Run import dry-run and iterate until anomalies acceptable.

