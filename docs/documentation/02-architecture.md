# 2. Architecture

## Directory layout

```
document_automation/
├── base/                        # Shared layout, templates, static files
│   ├── static/base/
│   │   ├── css/                 # Bootstrap 5, bootstrap-icons, my_styles.css
│   │   ├── images/              # Favicon, logos (legacy branding)
│   │   └── js/                  # bootstrap.bundle.min.js, my_scripts.js
│   └── templates/base/          # _base_index.html and partials
├── config/                      # Django project
│   ├── settings.py              # DEBUG vs production split
│   └── urls.py                  # admin + dashboard.urls + media
├── contract_files/
│   ├── created_contracts/       # Generated PDFs (one per submission)
│   └── models/                  # Reference originals (.docx/.pdf/.txt, in pt-BR)
├── dashboard/                   # Document pages and PDF generation
│   ├── templates/dashboard/     # Page + PDF templates per document type
│   ├── templatetags/            # contract_filters.py (fill filter)
│   ├── urls.py                  # One route per document type
│   └── views.py                 # One CBV per document type
├── docs/
│   ├── summary.md               # AI-oriented, always-current project summary
│   └── documentation/           # This documentation set (for humans)
├── utils/
│   ├── pages_photos/            # Screenshots of the original document model
│   └── tasks/                   # Task tickets registered from "#" prompts
├── manage.py
├── requirements.txt
└── .env / .env.example          # Environment variables (never commit real values)
```

## Apps and responsibilities

| App / module | Responsibility |
|--------------|----------------|
| `config` | Project settings and root URLconf. Environment-driven (`DEBUG` toggles dev vs production). |
| `base` | Shared UI: base template, sidebar, messages, Bootstrap 5 assets, project CSS/JS. **No views or models in use.** |
| `dashboard` | The product itself: home page and one CBV per document type, plus the WeasyPrint PDF flow. |
| `contract_files` | Not a Django app. Holds the reference originals (input) and the generated PDFs (output). |
| `utils` | Supporting material: reference screenshots and the `#` task-registration files. |

## Request flow

```
Browser
   │  GET /contract-sale-vehicle/
   ▼
config/urls.py ──► dashboard/urls.py (name='contract_sale_vehicle')
   ▼
dashboard/views.py — ContractSaleVehicleView (TemplateView)
   │  renders dashboard/contract_sale_vehicle.html
   │  (extends base/_base_index.html: sidebar + content + scripts)
   ▼
Form page with inline <input>/<textarea>/<checkbox> fields
   │
   │  POST /contract-sale-vehicle/ (all form fields, stripped)
   ▼
ContractSaleVehicleView.post()
   │  1. Strips every POST value
   │  2. render_to_string('dashboard/contract_sale_vehicle_pdf.html', {'fields': ...})
   │  3. WeasyPrint HTML(string=..., base_url=request.build_absolute_uri('/'))
   │  4. Saves a copy: contract_files/created_contracts/<type>_<YYYYMMDD_HHMM>.pdf
   │  5. Returns the PDF bytes as an attachment download
   ▼
Browser downloads the PDF
```

## Settings highlights (`config/settings.py`)

- **DEBUG split**: with `DEBUG=True` the app runs with empty `ALLOWED_HOSTS`;
  with `DEBUG=False` it loads `ALLOWED_HOSTS`, `TRUSTED_ORIGINS`, and enforces
  secure session/CSRF cookies (SSL redirect is commented out).
- **Database**: no hard-coded engine — the connection string comes from
  `DATABASE_URL` via `dj-database-url` (SSL required in production).
- **Localization**: `pt-br` language, `America/Sao_Paulo` timezone. Always
  respect these when formatting dates/currency manually.
- **Static**: `STATIC_ROOT` → `staticfiles/`, `MEDIA_ROOT` → `media/`;
  WhiteNoise is in the middleware stack for serving static files.

## Legacy artifacts — read before you "clean up"

The `base` app was inherited from a store management system. You will find
leftovers that are **not used** by the document workflow but are kept on
purpose:

- `base/templates/base/_base_footer.html` — an old "Get in touch" footer.
- `my_scripts.js` — legacy jQuery scroll-to-top, cookie-consent, contact-form
  AJAX, and mobile-navbar code (jQuery itself is *not* loaded by the current
  base script partial, so some of this code is inert).
- `my_styles.css` — contains the legacy `.receipt-page` scoped section and
  store branding colors (`--primary-color: #004F9F`,
  `--secondary-color: #FBB900`) that are still used by the sidebar/buttons.
- SEO/meta tags in `_base_head.html` still reference the old store system
  (marked with TODOs).
- `base/models.py`, `base/views.py`, `dashboard/models.py` are empty scaffolds.

**Do not remove, rename, or repurpose these files** just because they look
unused. The codebase is evolving rapidly and these artifacts may be adapted
later. See [05-conventions.md](05-conventions.md).
