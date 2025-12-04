# ADR 0001 — Checksum & Upsert Policy

Status: proposed
Date: 2025-12-03

Context
- Imports and automated ingestion require stable, idempotent deduplication of Exercise artifacts.
- Files may be moved/renamed while retaining identical content; importer must detect this by content fingerprinting.

Decision
- Use a checksum-based deduplication strategy with an explicit checksum_algorithm field.
- Enforce uniqueness at the DB level using a unique index on (checksum, checksum_algorithm).
- Maintain an append-only exercise_checksum_history table recording checksum, file_path and recorded_at for every import/apply event.
- Upsert semantics (apply mode):
  - If (checksum, checksum_algorithm) exists:
    - Update the existing Exercise record's metadata and file_path when appropriate.
    - Append a new row to exercise_checksum_history capturing the change.
    - Return the existing resource id in the API response.
  - If automatic merge is unsafe (e.g. checksum exists but other critical fields differ semantically):
    - Return 409 Conflict with payload describing the difference and the conflicting resource id.
    - CLI may offer --force to override and create a new record; server will require explicit override behavior.

Rationale
- Checksum provides deterministic idempotency regardless of file path.
- Recording history allows tracking moves/renames and diagnosing importer anomalies.
- DB-level uniqueness guards against race conditions during concurrent imports.

Schema sketch
- Table: exercise_checksum_history
  - id: integer PK
  - exercise_id: integer FK -> exercises.id (nullable if new record creation fails)
  - checksum: text
  - checksum_algorithm: text
  - file_path: text
  - recorded_at: datetime (UTC)
  - metadata_snapshot: text (optional JSON string)

API behavior
- POST /v1/exercises (apply mode)
  - success (new): 201 Created with created resource
  - success (upsert): 200 OK with existing/updated resource
  - conflict: 409 with body {"error":"checksum_conflict","message":"...","conflict_id": 123}

Operational notes
- Importer dry-run mode must report intended upserts, duplicates, and anomalies without writing to DB.
- Include checksum_algorithm in outputs so future algorithm changes remain backward compatible.
- Add a migration/maintenance task to backfill checksum_algorithm where missing.

Consequences
- Simple, deterministic merging for identical content.
- Additional storage cost for the history table, but valuable for audit and diagnostics.
- Requires clear CLI flags for forced creation when operator intends to override deduplication.

Next steps
- Implement exercise_checksum_history SQLModel and migrations (or direct SQL for SQLite).
- Add API responses and tests for 200/201/409 behaviors.
- Add importer dry-run report to include checksum_algorithm and history hints.

Approved-by: Diogo
