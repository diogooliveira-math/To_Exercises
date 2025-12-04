---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
inputDocuments:
  - docs/analysis/prd-To_Exercises-2025-12-03.md
  - docs/analysis/product-brief-To_Exercises-2025-12-03.md
  - docs/analysis/session-summary-To_Exercises-2025-12-03.md
  - docs/analysis/brainstorming-session-2025-12-02.md
workflowType: 'prd'
lastStep: 10
project_name: 'To_Exercises'
user_name: 'Diogo'
date: '2025-12-03'
---

# Product Requirements Document - To_Exercises

**Author:** Diogo
**Date:** 2025-12-03


## Introduction

(Placeholder) This PRD workspace was initialized by the PM facilitator. The content below will be appended as we work through the step-by-step PRD workflow.


## Discovered Input Documents

- docs/analysis/prd-To_Exercises-2025-12-03.md
- docs/analysis/product-brief-To_Exercises-2025-12-03.md
- docs/analysis/session-summary-2025-12-03.md
- docs/analysis/brainstorming-session-2025-12-02.md


## Executive Summary

To_Exercises is a backend-first product that provides a canonical exercise repository, deterministic import tooling, and a lightweight generation pipeline to produce LaTeX → PDF outputs. The MVP exposes a FastAPI-based CRUD service to manage exercises and a generator CLI that consumes the API to render PDFs. The system emphasizes idempotent import behavior, test-first development, and developer ergonomics so a single maintainer can reliably operate and evolve the project.

### What Makes This Special

- Canonical source-of-truth is a local file-based exercise set with metadata plus a checksum-driven importer that guarantees idempotent imports and robust duplicate detection.
- A minimal generator CLI integrated with the API produces LaTeX-based PDFs, keeping generation orthogonal to domain data and enabling reproducible outputs.
- Developer-first design: in-memory SQLite fixtures, TDD-first approach, and simple packaging to reduce onboarding friction for single-author maintenance.

## Project Classification

**Technical Type:** api_backend  
**Domain:** edtech (education / exercise content)  
**Complexity:** medium

Classification signals from the brief and documents:
- API, FastAPI, CRUD, endpoints, service
- Importer, dry-run, checksum, idempotent
- Generator, LaTeX, PDF, CLI
- Exercises, module, tags, difficulty
- TDD, in-memory SQLite, developer ergonomics

Proposed short vision statement (editable)

- “Make it trivial for a single maintainer to import, curate, and publish canonical exercise content as PDFs via a small, well-tested FastAPI service and generator CLI.”

Proposed problem statement (editable)

- “Authors and course maintainers need a reliable, idempotent way to import scattered exercise source files, manage canonical metadata, and generate consistent PDFs — current processes are error-prone and unreproducible.”

Who this serves (target users)

- Content authors and course maintainers (primary)
- Single-developer maintainers / ops (dev ergonomics)
- Instructors or curriculum teams generating printable PDFs

## Personas & Value Ladder (Elicitation)

- Content Author
  - Who: Course authors and exercise writers who prepare canonical exercise files.
  - Top 3 value outcomes:
    1. Confident, idempotent import of authored files with clear duplicate/issue reporting.
    2. Simple metadata editing and preview so content looks correct before publishing.
    3. Reliable PDF generation from selected exercises with predictable formatting.
  - Core features that deliver value: importer dry-run + anomaly report, metadata editor (CLI or small UI), generator CLI + preview command.

- Single-Developer Maintainer
  - Who: The solo engineer who maintains the service and tests.
  - Top 3 value outcomes:
    1. Fast, deterministic test runs (in-memory SQLite) and clear developer setup.
    2. Predictable upsert behavior and clear conflict handling to avoid data loss.
    3. Small, auditable code surface and easy local debug flow (logs, sample fixtures).
  - Core features that deliver value: test fixtures & docs, checksum upsert policy + explicit 409 conflict payload, concise README/dev quickstart and packaged layout.

