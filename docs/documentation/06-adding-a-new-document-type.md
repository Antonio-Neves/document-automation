# 6. Adding a New Document Type

This is the step-by-step recipe to add a new document type (e.g. a rental
contract), following the pattern established by the vehicle sale contract.
Replace `<type>` below with a short English identifier in snake_case
(e.g. `property_rental`).

> This guide reflects the current state of the code. If the contract flow gets
> refactored (form classes, shared base view, etc.), update this guide in the
> same change.

## Step 1 — Add the reference original

Drop the source document (`.docx`, `.pdf`, `.txt`) in
`contract_files/models/` (files in Portuguese, kept as-is). Screenshots of the
original pages can go in `utils/pages_photos/`.

## Step 2 — Create the page template

Create `dashboard/templates/dashboard/<type>.html`:

- Extend `base/_base_index.html` and fill `{% block title %}` and
  `{% block body_content %}`. The shared content header already renders the
  action controls (the two gender groups and **Gerar PDF**); do **not** define
  `header_actions`.
- Wrap everything in a `<form method="post" id="contract-form">{% csrf_token %}
  ... </form>`. The shared header controls target this id with
  `form="contract-form"`.
- If a future page is not a document form, opt out of the shared actions with
  `{% block header_actions %}{% endblock %}`.
- Root content in `<div class="contract" id="contract-<type>">`.
- Each clause: `<div class="clause" id="clause-N">` with
  `<h2 class="clause-title">` and a checkbox
  `<input type="checkbox" name="include_clause_N" value="1" class="clause-check" checked>`.
- Optional inner details and alternative variants: give each its own
  `.clause-check` checkbox bound to a `{% if fields.include_... %}` block in the
  PDF template. Clauses/signatures default to `checked` (opt-out); optional
  details can default to unchecked (opt-in). Some document types show both
  styles — see
  [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md#optional-sections-and-checkboxes).
- Signature blocks: `<div class="signature" id="signature-seller">`,
  `#signature-buyer`, `#witness-1`, `#witness-2` (or your own set, e.g. an
  extra `#signature-seller-spouse` row) with `.signature-check` checkboxes.
- Fields are `<input type="text" name="...">` (long free text =
  `<textarea name="..." rows="2">`) with English snake_case names grouped by
  entity (see the field-prefix table in
  [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md)).
- Input widths in `ch` units matching the original document's underscore count.
- For a non-contract document, adapt the root class/id and decide whether it
  should inherit the shared header actions or opt out with an empty
  `header_actions` block. The gender tag remains available either way.

## Step 3 — Create the PDF template

Create `dashboard/templates/dashboard/<type>_pdf.html`:

- Full standalone HTML document (not extending the base),
  `{% load contract_filters static %}`.
- `<link>` to `base/css/my_styles.css`: the `.contract-pdf` section there
  provides the `@page` rules (A4, 2cm margins, page counter) and the shared
  print typography (Arial 11pt, `line-height: 1.15`, space after paragraphs).
  Do not duplicate styles inline.
- Keep page breaks clean: wrap the signature area (the place-date line plus
  every signature row) in `<div class="signatures">`. The stylesheet applies
  `break-inside: avoid` to `.signatures`, `.signature-columns`, and
  `.signature`, and `break-after: avoid` to `.contract-place-date`, so the
  whole signature area stays together. Clauses are allowed to flow across
  pages (with `orphans`/`widows` and `break-after: avoid` on
  `.clause-title`), so a tall clause does not leave a blank page.
- Fill every field with `{{ fields.<name>|fill:<width> }}`.
- Wrap each optional block in `{% if fields.include_... %}` — whole clauses,
  signatures, optional inner details, and alternative variants alike.
- For party-related text, use the shared gender tag with explicit
  `masculino|feminino` pairs:
  `{% gender first_party_gender "do VENDEDOR|da VENDEDORA" %}` and
  `{% gender second_party_gender "ao COMPRADOR|à COMPRADORA" %}`.
  Write the whole phrase inside the pair, preserve capitalization, and do not
  put spaces around `|`.
- If the reference `.docx`/`.txt` uses conversion markers,
  `{masculino|feminino}` maps to `first_party_gender` and
  `[masculino|feminino]` maps to `second_party_gender`.
- Spouse and object terms stay neutral unless explicitly marked; do not infer
  grammar automatically. See
  [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md#gender-selection-in-document-pdfs).

## Step 4 — Add the CBV

In `dashboard/views.py`, add one class per document type. It inherits the
shared pipeline from `ContractPdfView` (defined once in the same file) and only
sets four attributes — never copy `post()` or `_pdf_filename()`:

```python
class Contract<Type>View(ContractPdfView):
    template_name = 'dashboard/<type>.html'
    pdf_template_name = 'dashboard/<type>_pdf.html'
    pdf_filename_prefix = '<type>'
    page_title = '<Menu label>'
```

Do not turn this into a single generic/slug-driven view: one class per document
type is a project convention (see
[05-conventions.md](05-conventions.md)).

## Step 5 — Add the URL

In `dashboard/urls.py`:

```python
path(
    '<type-in-kebab-case>/',
    views.Contract<Type>View.as_view(),
    name='<type>',
),
```

Remember: path kebab-case, `name` = template name.

## Step 6 — Add the sidebar link

In `base/templates/base/_base_sidebar.html`, add a `<li class="nav-item">`
with an `href="{% url '<type>' %}"` and a bootstrap icon.

The sidebar is grouped by topic: a non-clickable `<span class="nav-topic">`
header (always visible, not a collapsible menu) followed by a
`<ul class="nav flex-column sidebar-submenu">` holding the document links.
Add new document types inside the topic they belong to (e.g. under "Compra e
Venda").

Each link highlights itself when active by comparing the current URL name:
`class="nav-link{% if request.resolver_match.url_name == '<type>' %} active{% endif %}"`.

## Step 7 — Add a scoped CSS section

Append a new scoped section at the end of
`base/static/base/css/my_styles.css` for anything document-specific that the
generic `.contract` styles do not cover. Start from a copy of the `.contract`
section.

## Step 8 — Update the docs

- Add the new type to the **single index** in [README.md](README.md)
  ("Implemented document types"): type name, route, view, and menu label.
- Update [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md)
  or [02-architecture.md](02-architecture.md) only if the **pattern** changed
  (new form classes, shared base view, etc.) — never for a single new instance.

## Checklist

- [ ] Reference original in `contract_files/models/`
- [ ] Page template with `{% csrf_token %}` form, clauses, signatures; no
      `header_actions` block (inherits the shared actions)
- [ ] PDF template with `fill` filters, `{% if %}` exclusion blocks, and
      `{% gender %}` pairs for party-related text
- [ ] CBV in `dashboard/views.py`
- [ ] URL in `dashboard/urls.py` (name = template name)
- [ ] Sidebar entry
- [ ] Scoped CSS section in `my_styles.css` (if needed)
- [ ] Docs updated
- [ ] Manual smoke test: GET form → POST → PDF downloads and a copy appears in
      `contract_files/created_contracts/`
