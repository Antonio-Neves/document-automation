# Project Summary

> Read this file at the start of every chat, before working on any task.
> General rules live in `AGENTS.md`; this file shows the project direction, current state, and module conventions.

## Current state (Sep 2026)

- `config/urls.py` routes admin and includes `dashboard.urls` at the root.
- One CBV per contract in `dashboard/views.py` (currently `ContractSaleVehicleView`), served at `contract-sale-vehicle/` with `name='contract_sale_vehicle'` (URL `name` always equals the template name — see AGENTS.md).
- The `base` app layout was inherited from a store management system (sidebar, receipt CSS, "Sistema de Gestão de Loja" branding). Keep these artifacts — the codebase is evolving rapidly; do not remove or repurpose files just because they look unused.
- First document type: vehicle purchase and sale contract ("Contrato Particular de Compra e Venda de Veículo Automotor").

## Where it's going

1. Form page collects contract data (in memory only).
2. Each document type has its own page template with the contract HTML inline in `{% block body_content %}`.
3. On submit, the HTML is rendered and converted to PDF with WeasyPrint for download.
4. Checkboxes per clause and per signature block allow excluding sections from the document.
5. Print-empty mode: an empty contract prints with underscore lines so the client can fill it by hand.
6. Page breaks will be tuned later for a clean A4 print (`break-inside: avoid` on `.clause`/`.signature`, `@page` rules, checkboxes hidden on print).

## Key locations

- `contract_files/models/` — reference originals (`.docx`, `.pdf`, `.txt`, kept in Portuguese).
- `dashboard/views.py` — one CBV per contract (plus `IndexView` for the home page); each view sets `template_name` and `page_title`.
- `dashboard/urls.py` — URL `name` always matches the template name (e.g. `contract_sale_vehicle`), path in kebab-case (`contract-sale-vehicle/`).
- `dashboard/templates/dashboard/contract_sale_vehicle.html` — page template with the vehicle sale contract HTML inline.
- `base/static/base/css/my_styles.css` — project styles; new modules add a scoped section at the end (pattern: `.receipt-page`, `.contract`).
- `utils/tasks/` — task tickets registered from `#` prompts (see AGENTS.md); never executed, just registered.

## Contract page conventions (`contract_sale_vehicle.html`)

- Page extends `base/_base_index.html`; sidebar and footer come from the base/`_sidebar.html`, so the page only fills `title` and `body_content`.
- Root: `<div class="contract" id="contract-sale-vehicle">` inside `{% block body_content %}`.
- Each clause: `<div class="clause" id="clause-N">` (1 to 11) with `<h2 class="clause-title">`.
- Signature blocks: independent divs `#signature-seller`, `#signature-buyer`, `#witness-1`, `#witness-2`.
- Toggle checkboxes (screen-only, will be hidden on print): `.clause-check` before each clause title, `.signature-check` before each signature block; checked by default.
- Blank fields are `<input type="text">` (long descriptions are `<textarea rows="1">`) with `name` attributes in English (e.g. `seller_name`, `vehicle_plate`, `price`).
- Input widths use `ch` units equal to the original underscore count in the `.txt` model, so the layout matches the original document (e.g. name = 52ch, address = 70ch).
- Signature lines (including Name/CPF under each signature) remain static underscores — filled by hand.
- Content rules: pt-BR text, dates DD/MM/YYYY, currency R$; Arial only (never serif); left-aligned paragraphs (no justify); no law/article citations and no fixed percentages in the contract text.

## Open tasks / ideas

- Implement the contract form processing (POST) and WeasyPrint PDF generation (add WeasyPrint to `requirements.txt`).
- JavaScript to toggle clause/signature sections via the checkboxes.
- Print CSS: hide checkboxes, page breaks, empty inputs printed as lines.
- Task ticket pending: `utils/tasks/be-change-messages-html.md`.
- Open questions: signature block Name/CPF fields may become inputs later; keep DETRAN generic (state-specific references like DETRAN-PA should stay out).
