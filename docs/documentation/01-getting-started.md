# 1. Getting Started

## What is this project?

**Document Automation** is a web application that generates legal documents
(contracts and similar paperwork) as downloadable PDFs.

The user opens a document page (e.g. a vehicle purchase and sale contract),
fills in a form rendered like the final paper document, optionally unchecks
clauses and signature blocks they want to exclude, and submits. The backend
renders the filled document to HTML and converts it to PDF with WeasyPrint.

**Key principle: nothing is persisted.** Document templates and the data
entered in forms live only in memory for the duration of the request and are
discarded after the PDF is generated. The only files written to disk are the
generated PDFs (see [03-dashboard-and-contract-flow.md](03-dashboard-and-contract-flow.md)).

## Prerequisites

- Python 3.12+ (deployment pins `python-3.12.12` via `runtime.txt`; the
  project has also been run locally on Python 3.13).
- A virtual environment (`.venv/` is used locally).
- The system libraries required by WeasyPrint on your OS
  (Pango, cairo, etc. — see the
  [WeasyPrint install docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation)
  if PDF generation fails on import).

## Install

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file at the project root (see `.env.example` for the expected
variable names — **never** commit real values, and **never** read or expose
the contents of `.env`).

Variables read by `config/settings.py`:

| Variable | Used when | Purpose |
|----------|-----------|---------|
| `SECRET_KEY` | always | Django secret key |
| `DEBUG` | always | `"True"`/`"False"` — switches development vs production behavior |
| `ALLOWED_HOSTS` | `DEBUG=False` | Allowed host for production |
| `TRUSTED_ORIGINS` | `DEBUG=False` | CSRF trusted origins |
| `DATABASE_URL` | always | Connection string consumed by `dj-database-url` (SQLite locally, PostgreSQL in production) |

## Run the development server

```bash
python manage.py runserver
```

Then open the home page. The routes registered today:

| Path | Name | Purpose |
|------|------|---------|
| `/` | `dashboard` | Home page (`dashboard/templates/dashboard/index.html`) |
| `/contract-sale-vehicle/` | `contract_sale_vehicle` | Vehicle purchase and sale contract form |
| `/admin/` | — | Django admin |

> Note: URL `name`s always match their template names
> (e.g. `contract_sale_vehicle` — see [05-conventions.md](05-conventions.md)).

## Database

There are **no project models or migrations** — the database is only used by
Django's built-in apps (admin, auth, sessions, etc.). Local development uses
SQLite through `DATABASE_URL`. Never open, read, or modify the SQLite file
directly.

## Quick smoke test

1. Run the server and open `/contract-sale-vehicle/`.
2. Fill in a few fields, leave the checkboxes checked.
3. Click **Gerar PDF**.
4. A PDF is downloaded and a copy is saved under
   `contract_files/created_contracts/`.
