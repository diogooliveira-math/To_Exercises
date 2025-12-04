---
stepsCompleted: [1, 2]
inputDocuments: []
session_topic: 'Minimal Exercise Database core with LaTeX storage; postpone generators'
session_goals: 'Domain model, DB indexing of LaTeX files, Python API (CRUD), extensible adapter design'
selected_approach: 'ai-recommended'
techniques_used: ['structured: Decision Tree Mapping', 'structured: Solution Matrix', 'creative: Concept Blending']
ideas_generated: []
context_file: 'C:\Users\diogo\projects\To_Exercises\ExerciseDatabase'
---

# Brainstorming Session Results

**Facilitator:** Diogo
**Date:** 2025-12-02

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Minimal Exercise Database core with LaTeX storage; postpone generators

**Recommended Techniques:**

- **Decision Tree Mapping:** Map out core decisions (storage format, schema, API boundaries, migration strategy). Expected outcome: clear decision paths and criteria for choosing each technology and approach.

- **Solution Matrix:** Systematic grid of options for storage and indexing vs. pros/cons. Expected outcome: prioritized options for immediate implementation (SQLite index + LaTeX files, then Postgres + JSONB later).

- **Concept Blending:** Merge the idea of LaTeX-first storage with a lightweight DB index and API contract-first development. Expected outcome: concrete hybrid architecture to keep LaTeX editable while enabling API-driven features.

**AI Rationale:** These techniques are structured and practical, ideal for a solo developer needing actionable decisions, a clear migration plan for existing LaTeX assets, and a roadmap that keeps the system extensible while minimizing early complexity.

**Estimated Time:** ~60-90 minutes interactive planning (we can split into multiple shorter sessions)

**Next:** Continue to technique execution to produce concrete artifacts: schema drafts, API spec, migration plan, and initial test-suite scaffolding.

---

## Session Summary (EN / PT)

EN — Summary of decisions and current state:
- Core goal: build a minimal, maintainable Exercise Database indexing your LaTeX exercises; postpone generation (worksheet/assessment) features to adapters.
- Canonical storage: filesystem folder hierarchy (Disciplina → Tema/Module → Conceito → Tipo → Exercício). Prefer folder-level metadata.json when present.
- Tech choice: Python (FastAPI + SQLModel/SQLite for dev). Store LaTeX files on disk; index metadata and file paths in a lightweight DB. Materialize frequently queried fields (has_subvariants, difficulty_min/max, requires_graph, requires_calculation) and keep original JSON in a metadata column.
- Parent/child model: represent groups (folders with has_subvariants) as parent rows and concrete .tex variants as child rows (parent_exercise_id, variant_index). Use file_path as canonical unique key; use checksum to detect moved/duplicated files.
- Import strategy: idempotent, dry-run first, robust key fallbacks (metadata.json, per-exercise JSON, filename prefix matching). Produce import reports and resolve missing IDs interactively.

PT — Resumo das decisões e estado atual:
- Objetivo: criar uma base de exercícios mínima e sustentável que indexe os ficheiros LaTeX; adiar funcionalidades de geração (sebentas/testes) como adapters.
- Armazenamento canónico: estrutura de pastas (Disciplina → Tema/Módulo → Conceito → Tipo → Exercício). Preferir metadata.json a nível de pasta quando existir.
- Stack: Python (FastAPI + SQLModel/SQLite em desenvolvimento). Guardar ficheiros LaTeX no disco; indexar metadados e caminhos no DB. Materializar campos de consulta frequente (has_subvariants, difficulty_min/max, requires_graph, requires_calculation) e manter o JSON original na coluna metadata.
- Modelo pai/filho: representar grupos (pastas com has_subvariants) como linhas pai e variantes concretas como linhas filhas (parent_exercise_id, variant_index). Usar file_path como chave canónica; checksum para detectar duplicados/movimentos.
- Estratégia de importação: idempotente, executar dry-run primeiro, tratar variações nas chaves (metadata.json, JSON por exercício, matching por prefixo). Gerar relatórios de importação e resolver IDs em falta interativamente.

---

## Next actions chosen by user
1) Append this session summary to the brainstorming session document (completed).
2) Run a parent/child-aware import dry-run to validate mappings and surface anomalies (requested next).

I will now run the dry-run import (read-only) and produce a report in docs/analysis. No files will be modified.
