# Process: application-lifecycle (version 2)

# Purpose
Governs how an operator configures this repository, upgrades it to the current template application paradigm, and changes its mechanisms when operational friction or a new requirement appears.

# Scope
Covers application setup and configuration in `system/` and the framework contracts, upgrades pulled from the template repository, and coordinated mechanism changes across `AGENTS.md`, `process/`, `formats/`, `.agents/skills/`, and `scripts/`. Client onboarding is governed by `client-lifecycle`. Domain workflows created during setup are governed by their own files in `process/`.

# Roles
- Operator: Supplies configuration answers, approves setup and improvement gates, and commits changes under their email.
- Reviewer: Inspects an upgrade or improvement in a fresh context against the approved plan.
- Agent: Executes `setup-application`, `upgrade-app`, and `improve-process` inside the repository contracts.

# Cadence
- Stage 1 runs when the operator invokes setup with a configuration request, and when setup is invoked with no request so the reserved framework files and `system/` records can be completed.
- Stage 2 runs when the operator asks to upgrade this repository to the current template paradigm.
- Stage 3 runs whenever the operator identifies a recurring manual correction, a process defect, or a new application requirement.

# System of Record
## Mode
Repository Markdown

## Location
Root `AGENTS.md` (`system/global-context`), `process/*.md` (`system/process`), `formats/system/` and `formats/clients/`, `system/` (`system/users`, `system/user-roles`, `system/client-assignments`, `system/external-systems`, `system/application-backlog`, `system/question-journal`), `.agents/skills/*/SKILL.md`, and `docs/upgrades/` for an upgrade plan. Interstitial reports stay in `tmp/`.

# Inputs
- `docs/build-any-ai-application.md`.
- The operator's configuration request, or no request when a completeness scan is required.
- For Stage 2, network access to `https://github.com/1-to-100/ai-native-app` and a worktree that can accept the upgrade.
- For Stage 3, an operator change request or a backlog item handed over by `process-backlog`.

# Stages
## Stage 1: Application Setup
### Entry Criteria
The operator invokes `setup-application` with a configuration request, or with no request. The blueprint at `docs/build-any-ai-application.md` is readable.

### Description
The Agent determines which `system/` records the request changes and interviews the operator for those records. With no request, the Agent scans `system/` and the reserved framework files (root `AGENTS.md` and the `README.md` and `AGENTS.md` files for `process/`, `formats/`, `.agents/skills/`, `scripts/`, `clients/`, and `system/`), checks each governed file against its format, and interviews the operator until required setup is complete. Missing framework files are created in Global Context, Process, Format, Subtree Agent, Skill, then Script order. The Agent also interviews for external systems and walks through the shared administration those systems need.

### Graduation Criteria
Every required framework file exists, every `system/` registry is either filled from the operator's answers or explicitly confirmed empty, external-system administration steps the operator chose to complete are recorded, and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` exit with zero errors.

### Branching and Terminal Paths
- **Configured:** Advances to live operation. Client onboarding continues in `client-lifecycle`.
- **Mechanism Change:** A request that changes a process, format, skill, or checker is handed to Stage 3 instead of being patched inside setup.
- **Revision Needed:** The operator rejects part of a proposed global context, process, or format. Setup revises that mechanism before continuing down the creation order.
- **Aborted:** The operator cancels before completion. No partial unlinted change is committed.

### Implementing Skills
`setup-application`

## Stage 2: Template Upgrade
### Entry Criteria
The operator invokes `upgrade-app`. The worktree has no unrelated uncommitted changes, and `https://github.com/1-to-100/ai-native-app` is reachable.

### Description
The Agent clones the template application to a temporary directory, reads its `docs/build-any-ai-application.md` and the template files that process names, and writes a step-by-step upgrade plan under `docs/upgrades/`. One subagent executes that plan. A second subagent writes a review plan. A final subagent runs the review plan and fixes gaps.

### Graduation Criteria
The upgrade plan is in `docs/upgrades/`, the review subagent reports no remaining gaps, and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` exit with zero errors.

### Branching and Terminal Paths
- **Upgraded:** The operator is told the upgrade is complete and reviews the diff before commit.
- **Blocked:** Unrelated uncommitted work or an unreachable template URL stops the stage before any upgrade edit.
- **Review Failed:** The final review subagent could not make the repository match the upgrade plan. The stage stops with the findings still open.

### Implementing Skills
`upgrade-app`

## Stage 3: Continuous Process Improvement
### Entry Criteria
The operator invokes `improve-process` with a change request, or `process-backlog` hands over one backlog item whose requirement and plan are ready for implementation.

### Description
The Agent grills the request until the requirement and acceptance criteria are sufficient, writes an implementation plan, and waits for explicit operator approval. After approval, an independent subagent writes a review plan while the implementing agent applies the plan. A final fresh-context subagent runs the review plan and fixes verified gaps. Format changes migrate active documents in the same change.

### Graduation Criteria
The operator approved the plan, the final review subagent finished, affected mechanisms and active documents agree, and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` exit with zero errors.

### Branching and Terminal Paths
- **Accepted and Applied:** The working tree is ready for the operator to review and commit.
- **Plan Revised:** The operator changes the plan at the approval gate. Implementation does not start until the revised plan is approved.
- **Proposal Rejected (`Cancelled`):** The operator declines the plan. Governed files stay as they were before this stage.

### Implementing Skills
`improve-process`

# Outputs
- Configured system records and framework contracts, or a lint-clean mechanism change.
- An upgrade plan in `docs/upgrades/` when Stage 2 runs.
- Uncommitted interstitial reports in `tmp/`.

# Rules
- Follow creation and precedence order when building missing framework files: Global Context, Process, Formats, Subtree Agents, Skills, Scripts, then system and client data.
- A system-data edit that does not change a mechanism stays in Stage 1. A mechanism change goes to Stage 3.
- Never modify a format contract without bumping `format_version`, migrating active files, and updating `scripts/check.py` in the same change.
- Never write interstitial proposals or setup reports outside `tmp/`. Upgrade plans are the exception and belong in `docs/upgrades/`.

# Related
- Blueprint: `docs/build-any-ai-application.md`.
- Formats: `system/global-context`, `system/process`, and the `system/` record formats.
- Skills: `setup-application`, `upgrade-app`, `improve-process`.
- Processes: `client-lifecycle`, `user-administration`, `backlog-management`, `question-review`.
- Scripts: `scripts/check.py`, `scripts/setup-scripts.py`.
- Gaps: None.
