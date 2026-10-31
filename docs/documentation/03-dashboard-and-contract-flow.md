# 3. Dashboard and Contract Flow

This chapter describes how document pages work end to end. The whole pipeline —
one class-based view, one page template, one PDF template, one route — is common
to every document type, and the simplest document type is the reference for it.
A document type may add its own variations on top of the common pattern:
alternative sections, optional sub-blocks, and extra signature rows. The
authoritative list of types is the index in
[README.md](README.md#implemented-document-types); this chapter documents the
**shared pattern once**.

## Views (`dashboard/views.py`)

- **`IndexView`** — plain `TemplateView` for the home page
  (`dashboard/index.html`).
- **`ContractPdfView`** — shared base `TemplateView` holding the whole
  GET/POST pipeline (`get_context_data`, `post`, `_pdf_filename`) once, so no
  document type repeats it.
- **`ContractSaleVehicleCompleteView`** — concrete `ContractPdfView` subclass for the
  vehicle contract. Every document type has its own subclass like this one —
  see the index in
  [README.md](README.md#implemented-document-types) for the concrete names.
  There is **no** generic/slug-driven view: one class per document type.

Each concrete view only sets class attributes:

| Attribute | Value |
|-----------|-------|
| `template_name` | `dashboard/contract_sale_vehicle_complete.html` (form page) |
| `pdf_template_name` | `dashboard/contract_sale_vehicle_complete_pdf.html` (document to convert) |
| `pdf_filename_prefix` | `'contract_sale_vehicle_complete'` (base of the saved/downloaded filename) |
| `page_title` | `'Veículo Completo'` (shown in the browser tab) |

`get_context_data()` only adds `page_title`. There are no model forms — the
form is plain HTML inside the template.

## The two templates per document type

Every document type uses **two sibling templates**:

1. **Page template** (`contract_sale_vehicle_complete.html`) — what the user sees.
   It renders the document layout with real form controls:
   - `<input type="text" name="...">` for single-line fields,
   - `<textarea name="..." rows="2">` for long free-text fields,
   - `<input type="checkbox" class="clause-check|signature-check">` bound to a
     `{% if fields.include_... %}` block in the PDF template. A checked box
     (the default for clauses and signatures) keeps the block — *opt-out*; an
     unchecked box omits it — *opt-in*, used for optional sub-blocks.
   Field `name` attributes are in English and are the interface between the
   form and the PDF template (e.g. `seller_name`, `vehicle_plate`, `price`).
   The shared content header (`base/_base_index.html`) already renders the
   action controls: the gender toggles and the **Gerar PDF** submit button.
   Page templates therefore do not define `header_actions`; the dashboard
   overrides the block with an empty one to hide the controls. The submit
   button and the radio inputs reference the form via `form="contract-form"`
   because the header sits outside the form.

2. **PDF template** (`contract_sale_vehicle_complete_pdf.html`) — pure print HTML, no
   form controls. It receives `fields` (a dict of POST values) and fills them
   with the `fill` template filter. It links the project stylesheet
   (`base/css/my_styles.css`), whose `.contract-pdf` section provides the
   `@page` rules (A4, 2cm margins, page counter) and the shared print
   typography (Arial 11pt, `line-height: 1.15`, space after paragraphs).
   Clauses are allowed to flow across pages (with `orphans`/`widows` guards
   and `break-after: avoid` on the clause title, so a heading never ends a page
   alone). Signature blocks stay intact; the whole signature area (the
   place-date line plus every signature row) is wrapped in a
   `<div class="signatures">` so it always stays on a single page.

Input widths in the page template use `ch` units matching the original
document's underscore count (e.g. name = `52ch`, address = `70ch`), so the
on-screen layout mirrors the final paper layout.

## POST → PDF pipeline (`ContractPdfView.post`)

```python
def post(self, request, *args, **kwargs):
    from weasyprint import HTML

    fields = {key: value.strip() for key, value in request.POST.items()}
    context = {
        'fields': fields,
        'first_party_gender': self._normalize_gender(
            fields.get('first_party_gender')),
        'second_party_gender': self._normalize_gender(
            fields.get('second_party_gender')),
    }

    html_string = render_to_string(
        self.pdf_template_name, context, request=request)

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
- `_normalize_gender()` returns `feminine` only when that exact value is sent;
  anything else (including a missing value) falls back to `masculine`.
- `base_url` is the absolute root URL so WeasyPrint can resolve relative
  resources (e.g. fonts/images) during rendering.
- The PDF is both **downloaded** (attachment response) and **saved** to
  `contract_files/created_contracts/`. This is the only allowed persistence.
- No data from the form is ever stored in a database or in a session.

## Gender selection in document PDFs

Document PDFs can vary party-related text by grammatical gender. This is a
shared capability, not a per-document implementation: all current and future
document types share the same controls, tag, and fallback rules. Each PDF
template opts into the tag for the party-related text that needs it.

- The shared header (`base/_base_index.html`) renders two radio groups from
  `base/_contract_header_actions.html`:
  - **1º Interveniente** → `first_party_gender`
  - **2º Interveniente** → `second_party_gender`
- Each group accepts `masculine` or `feminine`; `masculine` is checked by
  default.
- The dashboard hides the controls by overriding the block:
  `{% block header_actions %}{% endblock %}`. Any future page that is not a
  document form can do the same.
- The radio inputs use `form="contract-form"` so they submit with the form even
  though the header is outside it.
- `ContractPdfView.post()` normalizes both values and passes
  `first_party_gender` and `second_party_gender` to the PDF template.

PDF templates use the `gender` tag from `contract_filters.py`:

```django
{% gender first_party_gender "do VENDEDOR|da VENDEDORA" %}
{% gender second_party_gender "ao COMPRADOR|à COMPRADORA" %}
```

Rules:

- The pair is always `masculino|feminino`; the left side is used for
  masculine, the right side for feminine.
- Write the whole phrase inside the pair, including articles and prepositions
  (e.g. `do VENDEDOR|da VENDEDORA`, not `do|da`).
- Do not put spaces around `|`.
- Preserve the original capitalization of each occurrence.
- A pair without `|` is returned unchanged; an empty feminine side, a missing
  gender, or an invalid gender falls back to the masculine side.
- There is no grammar inference: the feminine text must be written explicitly.
  This is what keeps the result predictable across hundreds of documents.
- Text about the spouse stays neutral (`inscrito(a)`, `portador(a)`,
  `residente e domiciliado(a)`), because the spouse's gender is independent of
  the first party's gender.
- Text about objects stays neutral (e.g. `o(a) {{ vehicle_type }}`,
  `avaliado(a)`, `recebido(a)`).

When the source text comes from a `.docx`/`.txt` reference, use the conversion
markers:

- `{masculino|feminino}` → `first_party_gender`
- `[masculino|feminino]` → `second_party_gender`

The markers are not Django syntax; they are only a convention for converting
the reference text into the `{% gender ... %}` calls in the PDF template.

Per-document work is limited to the pairs in that document's `*_pdf.html`.
The controls, the tag, the normalization, and the CSS live in one shared place.

## PDF file naming

`_pdf_filename()` (defined once in `ContractPdfView`) produces
`<pdf_filename_prefix>_<YYYYMMDD_HHMM>.pdf` using `timezone.localtime()`
(America/Sao_Paulo). Example (`pdf_filename_prefix = 'contract_sale_vehicle_complete'`):

```
contract_sale_vehicle_complete_20260905_1259.pdf
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
client can fill the printed document by hand; a filled field renders its value.
The same module also defines the `gender` tag used by document PDFs (see
[Gender selection in document PDFs](#gender-selection-in-document-pdfs)).

## Optional sections and checkboxes

Checkboxes drive every conditional block, both at the top level (whole clauses
and signatures) and inside a clause (optional details and alternative variants).

- Page template: each clause has
  `<input type="checkbox" name="include_clause_N" class="clause-check" checked>`
  and each signature block has
  `<input type="checkbox" name="include_signature_seller" class="signature-check" checked>`
  (buyer, witnesses, and any extra signature rows follow the same pattern).
- PDF template: the bound block is wrapped in
  `{% if fields.include_clause_N %} ... {% endif %}` (or the signature
  equivalent). Unchecked boxes simply do not exist in POST, so the `{% if %}`
  fails and the block is omitted from the PDF.
- Defaults: clauses and signatures ship `checked` (opt-out — included unless
  the user unchecks them). Optional inner details can ship unchecked (opt-in)
  instead (e.g. a complement, neighborhood, or alternative-area paragraph).
- Alternative variants: mutually exclusive blocks are plain sibling `{% if %}`
  blocks, each bound to its own checkbox (e.g. an object described two
  alternative ways).
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
| `price_*` / `payment_*` | Price and payment | `price`, `price_in_words`, `down_payment`, `price_delivery_item`, `payment_delivery_item`, `payment_delivery_value`, `installments_count`, `first_due_date` |
| `delivery_*` | Vehicle delivery data (handover of the vehicle) | `delivery_day`, `delivery_time`, `delivery_place` |
| `known_*` | Disclosed debts/defects | `known_debts`, `known_defects` |
| `forum_*` | Jurisdiction clause | `forum_city`, `forum_state` |
| `include_*` | Checkboxes for optional blocks | `include_clause_1`, `include_clause_1_land_complement`, `include_clause_3_delivery`, `include_signature_seller_spouse` |
| `first_party_gender` / `second_party_gender` | Shared header gender selection, not document data | `masculine`, `feminine` |

> Note: the vehicle `delivery_*` prefix (handover of the vehicle) is distinct
> from the `*_delivery_*` fields inside a price/payment prefix
> (`price_delivery_item`, `payment_delivery_item`, `payment_delivery_value`),
> which describe goods handed over as (part of) the payment.

## Routing (`dashboard/urls.py`)

One `path()` entry per document type, each following the same shape:

```python
path(
    '<type-in-kebab-case>/',
    views.Contract<Type>View.as_view(),
    name='<type>',
),
```

Rules: URL path in kebab-case, URL `name` **equal** to the template name, one
CBV per document type. The authoritative list of routes is the index in
[README.md](README.md#implemented-document-types); adding a document type = one
new block here — see
[06-adding-a-new-document-type.md](06-adding-a-new-document-type.md).
