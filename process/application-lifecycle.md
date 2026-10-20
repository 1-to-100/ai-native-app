# Process: application-lifecycle (version 1)

# Purpose
Governs how an operator takes this base repository, bootstraps it into a domain-specific AI-native application optimized for a single AI vendor, onboards clients or entities into structured Markdown records, and continuously upgrades the factory line as recurring manual edits or process changes arise.

# Scope
Covers the complete lifecycle of the application infrastructure itself: initial repository customization (`Stage 1`), entity onboarding into `clients/<slug>/` (`Stage 2`), and coordinated mechanism upgrades across `AGENTS.md`, `process/`, `formats/`, `.agents/skills/`, and `scripts/` (`Stage 3`). Domain-specific operational processes created during `Stage 1` are governed by their own files in `process/`.

# Roles
- Operator: Owns the business intent, answers the `create-application` interview, walks the `setup-client` ledger, approves `improve-process` proposals, and commits changes under their email.
- Client: Supplies upstream onboarding facts, signed commercial agreements, and answers to deferred open issues.
- Agent: Executes `create-application`, `setup-client`, and `improve-process` inside the repository contracts.

# Cadence
- Stage 1 runs once when bootstrapping a new AI application from this base template.
- Stage 2 runs once per new or migrating client/entity whenever a handoff file is ready.
- Stage 3 runs continuously whenever the Operator identifies a recurring manual correction, a process defect, or a new business requirement.

# System of Record
## Mode
Repository Markdown

## Location
Root `AGENTS.md` (`formats/global-context.md`), `process/*.md` (`formats/process.md`), `formats/*.md`, `.agents/skills/*/SKILL.md`, `clients/<slug>/` (`formats/client.md`, `formats/open-issues.md`), and `tmp/` for uncommitted interstitial reports.

# Inputs
- `docs/build-any-ai-application.md` (the governing factory blueprint).
- Operator's business domain knowledge, chosen AI vendor (`Claude`, `OpenAI`, or `Gemini`), and operator email address.
- For Stage 2: an onboarding handoff file conforming to `formats/handoff.md` and any signed `order-form.pdf`.
- For Stage 3: an operator change request or observed friction point from running an operational stage.

# Stages
## Stage 1: Application Bootstrap
### Entry Criteria
A clean clone of the base `ai-native-app` repository, the blueprint at `docs/build-any-ai-application.md`, and an Operator ready to define the application's scope, target AI environment, processes, and data formats.

### Description
The Operator invokes `create-application`. The Agent asks which AI vendor environment to optimize for (`Claude`, `OpenAI`, or `Gemini`), interviews the Operator to write the Global Context in the root `AGENTS.md`, maps each core business workflow into a stage-by-stage process file in `process/`, defines the required document schemas in `formats/`, writes subtree `AGENTS.md` files and initial operational skills in `.agents/skills/`, updates `scripts/check.py`, and wires the environment with `scripts/setup-scripts.py`.

### Graduation Criteria
Root `AGENTS.md`, `process/`, `formats/`, `.agents/skills/`, and `scripts/check.py` are written and approved by the Operator; `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` both exit with zero errors; and `tmp/create-application-report.md` is written.

### Branching and Terminal Paths
- **Approved and Lint-Clean:** Advances to live operation (`Stage 2` for entity onboarding and domain processes in `process/`).
- **Revision Needed:** If the Operator rejects part of the proposed processes or formats during the interview gates, `create-application` revises the affected mechanism before moving down the creation order.
- **Aborted:** If the Operator cancels before completion, no partial unlinted changes are committed.

### Implementing Skills
`create-application`

## Stage 2: Client and Entity Onboarding
### Entry Criteria
Stage 1 is complete (or the base formats are in force), and a handoff file in `formats/handoff.md` format (plus any sibling asset folder and redacted `order-form.pdf`) has been supplied for a client slug that does not yet exist in `clients/` or `archive/`.

