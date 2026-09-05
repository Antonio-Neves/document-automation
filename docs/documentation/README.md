# Developer Documentation

Welcome to the **Document Automation** developer documentation.

This folder contains the technical documentation of the project, written for
developers (and AI agents) who need to understand, maintain, or extend the
codebase. All documentation is written in English (US), as required by
[AGENTS.md](../../AGENTS.md).

> **Heads up for agents**: the file `docs/summary.md` (one level up) is a
> fast-moving project summary read at the start of every chat. This folder is
> the longer-form, human-oriented documentation.

---

## Contents

| # | File | What it covers |
|---|------|----------------|
| 1 | [01-getting-started.md](01-getting-started.md) | Prerequisites, environment variables, running the project |
| 2 | [02-architecture.md](02-architecture.md) | Project structure, apps, request flow, settings overview |
| 3 | [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md) | Contract views (CBVs), form processing, PDF generation with WeasyPrint |
| 4 | [04-frontend-and-styling.md](04-frontend-and-styling.md) | Base templates, Bootstrap 5, scoped CSS sections, legacy artifacts |
| 5 | [05-conventions.md](05-conventions.md) | Code, language, and workflow conventions (AGENTS.md distilled) |
| 6 | [06-adding-a-new-document-type.md](06-adding-a-new-document-type.md) | Step-by-step guide to add a new document type |
| 7 | [07-deployment.md](07-deployment.md) | DEBUG vs production settings, serving, release process |
| 8 | [08-roadmap-and-open-questions.md](08-roadmap-and-open-questions.md) | Next steps, known gaps, and open decisions |

---

## How this documentation is kept up to date

The codebase evolves rapidly (see `docs/summary.md`). The current policy is:

- Documentation is **written at milestones** — when a feature lands and
  stabilizes, its docs are updated in the same change.
- **Do not document speculation.** Only describe what exists today. Planned
  work lives in [08-roadmap-and-open-questions.md](08-roadmap-and-open-questions.md).
- There is intentionally **no PDF export yet**. Once the project stabilizes,
  a PDF generation step may be added on top of these Markdown sources.

The cadence (document earlier vs. later) is still being tuned — expect this
policy section to change.

---

## Where to find things quickly

| Question | Answer |
|----------|--------|
| How do I run the project? | [01-getting-started.md](01-getting-started.md) |
| Where is the contract logic? | [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md) |
| How do I add a new contract type? | [06-adding-a-new-document-type.md](06-adding-a-new-document-type.md) |
| Why is this file here / why is it unused? | [02-architecture.md](02-architecture.md) (legacy artifacts) |
| What are the rules I must follow? | [05-conventions.md](05-conventions.md) and `AGENTS.md` |
| What changed recently? | `docs/summary.md` (kept current by the AI workflow) |
