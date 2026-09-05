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

- Extend `base/_base_index.html`, fill `{% block title %}` and
  `{% block body_content %}`.
- Wrap everything in a `<form method="post">{% csrf_token %} ... </form>`
  ending with a `<button type="submit" class="btn btn-primary">Gerar PDF</button>`.
- Root content in `<div class="contract" id="contract-<type>">`.
- Each clause: `<div class="clause" id="clause-N">` with
  `<h2 class="clause-title">` and a checkbox
  `<input type="checkbox" name="include_clause_N" value="1" class="clause-check" checked>`.
- Signature blocks: `<div class="signature" id="signature-seller">`,
  `#signature-buyer`, `#witness-1`, `#witness-2` (or your own set) with
  `.signature-check` checkboxes.
- Fields are `<input type="text" name="...">` (long free text =
  `<textarea name="..." rows="1">`) with English snake_case names grouped by
  entity (see the field-prefix table in
  [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md)).
- Input widths in `ch` units matching the original document's underscore count.

## Step 3 — Create the PDF template

Create `dashboard/templates/dashboard/<type>_pdf.html`:

- Full standalone HTML document (not extending the base), `{% load contract_filters %}`.
- Inline `<style>` with `@page { size: A4; margin: 2cm; }`, Arial 12pt,
  `break-inside: avoid` on `.clause` / `.signature`.
- Fill every field with `{{ fields.<name>|fill:<width> }}`; textareas also get
  `|linebreaksbr`.
- Wrap each optional section in `{% if fields.include_... %}`.

## Step 4 — Add the CBV

In `dashboard/views.py`, add one class per document type, mirroring
`ContractSaleVehicleView`:

```python
class Contract<Type>View(TemplateView):
    template_name = 'dashboard/<type>.html'
    pdf_template_name = 'dashboard/<type>_pdf.html'
    page_title = '<Menu label>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def post(self, request, *args, **kwargs):
        # identical pipeline to ContractSaleVehicleView.post
        ...

    def _pdf_filename(self):
        timestamp = timezone.localtime().strftime('%Y%m%d_%H%M')
        return f'<type>_{timestamp}.pdf'
```

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

In `base/templates/base/_base_sidebar.html`, add a `<li class="nav-item mt-4">`
with an `href="{% url '<type>' %}"` and a bootstrap icon.

## Step 7 — Add a scoped CSS section

Append a new scoped section at the end of
`base/static/base/css/my_styles.css` for anything document-specific that the
generic `.contract` styles do not cover. Start from a copy of the `.contract`
section.

## Step 8 — Update the docs

- Add the new route to the table in [01-getting-started.md](01-getting-started.md).
- Update `docs/summary.md` (views, URLs, key locations).
- Update [02-architecture.md](02-architecture.md) and
  [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md) if the
  pattern changes.

## Checklist

- [ ] Reference original in `contract_files/models/`
- [ ] Page template with `{% csrf_token %}` form, clauses, signatures
- [ ] PDF template with `fill` filters and `{% if %}` exclusion blocks
- [ ] CBV in `dashboard/views.py`
- [ ] URL in `dashboard/urls.py` (name = template name)
- [ ] Sidebar entry
- [ ] Scoped CSS section in `my_styles.css` (if needed)
- [ ] Docs updated
- [ ] Manual smoke test: GET form → POST → PDF downloads and a copy appears in
      `contract_files/created_contracts/`
