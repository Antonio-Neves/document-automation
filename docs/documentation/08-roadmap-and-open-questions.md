# 8. Roadmap and Open Questions

This chapter lists planned work and open decisions. It is deliberately
separate from the rest of the documentation: everything here is **not yet
implemented** (or not yet decided), so treat it as a to-do board, not as a
description of the code.

## Planned (in rough order)

1. **Document form processing hardening** — the POST pipeline exists, but
   validation, required-field checks, and per-field trimming rules are minimal.
2. **JavaScript clause/signature toggling** — wire the `.clause-check` /
   `.signature-check` checkboxes to show/hide the corresponding sections live
   on the form page.
3. **Print CSS for the form page** — hide checkboxes on print, tune page
   breaks (`break-inside: avoid`), empty inputs printed as clean lines, so the
   on-screen form itself can print as a blank document ("print-empty mode").
4. **Per-document PDF layout tuning** — the shared `.contract-pdf` baseline
   (A4, 2cm margins, Arial 11pt with `line-height: 1.15`) is in place; the
   remaining work is fine-tuning each document type's template for a clean A4
   print.
5. **More document types** — the architecture is one-CBV-per-document; add
   new documents following
   [06-adding-a-new-document-type.md](06-adding-a-new-document-type.md).
6. **PDF filename collisions** — `_pdf_filename()` uses minute precision
   (`YYYYMMDD_HHMM`), so two submissions in the same minute overwrite the
   saved copy in `created_contracts/`. Add seconds or a suffix.
7. **Automatic cleanup of `created_contracts/`** — the README mentions a
   10-day retention policy; no cleanup job exists yet.
8. **Documentation pipeline** — eventually export this documentation set to a
   styled PDF (e.g. via WeasyPrint) once the project stabilizes and update
   cadence is decided.
9. **Apply gender-aware text to all document PDFs** — the shared tag, controls,
   normalization, and header are in place, but not every document template has
   been converted yet. Convert the remaining PDF templates and keep spouse and
   object terms neutral.
10. **Generalize gender selection for non-contract documents** — when the first
    non-contract document type arrives, decide where the shared `gender` tag
    lives (e.g. a `base`/`common` app), whether to introduce a shared
    `DocumentPdfView`, and how the header include handles a configurable form
    id.
11. **Scale document registration** — the current convention is one CBV, URL,
    and sidebar entry per document type. Revisit this before the number of
    document types grows enough for the boilerplate to become a maintenance
    problem.

## Pending task tickets (`utils/tasks/`)

| Ticket | Summary |
|--------|---------|
| `be-change-messages-html.md` | Change the `_messages.html` partial in `base/templates/base/` |
| `fe-chose-custom-fonts.md` | Change the fonts used in the project |

(These files are registered from `#` prompts and are intentionally
never executed by the AI workflow.)

## Open questions

- **Signature Name/CPF fields**: today they are static underscore lines filled
  by hand; they may become form inputs later so the printed PDF can include
  them.
- **Checkbox defaults**: all clauses/signatures are checked by default — is
  that the right default per document type?
- **DETRAN references**: keep them generic; do not introduce state-specific
  references (e.g. "DETRAN-PA").
- **Legacy base artifacts** (empty footer, store branding and cookie-consent CSS
  in `_base_head.html`): kept for now — decide when/if to repurpose them.
- **Form id for non-contract documents**: keep `contract-form` or standardize on
  `document-form` when the first non-contract document type arrives?
- **Spouse gender**: spouse text is neutral today; add a third gender control
  only if a document requires agreement for the spouse's own data.
- **More than two intervenients**: the shared header currently exposes two
  gender groups; decide how to extend it if a future document has more parties.
- **Shared document tags location**: keep the `gender` tag in
  `dashboard/templatetags/contract_filters.py` or move it to a shared
  `base`/`common` app when non-contract documents arrive?
- **Documentation cadence**: update docs at milestones vs. continuously — to
  be decided as the project evolves.
