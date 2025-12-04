# Story 2.1 — Importer dry-run report

As a content author, I want a dry‑run that lists duplicates and anomalies so that I can fix issues before applying.

Acceptance Criteria (BDD):
- Given a folder of exercise files, when I run `import --dry-run`, then a JSON anomaly report is produced listing duplicates, missing metadata, and suggested fixes.
- Given the dry-run report, when I review it, then file paths, checksums, and suggested remediation are present.

Technical Implementation Notes:
- Implement a CLI command `import --dry-run` that scans input paths and compares checksums to current DB (non-mutating).
- Report structure: {"files": [{"path": "...", "checksum": "...", "issues": ["missing metadata"]}], "summary": {"duplicates": 2, "missing_metadata": 3}}

Test Checklist:
- [ ] Dry-run produces JSON report format and sample output in test fixture
- [ ] Add unit tests for anomaly detection logic

Definition of Done:
- Dry-run command implemented and tested
- Report format documented

Saved: docs/stories/2-1-importer-dry-run.md