### Description
The Operator invokes `setup-client <path-to-handoff.md>`. The Agent validates the handoff with `python3 scripts/check.py --handoff <path>`, scaffolds `clients/<slug>/`, splits each handoff chapter into its governed document (`client.md`, `open-issues.md`, and domain files), reconciles commercial entitlements against `order-form.pdf`, and records every `None` field, placeholder, or discrepancy on the Setup Ledger with `Evidence` and a `Recommended Approach`. The Agent then walks the Setup Ledger entry by entry with the Operator, writing accepted answers into target documents and opening rows in `open-issues.md` for deferred items.

### Graduation Criteria
Every Setup Ledger entry is either answered in its target document (with its issue moved to `# Closed`) or recorded as an `# Open` row in `clients/<slug>/open-issues.md` with a `Next Step`; `clients/README.md` includes the client; `python3 scripts/check.py <slug>` passes with zero errors; and `tmp/setup-report-<slug>.md` is written.

### Branching and Terminal Paths
- **Onboarded (Active):** The client folder is lint-clean and enters the application's recurring operational processes.
- **Handoff Rejected (Returned Upstream):** If `python3 scripts/check.py --handoff <path>` fails with errors, `setup-client` halts before creating `clients/<slug>/` and returns the findings to the upstream handoff author.
- **Retired (`Archived`):** When an active client later offboards or terminates, their folder is moved to `archive/<slug>/` with an `ARCHIVED.md` note and `clients/README.md` and `archive/README.md` are updated.

### Implementing Skills
`setup-client`

## Stage 3: Continuous Process Improvement
### Entry Criteria
The Operator observes a recurring manual correction, a process bottleneck, a missing data field, or a new business rule while running the application, and invokes `improve-process` with the change request.

### Description
The Agent diagnoses the request against the precedence hierarchy defined in `docs/build-any-ai-application.md` (`Global Context` -> `Process` -> `Formats` -> `Subtree Agents` -> `Skills` -> `Scripts` -> active data files). It writes a complete impact analysis and change proposal to `tmp/improve-process-proposal.md` and presents it to the Operator for review. On explicit Operator approval, it updates all affected files in dependency order, bumps version numbers on modified processes and formats, migrates active documents to the new `format_version`, updates directory `README.md` inventories, and updates `scripts/check.py`.

### Graduation Criteria
The Operator explicitly approves the proposal; all affected mechanisms, active documents, and inventories are updated atomically; and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` pass with zero errors.

### Branching and Terminal Paths
- **Accepted and Applied:** Changes are verified and committed to the repository, becoming the new standard for the next run.
- **Proposal Revised:** The Operator modifies the scope or design at the proposal gate; `improve-process` updates `tmp/improve-process-proposal.md` and re-presents before editing any governed file.
- **Proposal Rejected (`Cancelled`):** The Operator declines the change; governed repository files remain untouched.

### Implementing Skills
`improve-process`

# Outputs
- Tailored Global Context (`AGENTS.md`), domain processes (`process/*.md`), format contracts (`formats/*.md`), skills (`.agents/skills/*/SKILL.md`), and verification rules (`scripts/check.py`).
- Lint-clean client folders under `clients/<slug>/` with tracked open issues in `clients/<slug>/open-issues.md`.
- Uncommitted interstitial reports in `tmp/` (`tmp/create-application-report.md`, `tmp/setup-report-<slug>.md`, `tmp/improve-process-proposal.md`).

# Rules
- Follow the creation and precedence order strictly: Global Context (`AGENTS.md`) -> Process (`process/`) -> Formats (`formats/`) -> Subtree Agents (`<dir>/AGENTS.md`) -> Skills (`.agents/skills/`) -> Scripts (`scripts/`) -> Client/Catalog Data (`clients/`).
- Never create a client folder outside `setup-client`.
- Never modify a format contract without bumping `format_version`, migrating active files, and updating `scripts/check.py` in the same commit.
- Never write interstitial proposals or setup reports outside `tmp/`.

# Related
- Blueprint: `docs/build-any-ai-application.md`.
- Formats: `formats/global-context.md`, `formats/process.md`, `formats/client.md`, `formats/open-issues.md`, `formats/handoff.md`.
- Skills: `create-application`, `setup-client`, `improve-process`.
- Scripts: `scripts/check.py`, `scripts/setup-scripts.py`.
- Gaps: None in the base lifecycle; domain-specific processes are added by `create-application`.
