# Format: clients/handoff (version 2)

## Purpose

The contract between upstream onboarding and this repository. A single Markdown handoff file, plus an optional sibling folder of files such as `order-form.pdf`, carries everything `setup-client` needs to build a complete `clients/<slug>/` directory. Anything upstream could not settle goes into the `# Open Issues` chapter, never into an undocumented gap.

## Location

Supplied as an input path to `setup-client` (for example `tmp/handoff/<slug>.md`). Never committed to the repository. The format identifier is `clients/handoff`.

## Header

The client header defined in `formats/README.md` with `format: clients/handoff`, `format_version: 2`, `client` set to the target client slug, and `created_by` / `updated_by` set to the upstream author's or operator's email address.

## Body

One `#` chapter per client document, in this order. Each chapter holds the matching client format's body shifted down one heading level (the format's `#` headings become `##`, its `##` headings become `###`, and so on):

| Chapter | Produces | Governing format |
| --- | --- | --- |
| `# Client` | `clients/<slug>/client.md` | `clients/client` |
| `# Open Issues` | `clients/<slug>/open-issues.md` | `clients/open-issues` |
| `# Decision Log` | `clients/<slug>/decision-log.md` | `clients/decision-log` |

When `setup-application` adds domain-specific client document formats, it adds a corresponding chapter row to this table and updates `scripts/check.py`.

```markdown
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

# Decision Log
## Decisions
None
```

## Rules

- Every required chapter must be present in order.
- Every section required by a chapter's governing format must be filled or hold `None`. A `None` that still needs an answer is either a row in `# Open Issues` or an entry `setup-client` raises on the Setup Ledger.
- Any file path referenced by the handoff (such as `<slug>/order-form.pdf`) must exist in the sibling folder beside the handoff file.
- The handoff carries no credentials, API keys, or unredacted payment card or bank numbers.
- A `# Closed` issue in the handoff must already have a matching decision in `# Decision Log`.

## Vocabularies

Uses the vocabularies defined in each chapter's governing format contract.

## Checks

- `python3 scripts/check.py --handoff <path>` validates the handoff before `setup-client` writes anything: client header with `format: clients/handoff` and `format_version: 2`, required chapters in order, and each chapter, shifted up one heading level, passing its governing format's checks.
