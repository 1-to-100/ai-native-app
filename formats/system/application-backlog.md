# Format: system/application-backlog (version 3)

## Purpose

The backlog of application changes and future enhancements that the operator wants to keep, but does not want to implement yet. `add-to-backlog` interviews the operator and captures an item with a complete typed request. `process-backlog` refines one item and hands it to `improve-process`.

## Location

`system/application-backlog.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md` with `format: system/application-backlog` and `format_version: 3`. No `client` key.

## Body

When no item exists yet, the body is the single line `None`. Otherwise each record uses an `# APP-NNNN` heading, with `NNNN` a four-digit integer, and these `##` sections in order. `## Request` holds the typed `###` subsections shown, in order, and nothing before the first one:

```markdown
# APP-0001
## Title
A short name for the request.

## Status
A Display Name from Backlog Statuses.

## Opened
The date the item was added, `YYYY-MM-DD`.

## Request
### Statement
The operator's request in their own words, without invented requirements.

### Problem and Trigger
What is missing or going wrong today, where it was seen, and who it affects.

### Desired Outcome
What must be observably true when the change is done, and how someone would check it.

### In Scope
What the change includes.

### Out of Scope
What the change deliberately excludes, or `None`.

### Mechanisms and Records Affected
The global context, processes, formats, skills, scripts, and `system/` records the change touches, and any active documents that would need migrating.

### Constraints
Rules that must keep holding, or `None`.

### Why Held
Why the item waits and what would make it urgent, or `None`.

### Open Points
Unresolved questions the operator could not answer yet, one `- ` bullet each naming what is missing and what would answer it, or `None`.

## Refined Requirement
The requirement after `process-backlog` has finalized it with the operator, or `None` while it is still `Proposed`.

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
- Client-specific missing facts stay in `clients/<slug>/open-items.md`. Only application-level changes and enhancements belong here.
- Every record carries all nine `###` subsections under `## Request`, in order. `### Statement`, `### Problem and Trigger`, `### Desired Outcome`, `### In Scope`, and `### Mechanisms and Records Affected` are never `None`. The other four may be `None`.
- `### Open Points` is `None` or a bullet list. An answered open point moves into the subsection it belongs to and leaves the list.
- `Proposed` means captured with a complete typed request and not yet refined or planned. `Ready` means the requirement, acceptance criteria, and plan are sufficient to invoke `improve-process` and no open point remains.
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

- System header with `format: system/application-backlog` and `format_version: 3`.
- The body is `None`, or every `#` heading matches `APP-` plus four digits, is unique, and contains `## Title`, `## Status`, `## Opened`, `## Request`, `## Refined Requirement`, `## Acceptance Criteria`, `## Plan`, `## Dependencies`, and `## Resolution` in that order.
- `## Request` opens directly with `### Statement` and contains exactly `### Statement`, `### Problem and Trigger`, `### Desired Outcome`, `### In Scope`, `### Out of Scope`, `### Mechanisms and Records Affected`, `### Constraints`, `### Why Held`, and `### Open Points` in that order, each non-empty. The five required subsections are not `None`. `### Open Points` is `None` or a bullet list.
- `## Title` is not `None`. `## Status` is a Backlog Status Display Name. `## Opened` is `YYYY-MM-DD`.
- `Ready` and `In Progress` require `## Refined Requirement`, `## Acceptance Criteria`, and `## Plan` to be other than `None`, and `### Open Points` to be `None`.
- `Done` and `Cancelled` require `## Resolution` to be other than `None`. `Proposed` allows `None` for the later sections.
- Every dependency bullet matches another heading in this file, is not the item itself, and the dependency graph has no cycle.
- A backticked repository path inside `## Plan` must exist.