- Instructor / Curriculum Operator
  - Who: Instructors assembling sets and producing PDFs for classes.
  - Top 3 value outcomes:
    1. Ability to select exercises, generate consistent PDFs, and include/exclude metadata.
    2. Confidence that generated PDFs match canonical content (no surprises).
    3. Simple way to re-run generation for updated content without manual cleanup.
  - Core features that deliver value: API list & filter endpoints, generator CLI with idempotent output paths, sample LaTeX template + conventions.

- Prioritization guidance (concise)
  1. First focus: Content Author → ensure importer dry-run and clear anomaly reporting (reduces biggest friction).
  2. Second: Single-Developer Maintainer → packaging, tests, and upsert/conflict semantics.
  3. Third: Instructor UX → generator polish and selection UX.

- Quick story triggers (BDD-style seeds)
  - Given an authored exercise file, when I run importer dry-run, then I receive a JSON anomalies report that lists duplicates and missing metadata.
  - Given a set of exercise IDs, when I run generator CLI, then a PDF is produced with consistent layout matching the sample template.
  - Given a checksum collision on import, when apply mode is used without --force, then API returns 409 with conflict_id and no data loss occurs.


## Innovation — JTBD Findings

1) Job statement / Declaração do job

- English: When I have a collection of authored exercise source files, I want to reliably import, validate, and publish them as consistent printable materials, so that I can produce class-ready PDFs without manual cleanup or duplication errors.
- Português: Quando eu tenho uma coleção de arquivos fonte de exercícios, eu quero importar, validar e publicar de forma confiável como materiais imprimíveis, para gerar PDFs prontos para aula sem limpeza manual ou erros de duplicação.

2) Current solutions people use / Soluções atuais

- English:
  - Manual: ad-hoc scripts + manual file edits + local LaTeX runs.
  - Spreadsheet or LMS uploads: manage metadata in a separate spreadsheet and hand-edit exports.
  - Single-purpose importer tools (homegrown) with brittle upsert semantics.
  - Full LMS or content platforms that are heavyweight and not developer-friendly.
- Português:
  - Manual: scripts ad‑hoc + edição manual + execuções locais de LaTeX.
  - Planilhas/LMS: metadados em planilhas e exportações manuais.
  - Ferramentas caseiras de importação com semântica de upsert frágil.
  - LMS completos, pesados e pouco amigáveis ao desenvolvedor.

3) Pain points / Dores reais

- English:
  - Non‑idempotent imports cause duplicates and data drift.
  - Missing or inconsistent metadata requires manual fixes before generation.
  - LaTeX build failures are noisy and hard to trace to source files.
  - Small teams/single maintainers struggle with setup, tests, and reproducibility.
  - Lack of clear anomaly reports means debugging import issues is time-consuming.
- Português:
  - Importações não idempotentes causam duplicatas e deriva de dados.
  - Metadados faltantes/inconsistentes exigem correções manuais antes da geração.
  - Falhas no build LaTeX são ruidosas e difíceis de vincular ao arquivo fonte.
  - Times pequenos/manutenção solo têm dificuldade com setup, testes e reprodutibilidade.
  - Falta de relatórios de anomalias claros torna a depuração demorada.

4) Unique value hypothesis (does this JTBD need exist & can To_Exercises win?) / Hipótese de valor único

- English — Hypothesis:
  - Combining a checksum-driven, two-stage importer (dry‑run + transactional apply), explicit anomaly reporting, and a generator that consumes the API yields a reproducible, low‑friction workflow that meaningfully reduces manual effort for authors and risk for maintainers.
  - This is defensible vs manual scripts because it makes idempotency explicit, auditable (checksum_history), and testable (in-memory fixture + contract tests).
- Português — Hipótese:
  - Combinar importador por checksum (dry‑run + apply transacional), relatórios de anomalias explícitos e gerador que consome a API produz um fluxo reprodutível e de baixa fricção, reduzindo esforço manual e risco para mantenedores.
  - É defensável em relação a scripts manuais porque torna idempotência explícita, auditável (checksum_history) e testável (fixtures em memória + testes de contrato).

5) Quick validation ideas (JTBD fit checks) / Ideias rápidas de validação

- English:
  - Run importer dry‑run on a realistic sample repo and measure number of manual fixes required vs current process (quantify reduction).
  - Simulate repeated imports (move/rename) to verify upsert + checksum_history prevents duplicates.
  - Do a short user test: ask an author to run import->preview->generate flow and rate effort/time and confidence.
