# Process: backlog-management (version 1)

# Purpose
Governs how a future application change is captured without being implemented yet, and how one captured item is refined into a requirement and plan that `improve-process` can execute.

# Scope
Covers `system/application-backlog.md` only. Client-specific missing facts belong in `client-lifecycle`. A change the operator wants implemented now skips this process and goes directly to `improve-process` through `application-lifecycle` Stage 3.

# Roles
- Operator: States the request, answers the refinement questions, and approves the handoff to implementation.
- Agent: Executes `add-to-backlog` and `process-backlog`.

# Cadence
- Stage 1 runs whenever the operator wants to save a feature request or issue for later.
- Stage 2 runs when the operator selects one backlog item to refine and implement.

# System of Record
## Mode
Repository Markdown

## Location
`system/application-backlog.md` governed by `system/application-backlog`. The implementation plan prepared in Stage 2 is written to `tmp/` and then carried into `improve-process`. The backlog `## Plan` section keeps the durable summary.

# Inputs
- The operator's feature request or issue, for Stage 1.
- One `APP-NNNN` heading, for Stage 2.
- Operator email address.

# Stages
## Stage 1: Capture Request
### Entry Criteria
The operator invokes `add-to-backlog` with a request, or is ready to state one. The request is an application change, not a missing fact about one client.

### Description
The Agent interviews only enough to record a title and the request in the operator's words, assigns the next `APP-NNNN` heading, and leaves the refined requirement, acceptance criteria, plan, and resolution as `None`.

### Graduation Criteria
A new `Proposed` row exists, its heading has never been used, and `python3 scripts/check.py` passes with zero errors.

### Branching and Terminal Paths
- **Captured:** The row is `Proposed` and the stage ends.
- **Client Fact:** The request is a missing or disputed fact about one client. The stage stops and points the operator to `review-open-issues` for that client.
- **Implement Now:** The operator decides not to wait. The stage stops and points the operator to `improve-process` with the same request.

### Implementing Skills
`add-to-backlog`

## Stage 2: Refine and Hand Off
### Entry Criteria
The operator invokes `process-backlog` and selects one `Proposed` item. The item's dependencies are `None` or are themselves `Done`.

### Description
The Agent grills the operator on that item until the requirement and acceptance criteria are sufficient to plan. It writes the plan to `tmp/backlog-plan-<id>.md`, records the summary on the backlog row, sets the status to `Ready`, and invokes `improve-process` with the requirement and plan. `improve-process` keeps its own approval gate before governed mechanism files change.

### Graduation Criteria
The selected item is `Ready` or has moved to `In Progress` or `Done` under `improve-process`, the plan summary is on the row, and `python3 scripts/check.py` passes with zero errors.

### Branching and Terminal Paths
- **Handed Off:** `improve-process` accepts the requirement and plan and continues under `application-lifecycle` Stage 3.
- **Still Vague:** The operator cannot yet answer a question the plan depends on. The item stays `Proposed`, the open point is written into `## Request`, and the stage stops.
- **Cancelled:** The operator drops the item. Status becomes `Cancelled`, `## Resolution` states why, and the row stays.
- **Blocked:** A dependency is not `Done`. The stage stops without refining past the blocker.

### Implementing Skills
`process-backlog`

# Outputs
- New and updated rows in `system/application-backlog.md`.
- `tmp/backlog-plan-<id>.md` for an item that reached planning.

# Rules
- Never delete a backlog row or reuse an `APP-NNNN` heading.
- Never implement the change inside `add-to-backlog` or `process-backlog`. Implementation belongs to `improve-process`.
- Never invent acceptance criteria the operator did not confirm.
- Never put a client-only fact on the application backlog.

# Related
- Format: `system/application-backlog`.
- Skills: `add-to-backlog`, `process-backlog`, `improve-process`.
- Process: `application-lifecycle`.
- Gaps: None.
