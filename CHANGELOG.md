# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-15

### Added

- Initial release of the document generator.
- Django 5.2 (LTS) on Python 3.13, with Bootstrap 5.
- PDF generation from HTML templates using WeasyPrint.
- Dashboard listing the available document types, each backed by a class-based
  view.
- In-memory form processing — no data is persisted except the generated PDFs.
- Environment-based settings for development and production (Gunicorn,
  WhiteNoise, PostgreSQL via `DATABASE_URL`).
- Developer documentation under [`docs/documentation/`](docs/documentation/).

[Unreleased]: https://gitlab.com/AntonioCalheirosNeves/document-automation/-/compare/v1.0.0...HEAD
[1.0.0]: https://gitlab.com/AntonioCalheirosNeves/document-automation/-/releases/v1.0.0
