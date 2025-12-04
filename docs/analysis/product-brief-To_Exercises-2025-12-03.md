---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - docs/analysis/brainstorming-session-2025-12-02.md
workflowType: 'product-brief'
lastStep: 0
project_name: 'To_Exercises'
user_name: 'Diogo'
date: '2025-12-03'
---

# Product Brief: To_Exercises

**Date:** 2025-12-03
**Author:** Diogo

---

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary / Resumo Executivo

PT:
Este projeto fornece uma solução prática para professores de matemática: um núcleo hierárquico de exercícios (Disciplina → Módulo → Conceito/Tema → Tipo → Exercício) que facilita CRUD, organização e pesquisa, combinado com um sistema modular de geração de materiais didáticos (sebentas, PDFs) com controlo granular. O produto destina-se ao uso diário por professores (reduzir tempo e fricção), enquanto o desenvolvimento será conduzido por um único autor nas horas vagas — daí a necessidade de práticas e arquitetura que tornem o desenvolvimento eficiente, automatizável e sustentável, com apoio de IA.

EN (short):
A practical exercise repository and content-generation system for math teachers, designed for daily use; development is single-author, IA-assisted, modular, and test-driven.

## Core Vision / Visão Principal

PT:
- Produto alvo: Ferramenta prática que permite que um professor gere, edite, organize e gere materiais a partir de uma base de exercícios hierarquizada, com operações CRUD simples e filtros úteis (dificuldade, variante, tipo, tags).
- Desenvolvimento: Projeto construído por uma pessoa (tu), nas horas vagas, com processos que maximizam produtividade (scaffolding por IA, TDD, API-first, modular architecture). Arquitetura hexagonal: core de domínio (DB + regras), adaptadores (importadores, UI/CLI, geradores), e integrabilidade futura (GenIA, web UI, scripts LaTeX).
- Integração futura: facilitar acrescentar GenIA para geração de exercícios, scripts automáticos de geração LaTeX → PDF, e um website/serviços que consumam a API sem mudar o core.

### Problem Statement / Declaração do Problema (revisto)

PT:
Professores perdem tempo a recolher e reformatar material didático encontrado, repetem trabalhos manuais para criar fichas e têm dificuldade em manter variantes e consistência. Para ti, o problema inclui também a necessidade de um sistema que suporte um fluxo de trabalho pessoal e um desenvolvimento sustentável (evitar repetir “spaghetti code”).

### Proposed Solution / Solução Proposta (enfática na separação)

PT:
- Core de domínio (DB leve, p.ex. SQLite em dev) indexando ficheiros LaTeX e metadados com modelo hierárquico canónico.  
- API-first (endpoints CRUD, filtros, import/export) para separar consumo (UI, scripts, GenIA) do armazenamento.  
- Camada de geração modular (consome o core) responsável por templates LaTeX, montagem de sebentas, PDFs e pipelines de export.  
- Desenvolvimento orientado a TDD, API contracts, modularização e uso de IA para acelerar scaffolding, geração de testes e refatoração.  
- Migração/limpeza: reusar e finalizar o artefacto existente (C:\Users\diogo\projects\To_Exercises\ExerciseDatabase) por um import dry-run e mapeamento canónico.

### Why Existing Solutions Fall Short (correção)

PT:
- Muitas soluções existentes obrigam a trabalhos manuais repetitivos; no teu caso anterior, o problema foi agravado por código ad-hoc gerado durante o desenvolvimento, criando desordem. O produto que propomos evita isso com contrato de API, testes e separação clara de responsabilidades.

### Key Differentiators / Diferenciadores

- Projeto pensado para um único desenvolvedor com automação por IA.  
- Separação clara entre uso diário (produto) e desenvolvimento (fluxo IA-assistido).  
- Arquitetura que facilita expansões (GenIA, website) sem reescrever core.

### Constraints / Restrições importantes

- Deve ser possível desenvolver e manter o projeto por uma pessoa com emprego a tempo inteiro.  
- Priorizar simplicidade e automação antes de optimizações prematuras.  
- Reuso e migração segura do artefacto C:\Users\diogo\projects\To_Exercises\ExerciseDatabase.

