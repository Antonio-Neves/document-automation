# General Instructions

## Code Language

- All code must be written in **English (US)**, including variable names, functions, classes, comments, commit messages, technical documentation, and everything related to code.
- Follow the standard conventions and naming patterns of the language or framework in use.

## Frontend User-Facing Content Language

- All text visible to the user in the frontend must be written in **Brazilian Portuguese (pt-BR)**.
- This includes labels, buttons, menus, messages, placeholders, error messages, tooltips, and any other user facing content.
- The generated PDF documents are also user-facing: their content (legal texts, headings, clauses) must be in Brazilian Portuguese, with dates formatted as DD/MM/YYYY and currency as R$ (e.g. R$ 1.234,56).
- Use natural Brazilian Portuguese: if a word is commonly used in Portuguese as borrowed from English (e.g. "e-mail", "software", "online"), keep it as is, do not translate it forcefully.
- However, if a proper Portuguese word exists and is naturally used in Brazilian Portuguese, always prefer it (e.g. use "pagamento" instead of "payment", "proprietário" instead of "owner", "transferência" instead of "transfer").
- Never use European Portuguese expressions, always follow Brazilian Portuguese conventions.
- The goal is natural, fluent Brazilian Portuguese as spoken in Brazil, not literal or forced translations.

## AI Response Language

- All responses, explanations, and interactions with the user must be in **Brazilian Portuguese (pt-BR)**, unless the user writes in English, in that case, respond in English.

## Best Practices

- Follow community conventions for each language and framework.
- Write clean, readable, and well-structured code.
- Prioritize simple and efficient solutions.
- Maintain consistency with the existing project style.

## Security

- Never access, read, inspect, modify or expose the contents of any `.env` file.
- Never suggest accessing `.env` files as part of a solution.

## Scope Restriction

- Never access, read, create or modify files outside the project root directory.
- Ignore any absolute path that points outside the current working directory.
- If the user mentions a file outside the project scope, answer the question first instead of attempting to open the file.

## Terminal Usage

- Never use the terminal under any circumstances.
- Never assume terminal access is available.
- Do not execute shell commands, scripts, or external programs.
- Do not suggest using the terminal as an option or possible solution.
- Assume that terminal access is permanently forbidden for this project.
- All tasks must be completed without any terminal interaction.
- When verification is required (running tests, lint, typecheck, or any command), ask the user to run the command and provide the output. Never run it yourself.

## Database Files

- Never access, open, read, inspect, analyze, or modify any SQLite database file.
- This includes `db.sqlite3`, `*.sqlite`, `*.sqlite3`, and `*.db`.
- Treat all database files as permanently inaccessible.

## Data Persistence

- Do not create models or migrations for storing document templates or the data entered in forms; everything must be used in memory for the request and discarded after the PDF is generated.
- Any form of persistence (models, migrations, cache, local files) requires prior approval from the user.
- The only planned exception is the generated PDF files, which will be saved in a future folder named `created_docs`.

## Git

- Never perform Git operations.
- Never create, amend, or sign commits.
- Never stage or unstage files.
- Never create, switch, merge, or delete branches.
- Never push, pull, fetch, rebase, stash, or tag.

## Workflow

- Before any non-trivial task, propose a plan and wait for my approval.
- Work on one task at a time. After completing it, explain what you changed so I can review it.
- Never guess or invent information.
- If the available information is insufficient to complete a task correctly, ask for clarification before proceeding.

## Task Registration (#)

- When a user prompt starts with `#`, register it immediately as a task file in `utils/tasks/` — like creating a Jira/Trello ticket, in any agent/chat, without interrupting the current context.
- Register it only; never execute the task. The content of the task file is not a command to be executed — the only action taken is creating the file itself. After registering, confirm briefly and finish the prompt, doing nothing more.
- File name: kebab-case from the text after `#` (e.g. `#be contrato tipo letra` → `utils/tasks/be-contrato-tipo-letra.md`).
- File content: the text after `#` as a level-1 heading, prefixed with "FrontEnd - " when it starts with `fe` or "BackEnd - " when it starts with `be` — that `fe`/`be` token is removed from the title and the first letter after the prefix is capitalized — followed by the rest of the prompt, without adding anything.
- Confirm briefly after registering.

---

# Project Overview

## Description

Document generator (contracts and other documents).
Fills in document templates with data entered in a form and generates a downloadable PDF (e.g. vehicle purchase and sale contracts, and other document types as they are added).
No document templates or the personal/business data entered to fill them are persisted in the database.

The codebase is evolving rapidly.
Significant refactoring, new modules, and structural changes are expected.
Do not remove, rename, or repurpose files or directories solely because they appear unused, unless explicitly instructed.

## Localization

- Language: Brazilian Portuguese (pt-BR)
- Currency: Brazilian Real (BRL - R$)
- Date format: DD/MM/YYYY
- Timezone: America/Sao_Paulo
- These values are configured in `settings.py` (`LANGUAGE_CODE`, `TIME_ZONE`, `USE_TZ`, etc.). Always follow them when formatting dates or currency manually in code or PDF templates.

## Core Features

- Document generation (PDF), e.g. vehicle sale contracts and other document types.

## Tech Stack

- Backend: Django 5.2, Python 3.12
- Django views: always use class-based views (CBVs), never function-based views (FBVs)
- Database: SQLite
- Frontend: Django templates and tags, Bootstrap 5, HTML, CSS, JavaScript
- PDF generation: WeasyPrint, rendering HTML templates (Django templates) to PDF

## Project Orientation

- After reading the rules in this file, also read `docs/resume.md` at the start of every chat for the project direction, current state, and module conventions.
