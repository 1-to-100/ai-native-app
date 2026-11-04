# Format: clients/open-items (version 4)

## Purpose

The one place that holds everything open for a client: the process runs currently in flight (which process, which stage, who is responsible, and how it is going) and the ad hoc issues to review with the customer. This contract is version 4 because it continues the lineage of the retired open-issues contract (versions 1 to 3), adding the in-flight queue.

Two queues live here. **In-flight process items** track every run of a process from `process/` that this client is moving through, with its current stage and responsible party. **Open issues** track anything unresolved, missing, or unconfirmed about the client, so no gap hides inside another document. An issue is opened when `setup-client`, `review-open-issues`, or an operational skill finds a missing fact (`None`), a conflict between sources, or a pending decision. It leaves `# Open` only when the answer has been written into the target document named by `Area` and the decision has been appended to `clients/<slug>/decision-log.md` in the same change.

## Location

`clients/<slug>/open-items.md`. One per client folder. The format identifier is `clients/open-items`.

## Header

The client header defined in `formats/README.md` with `format: clients/open-items`, `format_version: 4`, and `client` equal to the folder slug.

## Body

```markdown
# In Flight
| # | Opened | Process | Stage | Responsible | Updated | Status Notes |
| --- | --- | --- | --- | --- | --- | --- |

One row per process run currently in progress for this client, or the single line `None`. `#` is a positive integer, unique across all four tables in this file, and never reused. `Opened` is the `YYYY-MM-DD` date the run entered Stage 1. `Process` is the exact `# <Process Name>` heading of a process in a lifecycle stage file under `process/`. `Stage` is the exact `Stage N: <Name>` heading of the stage the run is currently in. `Responsible` is the party responsible for that stage right now: the stage's owning role slug (the first role under its `#### Owner`) while nobody has taken it on, the email of the user from `system/users.md` who took it on, or `Automation` when the stage is Automation-owned. `Updated` is the `YYYY-MM-DD` date of the last change to the row. `Status Notes` is a short plain-language note on where the work stands.

# Completed
| # | Opened | Completed | Process | Outcome | Status Notes |
| --- | --- | --- | --- | --- | --- |

One row per finished process run, or the single line `None`. When a run reaches a terminal path, its row moves here from `# In Flight` with its original `#` and `Opened` date, `Completed` set to today's date, `Outcome` naming the terminal path reached, and `Status Notes` holding the final note.

# Open
| # | Opened | Area | Issue | Next Step |
| --- | --- | --- | --- | --- |

One row per unresolved issue, or the single line `None` when nothing is open. `Opened` is `YYYY-MM-DD`. `Area` is a Display Name from Areas naming the document where the answer will land. `Issue` states what is missing or conflicting and why it matters. `Next Step` states who does what to resolve it.

# Closed
| # | Opened | Closed | Area | Issue | Resolution |
| --- | --- | --- | --- | --- | --- |

One row per resolved issue, or the single line `None` when nothing has been closed yet. When an open issue is answered, its row moves here from `# Open` with its original `#` and `Opened` date, `Closed` set to today's date (`YYYY-MM-DD`), and `Resolution` stating what was decided, which target section was written, and which `decision-log.md` row received the decision.
```

## Rules

- IDs (`#`) are unique positive integers across `# In Flight`, `# Completed`, `# Open`, and `# Closed`, and are never reused. One ID space keeps `open-items #<id>` unambiguous.
- A row is never deleted. An in-flight row moves to `# Completed`. An open issue moves to `# Closed`.
- A run enters `# In Flight` when a process starts for this client, at `Stage 1` with `Responsible` set to that stage's owning role. Each stage graduation advances `Stage` and resets `Responsible` to the next stage's owning role (or `Automation`). `whats-next` replaces the role slug with the email of the user who takes the stage on.
- `Responsible` is a role slug only when it is the current stage's owning role; it is an email only when that email is a record in `system/users.md`; it is `Automation` only when the current stage is Automation-owned.
- A run reaches `# Completed` only through a terminal path named in the process's `#### Branching and Terminal Paths`, and `Outcome` names that path.
- Closing an issue requires, in the same change, writing its answer into the document named by `Area` and appending one row to `# Decisions` in `clients/<slug>/decision-log.md`.
- The decision-log `Source` for that row is `open-items #<id>`.
- `setup-client` opens an issue row for every required field left `None` or deferred during the Setup Ledger walk.
- `review-open-issues` presents one `# Open` row at a time and does not close it until the operator accepts a resolution. `client-status` reads this file and writes nothing to it.

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

- Client header with `format: clients/open-items`, `format_version: 4`, and `client` matching the folder name.
- `# In Flight`, `# Completed`, `# Open`, and `# Closed` sections are present in exact order, each containing either `None` or a Markdown table with the exact column headers above.
- Every `#` ID is a positive integer and unique across all four tables.
- `Opened`, `Completed`, `Closed`, and `Updated` are valid `YYYY-MM-DD` dates.
- In `# In Flight`, `Process` matches a `# <Process Name>` heading in a lifecycle stage file under `process/`, `Stage` matches a `### Stage N: <Name>` heading of that process, and `Responsible` is that stage's owning role slug, an email that is a record heading in `system/users.md`, or `Automation` on an Automation-owned stage.
- In `# Completed`, `Process` matches a process heading under `process/`.
- `Area` is a valid Display Name from Areas.
- Every `# Closed` ID appears as `open-items #<id>` in the `Source` column of `clients/<slug>/decision-log.md`.
