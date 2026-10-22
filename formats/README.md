# Formats — shared conventions

Every governed document in this repository conforms to one format contract in this directory. Contracts live in two namespaces:

- `formats/system/` governs repository-wide files, including root `AGENTS.md`, process documents, and the records in `system/`.
- `formats/clients/` governs files in `clients/<slug>/` and the incoming handoff that creates them.

The format identifier is the contract path relative to `formats/` without `.md`. A user registry declares `format: system/users`. A client profile declares `format: clients/client`. Identifiers are globally unique.

## The formats

| Format | Governs | Header Style | One per |
| --- | --- | --- | --- |
| [`system/global-context.md`](system/global-context.md) | Root `AGENTS.md` | `# AGENTS.md — global context (version N)` | repository |
| [`system/process.md`](system/process.md) | `process/<slug>.md` | `# Process: <slug> (version N)` | business process |
| [`system/users.md`](system/users.md) | `system/users.md` | System header | repository |
| [`system/user-roles.md`](system/user-roles.md) | `system/user-roles.md` | System header | repository |
| [`system/client-assignments.md`](system/client-assignments.md) | `system/client-assignments.md` | System header | repository |
| [`system/external-systems.md`](system/external-systems.md) | `system/external-systems.md` | System header | repository |
| [`system/application-backlog.md`](system/application-backlog.md) | `system/application-backlog.md` | System header | repository |
| [`system/question-journal.md`](system/question-journal.md) | `system/question-journal.md` | System header | repository |
| [`clients/client.md`](clients/client.md) | `clients/<slug>/client.md` | Client header | client |
| [`clients/open-issues.md`](clients/open-issues.md) | `clients/<slug>/open-issues.md` | Client header | client |
| [`clients/decision-log.md`](clients/decision-log.md) | `clients/<slug>/decision-log.md` | Client header | client |
| [`clients/handoff.md`](clients/handoff.md) | Incoming onboarding handoff file (never stored in the repository) | Client header | client, at setup |

When `setup-application` or `improve-process` adds a document type, the contract goes under `formats/system/` or `formats/clients/` according to the files it governs, and this table gains a row in the same change.

Each format file has the same shape: **Purpose**, **Location**, **Header**, **Body**, **Rules**, **Vocabularies**, and **Checks**.

## The system header

Every governed document under `system/` opens with this YAML front matter and nothing more:

| Key | Type | Required | Meaning |
| --- | --- | --- | --- |
| `title` | text | yes | Human title of the registry, for example `Users` |
| `format` | text | yes | Namespaced format identifier, for example `system/users` |
| `format_version` | integer | yes | The version in that format file's title line |
| `created` | date | yes | `YYYY-MM-DD` |
| `created_by` | email | yes | The human operator's email address |
| `updated` | date | yes | Date of the last material edit |
| `updated_by` | email | yes | Email address of the human operator who made that edit |

```yaml
---
title: Users
format: system/users
format_version: 1
created: 2026-10-22
created_by: founder@company.com
updated: 2026-10-22
updated_by: founder@company.com
---
```

System records do not carry a `client` key.

## The client header

Every governed document under `clients/<slug>/`, and every handoff, opens with the system header keys plus `client` immediately after `format_version`:

| Key | Type | Required | Meaning |
| --- | --- | --- | --- |
| `client` | text | yes | The client slug; equals the folder name under `clients/<slug>/` |

```yaml
---
title: Acme Corp
format: clients/client
format_version: 2
client: acme-corp
created: 2026-10-22
created_by: founder@company.com
updated: 2026-10-22
updated_by: founder@company.com
---
```

A format may add `status` only when its Header section says so. Actor values (`created_by`, `updated_by`) are always a human email address.

## Body rules

- The body starts at heading level one (`#`). A **single-record** document's sections are `#` headings in the exact order its format lists. Fields under a section are `##` headings, with the value as the section's text, and `None` where there is no value.
- A **multi-record** document uses `#` for each record's name and shifts the format's sections down one heading level. When the registry has no records, the body is the single line `None`.
- No headings beyond those the format lists, except where the format says a heading is a record's or stage's own name.
- A required section with nothing to say holds the single line `None`. Never delete a required section.
- Short repeated items use a Markdown table with the exact column headers the format gives. An empty table cell is `—`.
- Dates are `YYYY-MM-DD`. Months are `YYYY-MM`. Yes/no in a table cell is `yes` or `no`.

## References

- **A format** is referenced by its namespaced identifier (`system/users`, `clients/open-issues`).
- **A file** is referenced by its slug (the filename without `.md`) when the format says to use a slug. Paths are written out when the format asks for a repository path.
- **A record inside a multi-record file** is referenced by its heading text exactly. User records are referenced by email. Role records are referenced by slug. Assignments are referenced by `A-NNNN`. Backlog items are referenced by `APP-NNNN`.
- **A vocabulary value** is written as the Display Name exactly as the governing format's table lists it.
- Client business documents never reference another client folder. `system/client-assignments.md` may store a client slug as routing metadata and nothing else about that client.

## What `scripts/check.py` enforces everywhere

- Root `AGENTS.md` conforms to `formats/system/global-context.md`.
- Every process document in `process/` conforms to `formats/system/process.md`, including stage structure and skill references.
- Every format contract under `formats/system/` and `formats/clients/` is discovered, and its title identifier matches its relative path.
- Every governed data document has a complete, typed YAML header whose `format` names a contract here and whose `format_version` matches that contract's current version.
- System documents omit `client`. Client documents include `client`.
- Body headings match the governing format in order and heading level.
- Vocabulary values match Display Names from the governing format's tables.
- References among users, roles, assignments, clients, processes, skills, external-system owners, backlog dependencies, issues, and decisions resolve.
- Directory inventories (`docs/README.md`, `process/README.md`, `formats/README.md`, `system/README.md`, `.agents/skills/README.md`, `scripts/README.md`) match the files on disk in both directions.
- In a staged git diff (`--staged`), `updated` and `updated_by` changed on every modified governed data document.
