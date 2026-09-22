---
name: add-contract-from-txt
description: Use ONLY when the user explicitly asks to add or create a new contract/document type in this project. Never trigger just because a new .txt/.docx/.pdf appears in contract_files/models/. Follows the canonical recipe in the project docs.
---

# Add a Contract from a Reference File (.txt)

## Hard rule: only run on explicit request

- **Do not create or modify anything without the user explicitly asking for it.**
- A new reference file (`.txt`, `.docx`, `.pdf`) appearing in
  `contract_files/models/` is **not** a trigger. The user will always say when a
  new contract should be created. Wait for that instruction.
- Creating a new contract means scaffolding templates, a CBV, a URL, a sidebar
  link and docs — never do it speculatively.

## Single source of truth

Follow the canonical recipe instead of repeating it here:

- **Recipe**: [docs/documentation/06-adding-a-new-document-type.md](../../../docs/documentation/06-adding-a-new-document-type.md)
  — the 8 steps and the checklist. If the recipe changes, it changes only there.
- **Working reference (sibling templates)**: use the already-implemented types
  as the pattern to mirror. The current list is the single index in
  [docs/documentation/README.md](../../../docs/documentation/README.md)
  ("Implemented document types"); read the page and PDF templates it points to
  in `dashboard/templates/dashboard/`, plus the CBVs in `dashboard/views.py`
  and routes in `dashboard/urls.py`.

## Non-negotiable: keep signatures on one page

Wrap the **place/date line plus every signature row** in a single
`<div class="signatures">` in the PDF template. `my_styles.css` applies
`break-inside: avoid` to `.signatures`, `.signature-columns` and `.signature`,
so the whole block never splits across two pages. See step 3 of the recipe.

## Conventions to enforce (from AGENTS.md)

- All code, identifiers, file names, CSS classes, ids and URL paths in English;
  all user-facing content (form labels, messages, PDF/legal text) in pt-BR.
- Class-based views only, never function-based views.
- No persistence: no models, migrations, cache or local files for templates or
  form data. Only the generated PDF is written, to
  `contract_files/created_contracts/`.
- Dates as DD/MM/YYYY, currency as R$ (e.g. R$ 1.234,56).
- Never use the terminal; never touch `.env`, SQLite files, or run Git
  operations. Ask the user to run any command and paste the output.

## Finish

Ask the user to run the manual smoke test (GET the form → POST → PDF downloads
and a copy appears in `contract_files/created_contracts/`), since the terminal
is off-limits for the agent.
