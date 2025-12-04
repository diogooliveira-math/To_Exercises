# Story 2.2 — Import apply with transactional upsert

As an operator, I want apply mode to be transactional and avoid duplicates so that production data integrity is preserved.

Acceptance Criteria (BDD):
- Given a set of valid exercise files, when I run `import --apply`, then the operation completes atomically and either all changes are applied or none are.
- Given a checksum conflict during apply, when conflict occurs, then the API/CLI returns 409 with a conflict_id and no partial mutations.

Technical Implementation Notes:
- Use DB transactions to ensure atomicity; in SQLite, use BEGIN/COMMIT semantics appropriately.
- Enforce uniqueness at DB-level and catch IntegrityError to translate into 409 error with conflict_id.

Test Checklist:
- [ ] Add tests that simulate conflicting checksum and assert 409 behavior
- [ ] Verify rollback semantics on partial failure

Definition of Done:
- Apply mode transactional and tested
- Conflict payload format documented and implemented

Saved: docs/stories/2-2-import-apply-transactional.md
