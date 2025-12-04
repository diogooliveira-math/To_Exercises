# Data Models (generated)

This document summarizes the primary SQLModel data models used by To_Exercises.

## Exercise

- id: integer (primary key)
- checksum: string (indexed) — unique detection key for import
- checksum_algorithm: string (default: sha256)
- file_path: string — original source file path
- parent_exercise_id: integer (nullable) — FK to Exercise.id
- tags_json: string (nullable) — JSON-serialized array of tags
- metadata_json: string (nullable) — JSON-serialized dict for arbitrary metadata
- created_at: datetime (ISO8601 UTC)
- updated_at: datetime (ISO8601 UTC)

Notes:
- exercise_checksum_history table records historical checksum/file_path pairs per exercise. This supports idempotent imports and conflict resolution.
- For production, consider adding explicit uniqueness constraints on (checksum, checksum_algorithm) and indexes for common query fields (tags, created_at).
