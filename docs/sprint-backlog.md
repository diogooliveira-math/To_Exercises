# Sprint Backlog — Initial Sprint (MVP Focus)

Author: Diogo (facilitated by BMad Master)
Date: 2025-12-04

English / Português

---

Sprint Goal / Objetivo da Sprint:
- English: Prepare the codebase, tests, and core workflows required to deliver a minimal, reliable MVP for To_Exercises: deterministic importer, basic CRUD API, and generator preview.
- Português: Preparar o código, testes e fluxos centrais necessários para entregar um MVP mínimo e confiável para To_Exercises: importador determinístico, API CRUD básica e preview do gerador.

Prioritized Backlog (grouped by Epic) / Backlog priorizado (agrupado por Épico):

Epic 1 — Foundation & Developer Experience (High) / Fundação & Experiência do Desenvolvedor (Alto)
- Story 1.1: Dev environment and CI setup — README quickstart, CI job running pytest, dockerfile (if desired)
  - Acceptance highlights: quickstart validated, CI runs pytest, tests pass on CI

Epic 2 — Importer & Content Management (Highest) / Importador & Gestão de Conteúdo (Mais Alto)
- Story 2.1: Importer dry-run report — CLI dry-run JSON anomaly report
  - Acceptance highlights: dry-run JSON report lists duplicates/missing metadata
- Story 2.2: Import apply with transactional upsert — atomic apply, 409 conflict payload
  - Acceptance highlights: transactional apply, 409 on conflict with conflict_id, history entries created

Epic 3 — API & CRUD (High) / API & CRUD (Alto)
- Story 3.1: Basic CRUD endpoints — POST/GET (upsert by checksum), list endpoint
  - Acceptance highlights: upsert works, 400 when checksum missing, contract tests exist

Epic 4 — Generator & Preview (Medium) / Gerador & Preview (Médio)
- Story 4.1: Generator preview mode — preview LaTeX/HTML without building PDF
  - Acceptance highlights: preview returns snippet and no PDF build invoked

Backlog ordering rationale / Racional de priorização:
- Establish reliable developer environment and CI first so all subsequent work is reproducible. / Preparar ambiente e CI primeiro para garantir reprodutibilidade.
- Implement importer core (dry-run + transactional apply) as the highest priority because canonical data is required before meaningful features. / Implementar o importador (dry-run + apply transacional) é prioridade máxima.
- Provide API and contract tests next so integrations and generator can rely on stable endpoints. / API e testes de contrato garantem estabilidade para integrações.
- Generator preview is important but depends on canonical data and API; schedule after core flows. / Preview depende de dados canônicos e da API.

Definition of Ready / Definição de Pronto:
- PRD and Architecture referenced (available) — OK
- Acceptance criteria present in story files — OK
- No time estimates included (by design) — OK

Next immediate actions (choose one) / Próximas ações imediatas (escolha uma):
1) Start sprint planning: convert stories into tasks and assign priorities (detailed task breakdown). / Iniciar planejamento da sprint: converter histórias em tarefas e atribuir prioridades.
2) Create issue tickets (export story files to issue format for tracker). / Criar tickets (exportar para tracker).
3) Run implementation-readiness check (validate stories against architecture). / Rodar checagem de prontidão de implementação.
4) Finalize backlog and exit to menu. / Finalizar backlog e retornar ao menu.

Saved: docs/sprint-backlog.md

---

BMad Master awaits your selection (1–4) / BMad Master aguarda sua seleção (1–4).
