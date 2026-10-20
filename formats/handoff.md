# Format: handoff (version 1)

## Purpose

The contract between upstream onboarding/sales and this repository. A single Markdown handoff file (plus an optional sibling folder of files such as `order-form.pdf` and assets) carries everything `setup-client` needs to build a complete `clients/<slug>/` directory without reading Slack, email, Google Drive, or chat history. Anything upstream could not settle goes into the `# Open Issues` chapter of the handoff, never into an undocumented gap.

## Location

Supplied as an input path to `setup-client` (for example from `tmp/handoff/<slug>.md`). Never committed to the repository.

## Header

The standard YAML header defined in `formats/README.md` with `format: handoff`, `format_version: 1`, `client` set to the target client slug, and `created_by` / `updated_by` set to the upstream author's or operator's email address.

## Body

One `#` chapter per client document format, in this order. Each chapter holds the matching client format's body shifted down one heading level (the format's `#` headings become `##`, its `##` headings become `###`, and so on):

| Chapter | Produces | Governing format |
| --- | --- | --- |
| `# Client` | `clients/<slug>/client.md` | `formats/client.md` |
| `# Open Issues` | `clients/<slug>/open-issues.md` | `formats/open-issues.md` |

When `create-application` adds domain-specific client document formats, it adds a corresponding chapter row to this table and updates `scripts/check.py`.

```markdown
---
title: Acme Corp — Handoff
format: handoff
format_version: 1
client: acme-corp
created: 2026-10-20
created_by: founder@company.com
updated: 2026-10-20
updated_by: founder@company.com
---

# Client
## General Information
### Name
Acme Corp
### Organization
Acme Corporation
### Website
https://example.com
### Time Zone
America/New_York
### Engagement Started
2026-10-20
### Contact
- Name: Jane Doe
- Email: jane@example.com
## Business Overview
...
## Business Problem
...
## Solution
...
## Entitlements
### Order Form
None
### Plan Name
Standard
### Starts
2026-10
### Renews
2027-10-20
### Deliverables
None
## Notes
None

# Open Issues
## Open
None
## Closed
None
```

## Rules

- Every required chapter must be present in order.
- Every section required by a chapter's governing format must be filled or hold `None` (with a matching row in `# Open Issues` or raised onto the Setup Ledger by `setup-client`).
- Any file path referenced by the handoff (such as `<slug>/order-form.pdf`) must exist in the sibling folder beside the handoff file.
- The handoff carries no credentials, API keys, or unredacted payment card/bank numbers.

## Vocabularies

Uses the vocabularies defined in each chapter's governing format contract (`formats/client.md`, `formats/open-issues.md`, and any domain client formats).

## Checks

- `python3 scripts/check.py --handoff <path>` validates the handoff before `setup-client` writes anything: standard header with `format: handoff` and `format_version: 1`, required chapters in order, and each chapter (shifted up one heading level) passing its governing format's checks.
