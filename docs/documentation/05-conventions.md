# 5. Conventions

This chapter distills the project-wide rules from `AGENTS.md`. Treat this as
a checklist, not an explanation — the authoritative source is `AGENTS.md`.

## Languages

| Scope | Language |
|-------|----------|
| Code (identifiers, comments, commit messages, file names, CSS classes, HTML ids, URL slugs, form `name` attributes) | **English (US)** |
| User-facing frontend text and generated PDFs | **Brazilian Portuguese (pt-BR)** |
| Reference originals in `contract_files/models/` | Portuguese (exception to the English rule) |

Frontend copy must be natural pt-BR: prefer proper Portuguese words when they
exist (e.g. "pagamento", not "payment"), keep established borrowings
("e-mail", "software", "online"), and never use European Portuguese forms.

## Django

- **Always class-based views (CBVs)** — never function-based views.
- One CBV per document type in `dashboard/views.py`.
- URL rules (in `dashboard/urls.py`):
  - path in kebab-case (e.g. `contract-sale-vehicle/`);
  - URL `name` always equals the template name
    (e.g. `contract_sale_vehicle` ↔ `dashboard/contract_sale_vehicle.html`).
- Localization: `pt-br`, `America/Sao_Paulo` — respect these when formatting
  dates or currency manually.

## Data persistence

- **Nothing about document templates or form data is persisted.** Everything
  lives in memory for the request and is discarded after the PDF is generated.
- Do not create models or migrations for templates or form data.
- Any form of persistence (models, migrations, cache, local files) requires
  prior approval.
- The only planned exception: generated PDFs saved to `created_contracts`
  (a future folder name; currently `contract_files/created_contracts/`).

## Security and forbidden actions

- Never access, read, inspect, modify, or expose the contents of any `.env`
  file. Never suggest accessing `.env` as a solution.
- Never open, read, or modify SQLite database files (`*.sqlite3`, `*.db`, etc.).
- Never use the terminal (this applies to the AI workflow; humans of course
  run commands themselves — see [01-getting-started.md](01-getting-started.md)).
- Never perform Git operations (commits, branches, push/pull, etc.) in the AI
  workflow.

## Workflow

- Before any non-trivial task, propose a plan and wait for approval.
- Work on one task at a time; after finishing, explain what changed.
- Never guess or invent information — if the available information is
  insufficient, ask for clarification first.
- Prompts starting with `#` are **task registrations**: create a file in
  `utils/tasks/` named kebab-case from the text after `#`
  (e.g. `#be contrato tipo letra` → `utils/tasks/be-contrato-tipo-letra.md`),
  with the prompt text as a level-1 heading prefixed
  `FrontEnd - `/`BackEnd - ` (the `fe`/`be` token is removed and capitalized).
  Register only — never execute the task.

## Codebase stewardship

- The project evolves fast; significant refactoring is expected.
- **Do not remove, rename, or repurpose files or directories** just because
  they look unused, unless explicitly instructed. Legacy artifacts from the
  inherited store-management base are documented in
  [02-architecture.md](02-architecture.md).

## Styling and frontend structure

- New CSS goes in a new scoped section at the end of `my_styles.css`
  (pattern: `.receipt-page`, `.contract`).
- Contract page conventions (ids `#clause-N`, `#signature-seller`, etc.,
  `ch`-based input widths) are described in
  [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md).
- Contract content: Arial only, left-aligned, no law citations, no fixed
  percentages, dates DD/MM/YYYY, currency R$.

## Documentation

- Technical documentation (this folder) is written in English (US).
- `docs/summary.md` is read at the start of every chat for the current project
  state; keep it current when the project structure changes.
