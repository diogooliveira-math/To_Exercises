# Story 3.1 — Basic CRUD endpoints

As an integrator, I want POST/GET/PUT/DELETE endpoints to manage exercises so that other tools can interact with the canonical dataset.

Acceptance Criteria (BDD):
- Given valid exercise payload, when POST /v1/exercises is called, then the exercise is created or updated (upsert) and returned.
- Given an existing exercise, when GET /v1/exercises/{id} is called, then the exercise data is returned with 200 status.
- Given invalid input, when POST is called without checksum, then 400 is returned.

Technical Notes:
- Expand endpoints to include PUT and DELETE as needed; ensure permission model is clarified in PRD for production.

Saved: docs/stories/3-1-basic-crud.md
