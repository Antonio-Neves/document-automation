# Developer Documentation

Welcome to the **Document Automation** developer documentation.

This folder contains the technical documentation of the project, written for
developers (and AI agents) who need to understand, maintain, or extend the
codebase. All documentation is written in English (US), as required by
[AGENTS.md](../../AGENTS.md).

> **Entry point for agents**: this README is read at the start of every chat
> (see `AGENTS.md`). Follow the links to the chapter relevant to the task:
> [03](03-dashboard-and-contract-flow.md) for the contract flow,
> [06](06-adding-a-new-document-type.md) when adding a document type, and
> [08](08-roadmap-and-open-questions.md) for pending work and open decisions.

## Current state

- The project generates legal documents (contracts) as downloadable PDFs,
  filled from an in-memory form and rendered with WeasyPrint.
- Every document type uses two sibling templates (a page form and a standalone
  PDF template) and one class-based view.
- The document types implemented so far are listed in the single index below;
  new types are added following
  [06-adding-a-new-document-type.md](06-adding-a-new-document-type.md).
- Nothing about the templates or the form data is persisted — only the
  generated PDFs are written to `contract_files/created_contracts/`.
- Pending work and open decisions live in
  [08-roadmap-and-open-questions.md](08-roadmap-and-open-questions.md).

---

## Implemented document types

**Single source of truth** for which document types exist. Other chapters link
back to this table instead of re-listing the types.

| Type (`name` = template prefix) | Route | View | Menu label |
|---------------------------------|-------|------|------------|
| `contract_sale_vehicle` | `/contract-sale-vehicle/` | `ContractSaleVehicleView` | Veículo |
| `contract_sale_property` | `/contract-sale-property/` | `ContractSalePropertyView` | Imóvel |

Each type has a page template `<type>.html` and a PDF template `<type>_pdf.html`
under `dashboard/templates/dashboard/`. The browser tab shows the view's
`page_title`, which may differ from the menu label (e.g. the vehicle tab shows
"Veículo Completo").

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

The codebase evolves rapidly. The current policy is:

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
| Which document types exist today? | [Implemented document types](#implemented-document-types) above |
| Where is the contract logic? | [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md) |
| How do I add a new contract type? | [06-adding-a-new-document-type.md](06-adding-a-new-document-type.md) |
| Why is this file here / why is it unused? | [02-architecture.md](02-architecture.md) (legacy artifacts) |
| What are the rules I must follow? | [05-conventions.md](05-conventions.md) and `AGENTS.md` |
| What is the current state / what's next? | "Current state" above and [08-roadmap-and-open-questions.md](08-roadmap-and-open-questions.md) |
