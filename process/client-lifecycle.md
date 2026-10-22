# Process: client-lifecycle (version 1)

# Purpose
Governs how a client enters the repository from a handoff and how unresolved client issues are decided, written into the client record, and appended to that client's decision log.

# Scope
Covers creation of `clients/<slug>/` and later review of `clients/<slug>/open-issues.md`. It does not discover prospects, negotiate commercial terms, or change application mechanisms. Mechanism changes go to `application-lifecycle`.

# Roles
- Operator: Supplies the handoff, walks the Setup Ledger, and accepts or defers each recommended issue resolution.
- Client: Supplies facts the operator cannot answer. The client does not edit the repository.
- Agent: Executes `setup-client` and `review-open-issues`.

# Cadence
- Stage 1 runs once per new or migrating client when a handoff file is ready.
- Stage 2 runs when the operator wants to work through that client's open issues, typically before or during the next client meeting.

# System of Record
## Mode
Repository Markdown

## Location
`clients/<slug>/` governed by `clients/client`, `clients/open-issues`, and `clients/decision-log`. Assignment routing for the client may be read from `system/client-assignments.md`.

# Inputs
- For Stage 1, a handoff file conforming to `clients/handoff` and any sibling `order-form.pdf`.
- For Stage 2, a client slug and the current `open-issues.md`, `decision-log.md`, and the rest of that client folder.
- Operator email address.

# Stages
## Stage 1: Client Onboarding
### Entry Criteria
A handoff file in `clients/handoff` format, plus any sibling asset folder and redacted `order-form.pdf`, has been supplied for a client slug that does not yet exist in `clients/` or `archive/`.

### Description
The operator invokes `setup-client` with the handoff path. The Agent validates the handoff, scaffolds `clients/<slug>/`, splits each chapter into its governed document (`client.md`, `open-issues.md`, and `decision-log.md`, plus any domain files), and walks the Setup Ledger with the operator. Deferred facts stay on `# Open`. Accepted facts are written to the target document, and any issue closed during the walk is appended to the decision log.

### Graduation Criteria
Every Setup Ledger entry is either written into its target document or recorded as an `# Open` row. Every `# Closed` row has a matching decision-log row. `clients/README.md` includes the client. `python3 scripts/check.py <slug>` passes with zero errors, and `tmp/setup-report-<slug>.md` is written.

### Branching and Terminal Paths
- **Onboarded (Active):** The client folder is lint-clean and can enter the application's operational processes.
- **Handoff Rejected (Returned Upstream):** `python3 scripts/check.py --handoff <path>` reports an error. `setup-client` stops before creating `clients/<slug>/`.
- **Retired (`Archived`):** When an active client later leaves, the folder moves to `archive/<slug>/` with an `ARCHIVED.md` note, and active assignments for that slug are ended through `update-user`.

### Implementing Skills
`setup-client`

## Stage 2: Open Issue Review
### Entry Criteria
`clients/<slug>/` exists, and the operator invokes `review-open-issues` for that slug. Stage 1 has already created `open-issues.md` and `decision-log.md`.

### Description
The Agent reads the open issues and the rest of the client folder, then prompts the operator with one issue and a recommended resolution grounded in that folder. On acceptance, the Agent writes the answer to the document named by `Area`, appends the decision, and moves the issue to `# Closed`. On deferral, the issue stays open and its `Next Step` is updated only from what the operator said.

### Graduation Criteria
The operator has accepted or deferred each issue that was presented. Every accepted issue has its answer in the target document and one new decision-log row. `python3 scripts/check.py <slug>` passes with zero errors.

### Branching and Terminal Paths
- **Resolved:** The presented issues are closed and the decision log holds them.
- **Deferred:** An issue stays on `# Open` with the operator's next step.
- **No Open Issues:** The stage stops immediately when `# Open` is `None`.
- **Unknown Client:** The slug is not a folder under `clients/`. The stage stops and asks the operator to pick a listed slug.

### Implementing Skills
`review-open-issues`

# Outputs
- A client folder containing `client.md`, `open-issues.md`, and `decision-log.md`.
- Closed issues matched one-for-one by decision-log sources of the form `open-issues #<id>`.
- `tmp/setup-report-<slug>.md` after onboarding.

# Rules
- Never create a client folder outside `setup-client`.
- Never invent a client fact. A silent source stays `None` and remains an open issue.
- Closing an issue writes the target document and the decision log in the same change.
- Client work reads only this client's assignment rows from `system/client-assignments.md`.

# Related
- Formats: `clients/handoff`, `clients/client`, `clients/open-issues`, `clients/decision-log`.
- Skills: `setup-client`, `review-open-issues`.
- Processes: `application-lifecycle`, `user-administration`.
- Scripts: `scripts/check.py`.
- Gaps: None.
