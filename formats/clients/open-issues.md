# Format: clients/open-issues (version 3)

## Purpose

Everything about a client or entity that is unresolved, missing, or unconfirmed, kept in one place so no gap hides inside another document. An issue is opened when `setup-client`, `review-open-issues`, or an operational skill finds a missing fact (`None`), a conflict between sources, or a pending decision. It leaves `# Open` only when the answer has been written into the target document named by `Area` and the decision has been appended to `clients/<slug>/decision-log.md` in the same change.

## Location

`clients/<slug>/open-issues.md`. One per client folder. The format identifier is `clients/open-issues`.

## Header

The client header defined in `formats/README.md` with `format: clients/open-issues`, `format_version: 3`, and `client` equal to the folder slug.

## Body

```markdown
# Open
| # | Opened | Area | Issue | Next Step |
| --- | --- | --- | --- | --- |

One row per unresolved issue, or the single line `None` when nothing is open. `#` is a positive integer, unique across both `# Open` and `# Closed`, and never reused. `Opened` is `YYYY-MM-DD`. `Area` is a Display Name from Areas naming the document where the answer will land. `Issue` states what is missing or conflicting and why it matters. `Next Step` states who does what to resolve it.

# Closed
| # | Opened | Closed | Area | Issue | Resolution |
| --- | --- | --- | --- | --- | --- |

One row per resolved issue, or the single line `None` when nothing has been closed yet. When an open issue is answered, its row moves here from `# Open` with its original `#` and `Opened` date, `Closed` set to today's date (`YYYY-MM-DD`), and `Resolution` stating what was decided, which target section was written, and which `decision-log.md` row received the decision.
```

## Rules

- Issue IDs (`#`) are unique positive integers across `# Open` and `# Closed` and are never reused.
- A row is never deleted. It moves from `# Open` to `# Closed`.
- Closing an issue requires, in the same change, writing its answer into the document named by `Area` and appending one row to `# Decisions` in `clients/<slug>/decision-log.md`.
- The decision-log `Source` for that row is `open-issues #<id>`.
- `setup-client` opens a row for every required field left `None` or deferred during the Setup Ledger walk.
- `review-open-issues` presents one `# Open` row at a time and does not close it until the operator accepts a resolution.

## Vocabularies

Areas:

| Display Name | Target Document |
| --- | --- |
| Client | `clients/<slug>/client.md` |
| Order Form | `clients/<slug>/order-form.md` |
| Access | `clients/<slug>/client.md` (`# Notes` or connected services) |
| Process | `clients/<slug>/` operational files |

`setup-application` and `improve-process` add domain-specific Areas here as new client document formats are added.

## Checks

- Client header with `format: clients/open-issues`, `format_version: 3`, and `client` matching the folder name.
- `# Open` and `# Closed` sections are present in exact order, each containing either `None` or a Markdown table with the exact column headers above.
- Every `#` ID is a positive integer and unique across both tables.
- `Opened` and `Closed` are valid `YYYY-MM-DD` dates.
- `Area` is a valid Display Name from Areas.
- Every `# Closed` ID appears as `open-issues #<id>` in the `Source` column of `clients/<slug>/decision-log.md`.