- Português:
  - Rodar dry‑run em um repositório amostral e medir correções manuais necessárias vs processo atual (quantificar redução).
  - Simular importações repetidas (move/rename) para verificar se upsert + checksum_history evita duplicatas.
  - Teste usuário curto: pedir a um autor para executar import->preview->generate e avaliar esforço/confiança.

Recommendation (concise) / Recomendação

- English: Focus the MVP to prove JTBD by delivering a rock‑solid dry‑run report, deterministic upsert behavior, and a generator preview mode — those three reduce the largest observed pains.
- Português: Foque o MVP em provar o JTBD entregando dry‑run confiável, comportamento de upsert determinístico e modo de preview no gerador — esses três reduzem as maiores dores observadas.


## Non-Functional Requirements

### Performance

- NFR-P1: API read endpoints (GET /v1/exercises, GET /v1/exercises/{id}) respond within 300ms p95 under normal single-node dev/production load for datasets up to 10k exercises.
- NFR-P2: Importer dry-run and apply operations complete within 60s for a batch of 100 exercises (baseline), with progress reporting for long-running runs.

### Security

- NFR-S1: All production traffic must use HTTPS; sensitive tokens and credentials stored encrypted at rest.
- NFR-S2: Import apply and generation endpoints require authenticated requests (token-based); dry-run may allow looser dev-only access per configuration.
- NFR-S3: Basic role separation: admin-level actions (deprecate source, re-import) require elevated privileges.

### Reliability & Availability

- NFR-R1: Import apply operations must be atomic per run; partial applies are not permitted (transactional behavior).
- NFR-R2: System recovers from generator failures without corrupting canonical data; failed generation must produce retryable error state and logs.

### Observability & Logging

- NFR-O1: Importer and generator produce structured logs with run_id, counts (processed/created/updated/skipped), anomaly counts, and durations.
- NFR-O2: Dry-run reports are persisted and queryable for at least 90 days.

### Scalability

- NFR-SC1: System supports at least 10k exercises and batch operations without significant degradation. Scale beyond that is a post-MVP concern.
- NFR-SC2: Implement basic rate-limiting controls configurable per endpoint for production deployments (defaults provided).

### Accessibility

- NFR-A1: Public-facing UIs (post-MVP web UI) should conform to WCAG 2.1 AA where applicable. (MVP CLI is not subject to web accessibility.)

### Privacy & Compliance

- NFR-PV1: Do not collect PII by default. If PII is present in exercise content, document retention and redaction policy; provide a deletion mechanism.
- NFR-PV2: Provide ability to configure data retention windows for importer reports and logs.

### Measurable NFR Outcomes

- API p95 latency under 300ms for read endpoints (testable in CI).
- Batch importer 100-exercise run completes under 60s in baseline environment (document environment).
- Dry-run reports persisted with retrieval latency under 1s for most queries.


### Next steps
- Apply scoping to PRD (done).
- [C] Continue to Functional Requirements (Step 9) when you’re ready.
- [A] Advanced Elicitation to refine roadmap further.
- [P] Party Mode to get team feedback.

Epic 1 — Foundation & Developer Experience / Fundação e Experiência do Desenvolvedor

- User value statement:
  - English: “Provide a reliable, auditable foundation so a single maintainer can safely import, store, and evolve exercise data.”
  - Português: “Oferecer uma fundação confiável e auditável para que um único mantenedor importe, armazene e evolua dados de exercícios com segurança.”
- PRD coverage: Core persistence model, checksum uniqueness, importer idempotency, test-first developer UX.
- Technical context: FastAPI + SQLModel, SQLite for dev (in-memory for tests) with exercise_checksum_history and unique checksum index; upsert-by-checksum semantics; transactional apply.
- UX integration: CLI/small admin endpoints for dry-run verification and metadata preview.
- Dependencies: None (first epic).
- Sample story seeds:
  - Given a clean DB, when the schema migration runs, then exercise_checksum_history exists and unique index on checksum is present.
  - Given an exercise file with checksum X, when applied via import apply mode, then an upsert occurs and checksum history is appended.

