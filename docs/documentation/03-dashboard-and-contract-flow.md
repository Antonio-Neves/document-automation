# 3. Dashboard and Contract Flow

This chapter describes how document pages work end to end, using the only
document type implemented so far: the vehicle purchase and sale contract
("Contrato Particular de Compra e Venda de Veículo Automotor").

## Views (`dashboard/views.py`)

- **`IndexView`** — plain `TemplateView` for the home page
  (`dashboard/index.html`).
- **`ContractSaleVehicleView`** — `TemplateView` that handles both GET and POST
  for the vehicle contract.

Class attributes on `ContractSaleVehicleView`:

| Attribute | Value |
|-----------|-------|
| `template_name` | `dashboard/contract_sale_vehicle.html` (form page) |
| `pdf_template_name` | `dashboard/contract_sale_vehicle_pdf.html` (document to convert) |
| `page_title` | `'Veículo'` (shown in the browser tab) |

`get_context_data()` only adds `page_title`. There are no model forms — the
form is plain HTML inside the template.

## The two templates per document type

Every document type uses **two sibling templates**:

1. **Page template** (`contract_sale_vehicle.html`) — what the user sees.
   It renders the contract layout with real form controls:
   - `<input type="text" name="...">` for single-line fields,
   - `<textarea name="..." rows="1">` for long free-text fields,
   - `<input type="checkbox" class="clause-check|signature-check">` to exclude
     whole sections.
   Field `name` attributes are in English and are the contract between the form
   and the PDF template (e.g. `seller_name`, `vehicle_plate`, `price`).

2. **PDF template** (`contract_sale_vehicle_pdf.html`) — pure print HTML, no
   form controls. It receives `fields` (a dict of POST values) and fills them
   with the `fill` template filter. It carries its own inline `<style>` with
   `@page` rules (A4, 2cm margins, Arial 12pt, `break-inside: avoid` on
   clauses/signatures).

Input widths in the page template use `ch` units matching the original
document's underscore count (e.g. name = `52ch`, address = `70ch`), so the
on-screen layout mirrors the final paper layout.

## POST → PDF pipeline (`ContractSaleVehicleView.post`)

```python
def post(self, request, *args, **kwargs):
    from weasyprint import HTML

    fields = {key: value.strip() for key, value in request.POST.items()}

    html_string = render_to_string(
        self.pdf_template_name, {'fields': fields}, request=request)

    pdf_bytes = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/'),
    ).write_pdf()

    filename = self._pdf_filename()
    output_dir = settings.BASE_DIR / 'contract_files' / 'created_contracts'
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_bytes(pdf_bytes)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
```

Notes:

- The import of `weasyprint` is inside the method (lazy import).
- `base_url` is the absolute root URL so WeasyPrint can resolve relative
  resources (e.g. fonts/images) during rendering.
- The PDF is both **downloaded** (attachment response) and **saved** to
  `contract_files/created_contracts/`. This is the only allowed persistence.
- No data from the form is ever stored in a database or in a session.

## PDF file naming

`_pdf_filename()` produces `<template_prefix>_<YYYYMMDD_HHMM>.pdf` using
`timezone.localtime()` (America/Sao_Paulo). Example:

```
contract_sale_vehicle_20260905_1259.pdf
```

Note the minute-only timestamp: two submissions within the same minute
overwrite each other in `created_contracts/` (the download itself is always
correct). This is a known rough edge — see
[08-roadmap-and-open-questions.md](08-roadmap-and-open-questions.md).

## Template filter `fill` (`dashboard/templatetags/contract_filters.py`)

```python
@register.filter
def fill(value, width=20):
    """Return the field value stripped,
    or underscores of the given width if empty."""
    value = (value or '').strip()
    if value:
        return value
    return '_' * width
```

Used everywhere in the PDF template as `{{ fields.<name>|fill:<width> }}`.
An empty field renders as a run of underscores (the "print-empty" style) so the
client can fill the printed contract by hand; a filled field renders its value.
Textareas additionally use `|linebreaksbr` so line breaks survive in the PDF.

## Clause and signature exclusion

- Page template: each clause has
  `<input type="checkbox" name="include_clause_N" class="clause-check" checked>`
  and each signature block has
  `<input type="checkbox" name="include_signature_seller" class="signature-check" checked>`
  (buyer and the two witnesses follow the same pattern).
- PDF template: each section is wrapped in
  `{% if fields.include_clause_N %} ... {% endif %}` (or the signature
  equivalent). Unchecked boxes simply do not exist in POST, so the `{% if %}`
  fails and the section is omitted from the PDF.
- The checkboxes are screen-only controls and are planned to be hidden on
  print (see roadmap).

## Field naming conventions

All form fields are snake_case English names, grouped by entity:

| Prefix | Meaning | Example fields |
|--------|---------|----------------|
| `seller_*` | Seller identification | `seller_name`, `seller_cpf`, `seller_address` |
| `buyer_*` | Buyer identification | `buyer_name`, `buyer_rg` |
| `vehicle_*` | Vehicle description | `vehicle_type`, `vehicle_plate`, `vehicle_renavam` |
| `payment_*` | Price and payment | `price`, `price_in_words`, `payment_details` |
| `delivery_*` | Delivery data | `delivery_day`, `delivery_time`, `delivery_location` |
| `known_*` | Disclosed debts/defects | `known_debts`, `known_defects_details` |
| `place_*` | Signature place/date line | `place_city`, `place_day`, `place_month` |
| `forum_*` | Jurisdiction clause | `forum_city`, `forum_state` |
| `include_*` | Exclusion checkboxes | `include_clause_1`, `include_witness_2` |

## Routing (`dashboard/urls.py`)

```python
urlpatterns = [
    path('', views.IndexView.as_view(), name='dashboard'),
    path(
        'contract-sale-vehicle/',
        views.ContractSaleVehicleView.as_view(),
        name='contract_sale_vehicle',
    ),
]
```

Rules: URL path in kebab-case, URL `name` **equal** to the template name, one
CBV per document type. Adding a document type = adding one block here — see
[06-adding-a-new-document-type.md](06-adding-a-new-document-type.md).
