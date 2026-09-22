# 4. Frontend and Styling

## Template chain

Every page extends `base/_base_index.html` and only fills two blocks:

```
base/_base_index.html
├── {% block title %}            ← page title (browser tab)
├── includes _base_head.html     ← meta tags, icons, CSS (Bootstrap, icons, my_styles)
├── includes _base_sidebar.html  ← the fixed left sidebar with the document menu
├── includes _messages.html      ← Django messages (Bootstrap alerts)
├── {% block body_content %}     ← the actual page content
└── includes _base_script.html   ← bootstrap.bundle.min.js + my_scripts.js
```

| Partial | Purpose |
|---------|---------|
| `_base_head.html` | Meta tags (some legacy SEO tags with TODOs), favicon, Bootstrap 5 CSS, bootstrap-icons, `my_styles.css`, cookie-consent CSS from CDN |
| `_base_sidebar.html` | Sidebar menu: "Página Inicial" and one entry per document type (see the index in [README.md](README.md#implemented-document-types)). Admin/logout entries are commented out |
| `_messages.html` | Renders Django `messages` as dismissible Bootstrap alerts (`error` maps to `danger`) |
| `_base_script.html` | Loads `my_scripts.js` then `bootstrap.bundle.min.js` |

Pages are filled by Django templates and tags only — there is no build step,
no bundler, no npm. Bootstrap is vendored in `base/static/base/css/` and
`base/static/base/js/`.

## Styling strategy (`base/static/base/css/my_styles.css`)

The project CSS is organized in **scoped sections**, one per module:

```
:root                      → brand palette
Base Layout                → sidebar, buttons, badges (store-system legacy)
.receipt-page              → legacy sale-receipt styles (kept, unused today)
.contract                  → the contract form page styles
.contract-pdf              → the PDF document styles (print)
```

Rules:

- Brand colors: `--primary-color: #004F9F` (blue), `--secondary-color: #FBB900`
  (yellow). Sidebar and `.btn-primary` use them.
- **New modules append a new scoped section at the end of the file**, following
  the `.receipt-page` / `.contract` pattern. Never interleave styles into other
  sections.
- The `.contract-pdf` section defines the print `@page` rules (A4, 2cm margins),
  a named `contract-page` page with a page counter, and the shared print
  typography. The PDF template links this stylesheet instead of carrying inline
  styles.

### The `.contract` section

Makes the form page look like a sheet of paper:

- `.contract` → `210mm × 297mm` white sheet, centered, with box shadow;
  Arial 12pt, `line-height: 1.8`.
- Inputs/textarea are borderless with only a bottom border
  (`border-bottom: 1px solid #000`, transparent background) so they read as
  blank lines of the document.
- Titles are centered (`contract-title`), clauses are left-aligned paragraphs
  — **no justified text**.
- Screen-only controls: `.clause-check` and `.signature-check` checkboxes.
  They are planned to be hidden on print (see roadmap).

### The `.contract-pdf` section

Styles for the standalone PDF templates (the actual print output):

- Arial 11pt with `line-height: 1.15`; paragraphs add `8pt` of space after
  (no space before); the centered `contract-title` has `margin-bottom: 18pt`.
- `@page` A4 with 2cm margins, plus the `contract-page` named page and its page
  counter footer.
- Pagination guards: `break-inside: avoid` on `.clause`, `.signatures`,
  `.signature-columns`, and `.signature`; `break-after: avoid` on the
  `.contract-place-date` line. Templates must wrap the signature area (place
  date plus every signature row) in `<div class="signatures">` so it is never
  split across pages.

## JavaScript (`base/static/base/js/my_scripts.js`)

Current state is mostly legacy and partially inert:

- jQuery-based scroll-to-top and cookie-consent code — note that **jQuery is
  not loaded** by `_base_script.html` today, so this code does not run.
- `hide_contact_form()` / AJAX contact-form code — tied to the legacy footer
  form, unused.
- Vanilla JS mobile-navbar toggle code (`#navbar`) — no matching markup in the
  current base template, inert.

Planned for this file: a small module to toggle contract clauses/signature
blocks on/off when their checkboxes change (see
[08-roadmap-and-open-questions.md](08-roadmap-and-open-questions.md)).

## Content rules for user-facing HTML

All user-facing text is Brazilian Portuguese (pt-BR). For contract content:

- Font: **Arial only** (never serif).
- Dates as `DD/MM/YYYY`, currency as `R$`.
- Left-aligned paragraphs, never justified.
- No law/article citations and no fixed percentages in the contract text.
- Keep "DETRAN" generic — no state-specific references (e.g. "DETRAN-PA").

For a full list of language rules, see [05-conventions.md](05-conventions.md).