Epic 2 — Idempotent Importer & Content Management / Importador Idempotente e Gestão de Conteúdo

- User value statement:
  - English: “Let content authors import their exercise files confidently with a dry‑run that surfaces duplicates and anomalies, then apply safely.”
  - Português: “Permitir que autores importem seus arquivos com confiança, com um dry‑run que mostra duplicatas/anomalias e um apply seguro.”
- PRD coverage: Importer dry-run, anomaly reporting, idempotent apply semantics, checksum conflict handling.
- Technical context: Two-stage importer: dry-run → JSON anomaly report; apply → transactional upsert using checksum; conflict 409 payload with conflict_id.
- UX integration: CLI commands: import dry-run, import apply (--force opt-in), and API endpoint to fetch last dry-run report.
- Dependencies: Builds on Epic 1 (DB & API).
- Sample story seeds:
  - Given a folder of exercise files containing duplicates, when dry-run is executed, then JSON report lists duplicates with file paths and checksums.
  - Given a checksum collision on apply, when apply runs without --force, then API returns 409 and no DB mutation occurs.

Epic 3 — Generator & Distribution Experience / Gerador e Experiência de Distribuição

- User value statement:
  - English: “Allow instructors and authors to assemble exercise sets and produce consistent, idempotent PDFs via the API and generator CLI.”
  - Português: “Permitir que instrutores e autores montem conjuntos de exercícios e gerem PDFs consistentes e idempotentes via API e CLI do gerador.”
- PRD coverage: Generator CLI, LaTeX template, selection/filter API endpoints, idempotent output handling.
- Technical context: Generator calls API to fetch exercise payloads, applies minimal LaTeX template, invokes local TeX (pdflatex/latexmk) if available. Output paths must be idempotent (overwrite by default or use versioned filename).
- UX integration: CLI: select by IDs / filter; preview mode to render minimal HTML or LaTeX snippet; generator returns structured result including warnings.
- Dependencies: Requires Epic 1 + Epic 2 (data model + importer).
- Sample story seeds:
  - Given selected exercise IDs, when generator CLI runs in preview mode, then a rendered LaTeX snippet is produced and no PDF is written.
  - Given generator run with IDs, when successful, then final PDF is produced at the expected output path and contains canonical content.

## Success Criteria

### User Success

- Content Author: Successful import flow — importer dry-run provides actionable anomalies report and a measurable reduction in manual post-import fixes.
- Instructor: Able to generate a PDF for a selected exercise set, and confirm PDF matches canonical content (acceptance via sample QA).
- Developer: Tests run deterministically using in-memory SQLite; CI demonstrates stability and low flakiness over repeated runs.

### Business Success

- Minimal viable adoption: initial org/course uses generated PDFs in a pilot (define scope with user).
- Developer productivity: clear dev quickstart and packaging reduce onboarding friction.
- Operational reliability: importer apply mode avoids data loss via transactional upserts and conflict handling.

### Technical Success

- Importer dry-run produces JSON report with anomalies and deduplication candidates for every run.
- Apply mode is transactional and idempotent (no duplicate exercise records by checksum).
- API contract implemented with OpenAPI and contract tests passing in CI.

### Measurable Outcomes

- FR coverage: All PRD functional requirements will be mapped to stories before implementation.
- Acceptance Test Pass Rate: All PRD-mapped stories pass in CI.
- Importer anomaly rate baseline established and reduced over iterations.

## Product Scope

### MVP - Minimum Viable Product

- Foundation: DB schema, checksum history, basic API endpoints, importer dry-run.
- Core flows: import dry-run + apply, basic generator CLI, simple metadata editor/preview.
- Tests & CI: in-memory test fixtures, unit + integration tests for core flows.

### Growth Features (Post-MVP)

- Web UI for metadata editing and preview
- Advanced templating for generator (themes, layouts)
- Multi-author collaboration, user roles

### Vision (Future)

- Hosted service option with multi-user management and richer export formats.


Reply with [A] Advanced Elicitation, [P] Party Mode, or [C] Continue to proceed to User Journey Mapping (Step 4 of 10).