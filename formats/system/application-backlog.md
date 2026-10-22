# Format: system/application-backlog (version 1)

## Purpose

The backlog of application changes and future enhancements that the operator wants to keep, but does not want to implement yet. `add-to-backlog` captures an item. `process-backlog` refines one item and hands it to `improve-process`.

## Location

`system/application-backlog.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md` with `format: system/application-backlog` and `format_version: 1`. No `client` key.

## Body

When no item exists yet, the body is the single line `None`. Otherwise each record uses an `# APP-NNNN` heading, with `NNNN` a four-digit integer, and these `##` sections in order:

```markdown
# APP-0001
## Title
A short name for the request.

## Status
A Display Name from Backlog Statuses.

## Opened
The date the item was added, `YYYY-MM-DD`.

## Request
The operator's request as supplied, without invented requirements.

## Refined Requirement
The requirement after `process-backlog` has grilled it enough to plan, or `None` while it is still `Proposed`.

## Acceptance Criteria
The observable conditions that show the requirement is implemented, or `None` while it is still `Proposed`.

## Plan
A summary of the approved implementation plan, or `None` before a plan exists. When the plan has a repository path, name it in backticks.

## Dependencies
Other backlog headings this item waits on, one `- APP-NNNN` per line, or `None`.

## Resolution
What was implemented and where, or why the item was cancelled. `None` until the item is `Done` or `Cancelled`.
```

## Rules

- Headings are never reused or deleted. A finished item stays in the file with status `Done` or `Cancelled`.
- Client-specific missing facts stay in `clients/<slug>/open-issues.md`. Only application-level changes and enhancements belong here.
- `Proposed` means captured and not yet refined. `Ready` means the requirement, acceptance criteria, and plan are sufficient to invoke `improve-process`.
- Dependencies refer to other headings in this same file and must not form a cycle.

## Vocabularies

Backlog Statuses:

| Display Name | Meaning |
| --- | --- |
| Proposed | Captured for later. Requirement and plan are not finished. |
| Ready | Refined and planned enough to implement through `improve-process`. |
| In Progress | `improve-process` is applying the approved plan. |
| Done | The requirement was implemented and reviewed. |
| Cancelled | The operator decided not to implement it. The row remains. |

## Checks

- System header with `format: system/application-backlog` and `format_version: 1`.
- The body is `None`, or every `#` heading matches `APP-` plus four digits, is unique, and contains `## Title`, `## Status`, `## Opened`, `## Request`, `## Refined Requirement`, `## Acceptance Criteria`, `## Plan`, `## Dependencies`, and `## Resolution` in that order.
- `## Title` and `## Request` are not `None`. `## Status` is a Backlog Status Display Name. `## Opened` is `YYYY-MM-DD`.
- `Ready` and `In Progress` require `## Refined Requirement`, `## Acceptance Criteria`, and `## Plan` to be other than `None`.
- `Done` and `Cancelled` require `## Resolution` to be other than `None`. `Proposed` allows `None` for the later sections.
- Every dependency bullet matches another heading in this file, is not the item itself, and the dependency graph has no cycle.
- A backticked repository path inside `## Plan` must exist.
