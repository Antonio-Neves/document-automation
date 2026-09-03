# Project Resume

> Read this file at the start of every chat, before working on any task.
> General rules live in `AGENTS.md`; this file shows the project direction, current state, and module conventions.

## What the project is

- Document generator (contracts and other documents).
- Fills HTML templates with data entered in a form and generates a downloadable PDF.
- No document templates or form data are persisted — everything is used in memory per request and discarded after the PDF is generated.
- The only planned exception: generated PDFs will be saved in a future `created_docs` folder (kept for 10 days, then deleted).

## Tech stack

- Backend: Django 5.2, Python 3.12
- Database: SQLite
- Frontend: Django templates and tags, Bootstrap 5, HTML, CSS, JavaScript
- PDF generation: WeasyPrint (not yet in `requirements.txt`)

## Current state (Sep 2026)

- Early phase: no contracts app/views yet; `config/urls.py` only routes admin.
- The `base` app layout was inherited from a store management system (sidebar, receipt CSS, "Sistema de Gestão de Loja" branding). Keep these artifacts — the codebase is evolving rapidly; do not remove or repurpose files just because they look unused.
- First document type: vehicle purchase and sale contract ("Contrato Particular de Compra e Venda de Veículo Automotor").

## Where it's going

1. Form page collects contract data (in memory only).
2. Page includes the contract fragment (Django include) inside a `<form>`.
3. On submit, the HTML is rendered and converted to PDF with WeasyPrint for download.
4. Checkboxes per clause and per signature block allow excluding sections from the document.
5. Print-empty mode: an empty contract prints with underscore lines so the client can fill it by hand.
6. Page breaks will be tuned later for a clean A4 print (`break-inside: avoid` on `.clausula`/`.assinatura`, `@page` rules, checkboxes hidden on print).

## Key locations

- `contracts/models/` — reference originals (`.docx`, `.pdf`, `.txt`) plus the generated HTML fragment `contrato_compra_venda_veiculo.html`.
- `base/static/base/css/my_styles.css` — project styles; new modules add a scoped section at the end (pattern: `.receipt-page`, `.contrato`).
- `utils/tasks/` — task tickets registered from `#` prompts (see AGENTS.md); never executed, just registered.

## Contract fragment conventions (`contrato_compra_venda_veiculo.html`)

- Root: `<div class="contrato" id="contrato-compra-venda-veiculo">`; fragment only — no `<html>/<head>/<body>` and no `<form>` (the including page provides it).
- Each clause: `<div class="clausula" id="clausula-N">` (1 to 11) with `<h2 class="clausula-titulo">`.
- Signature blocks: independent divs `#assinatura-vendedor`, `#assinatura-comprador`, `#testemunha-1`, `#testemunha-2`.
- Toggle checkboxes (screen-only, will be hidden on print): `.clausula-check` before each clause title, `.assinatura-check` before each signature block; checked by default.
- Blank fields are `<input type="text">` (long descriptions are `<textarea rows="1">`) with `name` attributes in English (e.g. `seller_name`, `vehicle_plate`, `price`).
- Input widths use `ch` units equal to the original underscore count in the `.txt` model, so the layout matches the original document (e.g. name = 52ch, address = 70ch).
- Signature lines (including Name/CPF under each signature) remain static underscores — filled by hand.
- Content rules: pt-BR text, dates DD/MM/YYYY, currency R$; Arial only (never serif); left-aligned paragraphs (no justify); no law/article citations and no fixed percentages in the contract text.

## Provisional markup to remove

- `<meta charset="UTF-8">` and the temporary `<style>` block at the top of `contrato_compra_venda_veiculo.html` exist only for standalone browser preview; remove both once the fragment is served through Django.

## Open tasks / ideas

- Implement the contract form, views, and WeasyPrint PDF generation (add WeasyPrint to `requirements.txt`).
- JavaScript to toggle clause/signature sections via the checkboxes.
- Print CSS: hide checkboxes, page breaks, empty inputs printed as lines.
- Task ticket pending: `utils/tasks/be-change-messages-html.md`.
- Open questions: signature block Name/CPF fields may become inputs later; keep DETRAN generic (state-specific references like DETRAN-PA should stay out).
