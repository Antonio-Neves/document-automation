# 7. Deployment

## Runtime

- **Python**: `runtime.txt` pins `python-3.12.12` for the deployment platform.
- **Server**: `gunicorn` (also `waitress` is in requirements as an
  alternative; `asgiref`/`wsgi` are standard Django companions).
- **Database**: PostgreSQL via `DATABASE_URL` in production (`ssl_require=True`).

## `Procfile`

```
release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn config.wsgi --preload --log-file -
```

- The `release` step runs migrations (Django built-in apps only — the project
  has no models of its own) and collects static files.
- Static files are served by **WhiteNoise** (configured in the middleware
  stack of `config/settings.py`).

## Development vs production (`config/settings.py`)

Behavior is switched by the `DEBUG` environment variable (`"True"` /
`"False"`):

| Setting | `DEBUG=True` (dev) | `DEBUG=False` (prod) |
|---------|--------------------|----------------------|
| `ALLOWED_HOSTS` | empty | from `ALLOWED_HOSTS` env var |
| Database | `DATABASE_URL` via `dj-database-url`, `conn_max_age=600` | same + `ssl_require=True` |
| Cookies | default | `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` |
| CSRF origins | — | `CSRF_TRUSTED_ORIGINS` from `TRUSTED_ORIGINS` env var |
| SSL redirect | — | commented out (enable when the platform terminates TLS) |

## Generated PDFs

Generated files accumulate in `contract_files/created_contracts/`
(one per submission). The README states a retention policy (generated PDFs are
kept for 10 days and then deleted) — an automatic cleanup mechanism is not
implemented yet.

## Environment variable checklist (production)

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `TRUSTED_ORIGINS`
- `DATABASE_URL` (PostgreSQL with SSL)

See [01-getting-started.md](01-getting-started.md) for the full variable
reference. Never commit real values to the repository.