Sugestões de próximos passos concretos (minha recomendação)
1. Import dry-run completo do ExerciseDatabase → relatório (anomalias, duplicados, campos faltantes).  
2. Definir um primeiro API contract mínimo (CRUD para Exercise + endpoints de busca/filtragem).  
3. Esboçar o modelo de dados (ER) com exemplos reais a partir dos ficheiros importados.  
4. Gerar scaffolding de testes TDD para as regras de domínio essenciais (ex.: import idempotente, uniqueness via checksum).  
5. Planeamento de um pipeline de geração minimal (LaTeX template + script de construção) que pode ser chamado pela API.

## Target Users

### Primary User — Diogo (Teacher / Developer)
PT:
- Perfil: Professor de matemática (ensino profissional e/ou secundário/terciário), também desenvolvedor do sistema nas horas vagas. Mantém um folder local com exercícios LaTeX (ExerciseDatabase) e tem conforto com Python/SQLite/LaTeX.
- Motivações: reduzir trabalho manual diário; gerir variantes, evitar duplicações; gerar sebentas/PDFs com controlo granular; manter desenvolvimento sustentável (um autor) com apoio de IA.
- Restrições: tempo limitado; prefere ferramentas que exponham APIs/CLI simples e que sejam testadas e modulares.
- Sucesso: import idempotente do histórico, criação/edição rápidas de exercícios, geração repetível de materiais em fluxos curtos.

EN (short): Teacher who also develops the tool — needs effortless daily workflows and dev practices that scale for a single author.

### Secondary Users
PT:
1. Outros professores de matemática — variam em literacia técnica; alguns preferem UI simples, outros CLI/API.  
2. Administrador de departamento / coordenador — interessado em partilha, permissões, currículos, arquivo.  
3. Stakeholder: Estudantes — consumidores finais do material (detalhado abaixo).

EN: secondary stakeholders include peer teachers and department staff; students are an important stakeholder group.

### Student Stakeholder (detailed)

PT:
- Perfil: Estudantes de ensino profissional (por exemplo: informática, desporto, culinária, contabilidade, farmácia, cabeleireiro). Categoria: “Estudante de ensino profissional”.
- Preferências pedagógicas:
  - Progressão linear e fractal (scaffold + repetição intencional).
  - Fortemente valorizam exercícios com contexto aplicado ao mundo profissional e doméstico.
  - Exemplos de contextos reais a incluir: decisões económicas domésticas, gestão e logística familiar (orçamentos, planeamento de compras), poupanças e juros, impostos simples, faturação/contabilidade básica, análise de dados aplicada (p.ex. métricas em redes sociais), problemas de logística (rotas, otimização simples), e cenários profissionais (restaurante, ginásio, oficina, farmácia).
  - Mistura desejada: problemas abstratos para treino formal + muitos exercícios aplicados que liguem a experiências diárias/profissionais.
- Como usam o material:
  - Leem sebentas/folhas de exercícios, resolvem em aula e em casa; apreciam exemplos que referenciem ferramentas/populares apps quando relevantes.
- Sucesso para estudante:
  - Conseguir aplicar conceitos matemáticos em cenários profissionais/domésticos relevantes; ver coerência e repetição de ideias ao longo das sessões.

EN (short): Students = vocational-education learners; prefer scaffolded, recurring, and real-world-flavoured exercises that make math relevant.

### User Journeys (high-level, for each persona)

- Diogo (Teacher / Developer)
  - Discovery: Uses local repo or personal notes → decides to import into the system.
  - Onboarding: Runs import dry-run → resolves anomalies → maps hierarchy (Disciplina→Módulo→Conceito→Tipo→Exercício).
  - Core Use: Create/Edit/Tag exercises, assemble sets by filter (difficulty, theme, context), trigger LaTeX generation → produce sebenta/PDF, review and iterate.
  - Development Flow: Create API contract → scaffold code via IA → write tests → merge; uses modular generation adapters to add new templates or GenIA later.
  - Success moment: First full sebenta generated automatically with correct variants and minimal manual patching.

