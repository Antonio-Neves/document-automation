# 8. Roadmap and Open Questions

This chapter lists planned work and open decisions. It is deliberately
separate from the rest of the documentation: everything here is **not yet
implemented** (or not yet decided), so treat it as a to-do board, not as a
description of the code.

## Planned (in rough order)

1. **Contract form processing hardening** — the POST pipeline exists, but
   validation, required-field checks, and per-field trimming rules are minimal.
2. **JavaScript clause/signature toggling** — wire the `.clause-check` /
   `.signature-check` checkboxes to show/hide the corresponding sections live
   on the form page.
3. **Print CSS for the form page** — hide checkboxes on print, tune page
   breaks (`break-inside: avoid`), empty inputs printed as clean lines, so the
   on-screen form itself can print as a blank contract ("print-empty mode").
4. **PDF layout tuning** — fine-tune `@page` rules, margins, and clause
   spacing in the PDF template for a clean A4 print.
5. **More document types** — the architecture is one-CBV-per-document; add
   new contracts following
   [06-adding-a-new-document-type.md](06-adding-a-new-document-type.md).
6. **PDF filename collisions** — `_pdf_filename()` uses minute precision
   (`YYYYMMDD_HHMM`), so two submissions in the same minute overwrite the
   saved copy in `created_contracts/`. Add seconds or a suffix.
7. **Automatic cleanup of `created_contracts/`** — the README mentions a
   10-day retention policy; no cleanup job exists yet.
8. **Documentation pipeline** — eventually export this documentation set to a
   styled PDF (e.g. via WeasyPrint) once the project stabilizes and update
   cadence is decided.

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
- **Legacy base artifacts** (footer, jQuery code, receipt CSS, store branding
  in `_base_head.html`): kept for now — decide when/if to repurpose them.
- **Documentation cadence**: update docs at milestones vs. continuously — to
  be decided as the project evolves.
