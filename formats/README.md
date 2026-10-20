# Formats — shared conventions

Every governed document in this repository conforms to one format contract in this directory. This file holds what every format shares: the inventory of format contracts, the standard YAML header for data documents, the body heading rules, how references are written, and what `scripts/check.py` enforces everywhere.

## The formats

| Format | Governs | Header Style | One per |
| --- | --- | --- | --- |
| [`global-context.md`](global-context.md) | Root `AGENTS.md` | `# AGENTS.md — global context (version N)` | repository |
| [`process.md`](process.md) | `process/<slug>.md` | `# Process: <slug> (version N)` | business process |
| [`handoff.md`](handoff.md) | Incoming onboarding handoff file (never stored in the repository) | Standard YAML header | client, at setup |
| [`client.md`](client.md) | `clients/<slug>/client.md` | Standard YAML header | client |
| [`open-issues.md`](open-issues.md) | `clients/<slug>/open-issues.md` | Standard YAML header | client |

When `create-application` or `improve-process` adds domain-specific document types (such as plans, deliverables, personas, or catalogs), each new type gets a `formats/<name>.md` contract here and a row in the table above.

Each format file has the same shape: **Purpose**, **Location**, **Header** (where it adds to or differs from the standard header), **Body** (the sections in order, as a template, with the text under each heading saying what that section holds and the rules that apply to it), **Rules**, **Vocabularies** (the closed tables that format selects from), and **Checks** (what `scripts/check.py` enforces).

## The standard header

Every governed data document under `clients/` (and any shared catalog directory) opens with this YAML front matter and nothing more, unless its format explicitly adds `status`.

| Key | Type | Required | Meaning |
| --- | --- | --- | --- |
| `title` | text | yes | Human title of the document, e.g. `Acme Corp`, `Acme Corp — Open Issues` |
| `format` | text | yes | Governing format slug; must name a file in `formats/` |
| `format_version` | integer | yes | The version of that format this document conforms to, as stated in the format file's title line |
| `client` | text | client files | The client slug; equals the folder name under `clients/<slug>/` |
| `created` | date | yes | `YYYY-MM-DD` |
| `created_by` | email | yes | The human operator's email address; when a skill wrote the file, the operator who ran it |
| `updated` | date | yes | Date of the last material edit; changes in every commit that touches the file |
| `updated_by` | email | yes | Email address of the human operator who made that edit |

```yaml
---
title: Acme Corp
format: client
format_version: 1
client: acme-corp
created: 2026-10-20
created_by: founder@company.com
updated: 2026-10-20
updated_by: founder@company.com
---
```

Actor values (`created_by`, `updated_by`) are always a human email address—never a name, a handle, or an agent identifier.

## Body rules

- The body starts at heading level one (`#`). A **single-record** document's sections are `#` headings in the exact order its format lists. Fields under a section are `##` headings, with the value as the section's text, and `None` where there is no value.
- A **multi-record** document uses `#` for each record's name and shifts the format's sections down one heading level.
- No headings beyond those the format lists, except where the format says a heading is a record's or stage's own name.
- A required section with nothing to say holds the single line `None`. Never delete a required section.
- Short repeated items use a Markdown table with the exact column headers the format gives. An empty table cell is `—`.
- Dates are `YYYY-MM-DD`. Months are `YYYY-MM`. Yes/no in a table cell is `yes` or `no`.

## References

- **A file** is referenced by its slug (the filename without `.md`).
- **A record inside a multi-record file** is referenced by its heading text exactly.
- **A vocabulary value** is written as the Display Name exactly as the governing format's table lists it.
- References never cross client folders.

## What `scripts/check.py` enforces everywhere

- Root `AGENTS.md` conforms to `formats/global-context.md`.
- Every process document in `process/` conforms to `formats/process.md`, including stage structure and skill references.
- Every governed data document has a complete, typed YAML header whose `format` names a file here and whose `format_version` matches the format's current version.
- Body headings match the governing format in order and heading level.
- Vocabulary values match Display Names from the governing format's tables.
- Directory inventories (`docs/README.md`, `process/README.md`, `formats/README.md`, `.agents/skills/README.md`, `scripts/README.md`) match the files on disk.
- In a staged git diff (`--staged`), `updated` and `updated_by` changed on every modified data document.