- Other Teachers
  - Onboarding: Import sample dataset or use shared repository; use UI/CLI guided flows to find/filter exercises and generate worksheets.
  - Core Use: Search by curriculum topic or tag; assemble printable sheets; save presets for future classes.

- Department Admin
  - Onboarding: Connect to repo or central store; assign permissions; curate shared collections.
  - Core Use: Export curriculum reports, track usage, manage backups.

- Students
  - Discovery: Receive sebenta/worksheet in class or via LMS/email.
  - Core Use: Work exercises in provided order (linear), revisit repeated core ideas (fractal), apply to practical contexts.
  - Success moment: Recognize progression across exercises and apply math to a familiar real-world task.

Implications for product design (brief)

- Metadata must capture: progression level, variant linkage (parent/child), context/theme (e.g., “social-media”, “accounting”), real-world tags, and difficulty.  
- Support for templated LaTeX output that can express scaffolding (hints, worked examples) and multiple variants.  
- API endpoints to select exercises by progression/recurrence patterns and contextual tags.  
- Importer should preserve parent/child relationships and detect duplicate variants by checksum.  
- UX: allow Diogo quick presets to assemble a “linear + fractal” sebenta (choose core concepts, set recurrence frequency, choose contextual domain).

Candidate user-focused success metrics (suggestions)

- Teacher workflow: Generate a lesson sebenta in under 10 minutes from selection → PDF.  
- Import quality: Dry-run import with < 5 anomalies per 100 exercises (configurable).  
- Student engagement: > X% of exercises in generated materials include real-world context tags (configurable).  
(We can refine numerical targets if you want.)

---

## Success Metrics

- Core operational metrics:
  - CRUD Reliability: Automated tests that validate create/read/update/delete for Exercise records and metadata.
  - Import Idempotency: Importer tests that assert running the import twice does not create duplicates or break parent/child links.
  - Test-driven Quality: Project has an automated test suite that runs on CI; tests must pass for changes to be accepted.

- Notes:
  - Student contextual coverage and early-adoption metrics are optional and deferred to a later generation module or GenIA integration.
  - No business/adoption metrics are defined — the project remains personal and developer-focused.

---

## MVP Scope

### Core Features

1. Persistent exercise store (SQLite) with hierarchical model: Discipline → Module → Concept → ExerciseType → Exercise. Includes metadata fields (title, difficulty, tags, parent_exercise_id, variant_index, file_path, checksum).
2. CRUD API (FastAPI HTTP service) exposing endpoints to create/read/update/delete exercises and query by filters (tags, difficulty, module, checksum). The API will be the single source of truth for clients.
3. Importer: idempotent dry-run importer from ExerciseDatabase folder that reports anomalies (missing metadata, duplicate checksum, unmapped parent/child).
4. Test suite (TDD-first): automated tests covering the importer, uniqueness rules, and CRUD flows.
5. Minimal generation script (CLI) that calls the CRUD API to fetch exercises by list of IDs, assembles fetched exercises into a LaTeX document and runs a LaTeX build to produce a PDF. This CLI talks to the local FastAPI service (HTTP) and uses exercise IDs as input.
6. Documentation: README with quickstart for import, CRUD usage examples, how to run the generator, and how to run tests.

### Out of Scope for MVP

- Full modular generation module with complex templates and recurrence logic for sebentas.
- Web UI or hosted deployment.
- GenIA integrations or advanced automation scaffolding.
- Complex user/permission management and sharing features.

### MVP Success Criteria

1. Importer runs in dry-run mode and produces a report with anomalies; running the importer twice causes no duplicates (idempotency test passes).
2. CRUD API functional tests pass: create → read → update → delete round-trip works for typical exercise records.
3. Minimal generation script produces a valid PDF from a small sample (LaTeX build succeeds with provided template) by calling the CRUD API.
4. Test suite runs in CI and passes locally (developer can run tests easily).
5. README provides clear steps for setup, import, and generation.

### Future Vision

- Modular generation adapters, GenIA-powered exercise creation, web UI, sharing/permissions, presets for vocational tracks, advanced analytics.

