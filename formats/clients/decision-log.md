# Format: clients/decision-log (version 2)

## Purpose

The single log of decisions made for one client. It replaces any file-specific decisions table. Before an agent asks the operator a question during client work, it reads this log: if an existing decision answers the question, the agent proceeds on that decision and cites it.

## Location

`clients/<slug>/decision-log.md`. One per client folder. The format identifier is `clients/decision-log`.

## Header

The client header defined in `formats/README.md` with `format: clients/decision-log`, `format_version: 2`, and `client` equal to the folder slug.

## Body

```markdown
# Decisions
| # | Date | Area | Decision | Source |
| --- | --- | --- | --- | --- |

One row per decision, or the single line `None` when no decision has been recorded. `#` is a positive integer and is never reused. `Date` is `YYYY-MM-DD`. `Area` is a Display Name from the Areas vocabulary in `formats/clients/open-items.md`, naming the document the decision changed. `Decision` states what was decided. `Source` is `open-items #<id>` when the decision closes a client issue, or `operator` when the operator decided it outside an issue row.
```

## Rules

- Rows are append-only. A reversal is a new dated row. No row is deleted or reworded.
- Closing an issue in `open-items.md` appends exactly one decision row whose `Source` is `open-items #<id>` and whose `Area` matches that issue.
- An in-flight process row completing in `open-items.md` does not require a decision row. A decision cites an issue, never an in-flight item.
- No other document in the client folder keeps its own decisions table.
- The log records the decision for this client only. It does not compare the client with another client.

## Vocabularies

Uses Areas from `formats/clients/open-items.md`.

## Checks

- Client header with `format: clients/decision-log`, `format_version: 2`, and `client` matching the folder name.
- The only `#` section is `# Decisions`, containing either `None` or a Markdown table with columns `#`, `Date`, `Area`, `Decision`, and `Source`.
- Every `#` is a unique positive integer. `Date` is `YYYY-MM-DD`. `Area` is a valid Areas Display Name.
- `Source` is `operator` or `open-items #<id>`, and that id is a `# Closed` issue in the client's `open-items.md`.
- Every closed issue id in `open-items.md` is cited by exactly one `Source` cell.
