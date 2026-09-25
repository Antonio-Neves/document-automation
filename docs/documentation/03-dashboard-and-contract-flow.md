# 3. Dashboard and Contract Flow

This chapter describes how document pages work end to end. The whole pipeline —
one class-based view, one page template, one PDF template, one route — is common
to every document type, and the vehicle purchase and sale contract ("Contrato
Particular de Compra e Venda de Veículo Automotor") is the simplest reference
for it. A document type may add its own variations on top of the common pattern:
alternative sections, optional sub-blocks, and extra signature rows (the
property contract is the current example). The authoritative list of types is
the index in [README.md](README.md#implemented-document-types); this chapter
documents the **shared pattern once**.

## Views (`dashboard/views.py`)

- **`IndexView`** — plain `TemplateView` for the home page
  (`dashboard/index.html`).
- **`ContractPdfView`** — shared base `TemplateView` holding the whole
  GET/POST pipeline (`get_context_data`, `post`, `_pdf_filename`) once, so no
  document type repeats it.
- **`ContractSaleVehicleView`** — concrete `ContractPdfView` subclass for the
  vehicle contract. Every document type has its own subclass like this one —
  see the index in
  [README.md](README.md#implemented-document-types) for the concrete names.
  There is **no** generic/slug-driven view: one class per document type.

Each concrete view only sets class attributes:

| Attribute | Value |
|-----------|-------|
| `template_name` | `dashboard/contract_sale_vehicle.html` (form page) |
| `pdf_template_name` | `dashboard/contract_sale_vehicle_pdf.html` (document to convert) |
| `pdf_filename_prefix` | `'contract_sale_vehicle'` (base of the saved/downloaded filename) |
| `page_title` | `'Veículo Completo'` (shown in the browser tab) |

`get_context_data()` only adds `page_title`. There are no model forms — the
form is plain HTML inside the template.

## The two templates per document type

Every document type uses **two sibling templates**:

1. **Page template** (`contract_sale_vehicle.html`) — what the user sees.
   It renders the contract layout with real form controls:
   - `<input type="text" name="...">` for single-line fields,
   - `<textarea name="..." rows="2">` for long free-text fields,
   - `<input type="checkbox" class="clause-check|signature-check">` bound to a
     `{% if fields.include_... %}` block in the PDF template. A checked box
     (the default for clauses and signatures) keeps the block — *opt-out*; an
     unchecked box omits it — *opt-in*, used for optional sub-blocks.
   Field `name` attributes are in English and are the contract between the form
   and the PDF template (e.g. `seller_name`, `vehicle_plate`, `price`).

2. **PDF template** (`contract_sale_vehicle_pdf.html`) — pure print HTML, no
   form controls. It receives `fields` (a dict of POST values) and fills them
   with the `fill` template filter. It links the project stylesheet
   (`base/css/my_styles.css`), whose `.contract-pdf` section provides the
   `@page` rules (A4, 2cm margins, page counter) and the shared print
   typography (Arial 11pt, `line-height: 1.15`, space after paragraphs).
   Pagination guards keep clauses and signature blocks from splitting across
   pages; the whole signature area (the place-date line plus every signature
   row) is wrapped in a `<div class="signatures">` so it always stays on a
   single page.

Input widths in the page template use `ch` units matching the original
document's underscore count (e.g. name = `52ch`, address = `70ch`), so the
on-screen layout mirrors the final paper layout.

## POST → PDF pipeline (`ContractPdfView.post`)

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

`_pdf_filename()` (defined once in `ContractPdfView`) produces
`<pdf_filename_prefix>_<YYYYMMDD_HHMM>.pdf` using `timezone.localtime()`
(America/Sao_Paulo). Example (`pdf_filename_prefix = 'contract_sale_vehicle'`):

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

## Optional sections and checkboxes

Checkboxes drive every conditional block, both at the top level (whole clauses
and signatures) and inside a clause (optional details and alternative variants).

- Page template: each clause has
  `<input type="checkbox" name="include_clause_N" class="clause-check" checked>`
  and each signature block has
  `<input type="checkbox" name="include_signature_seller" class="signature-check" checked>`
  (buyer, witnesses, and the spouse rows in the property contract follow the
  same pattern).
- PDF template: the bound block is wrapped in
  `{% if fields.include_clause_N %} ... {% endif %}` (or the signature
  equivalent). Unchecked boxes simply do not exist in POST, so the `{% if %}`
  fails and the block is omitted from the PDF.
- Defaults: clauses and signatures ship `checked` (opt-out — included unless
  the user unchecks them). Optional inner details can ship unchecked (opt-in)
  instead, e.g. the property contract's complement, neighborhood, built-area
  variant, and installment paragraph.
- Alternative variants: mutually exclusive blocks are plain sibling `{% if %}`
  blocks, each bound to its own checkbox. The property contract uses this for
  the object described in the first clause (land only vs. built property).
- The checkboxes are screen-only controls and are planned to be hidden on
  print (see roadmap).

## Field naming conventions

All form fields are snake_case English names, grouped by entity:

| Prefix | Meaning | Example fields |
|--------|---------|----------------|
| `seller_*` | Seller identification | `seller_name`, `seller_cpf`, `seller_marital_status`, `seller_city` |
| `buyer_*` | Buyer identification | `buyer_name`, `buyer_rg`, `buyer_profession`, `buyer_state` |
| `vehicle_*` | Vehicle description | `vehicle_type`, `vehicle_plate`, `vehicle_renavam` |
| `property_land_*` | Property object — land | `property_land_address`, `property_land_area`, `property_land_front_measure` |
| `property_built_*` | Property object — built property | `property_built_address`, `property_built_area`, `property_built_contents` |
| `payment_*` | Price and payment | `price`, `price_in_words`, `down_payment`, `installments_count`, `first_due_date` |
| `delivery_*` | Delivery data | `delivery_day`, `delivery_time`, `delivery_place` |
| `known_*` | Disclosed debts/defects | `known_debts`, `known_defects` |
| `place_*` | Signature place/date line | `place_city`, `place_day`, `place_month` |
| `forum_*` | Jurisdiction clause | `forum_city`, `forum_state` |
| `include_*` | Checkboxes for optional blocks | `include_clause_1`, `include_clause_1_land_complement`, `include_signature_seller_spouse` |

## Routing (`dashboard/urls.py`)

```python
urlpatterns = [
    path('', views.IndexView.as_view(), name='dashboard'),
    path(
        'contract-sale-vehicle/',
        views.ContractSaleVehicleView.as_view(),
        name='contract_sale_vehicle',
    ),
    path(
        'contract-sale-property/',
        views.ContractSalePropertyView.as_view(),
        name='contract_sale_property',
    ),
]
```

Rules: URL path in kebab-case, URL `name` **equal** to the template name, one
CBV per document type. Adding a document type = adding one block here — see
[06-adding-a-new-document-type.md](06-adding-a-new-document-type.md).
