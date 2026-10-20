# Format: process (version 1)

## Purpose

Defines a business workflow as a sequence of discrete, handoff-sized stages with explicit entry criteria, stage descriptions, graduation criteria, branching or terminal outcomes (such as `Closed Won` and `Closed Lost`), the system of record where the process is modeled, and the skills that implement each stage.

## Location

`process/<slug>.md`, with a matching row in `process/README.md`.

## Header

No YAML front matter. The first line is `# Process: <slug> (version N)`, where `<slug>` matches the filename without `.md` and `N` is a positive integer.

## Body

```markdown
# Purpose
One paragraph stating what this process achieves for the business and why it exists.

# Scope
What this process covers from start to finish, and what it leaves to upstream or downstream processes.

# Roles
A bullet list or table of the human and agent roles that participate in this process, selected from the Role vocabulary in `process/README.md`.

# Cadence
When this process runs or what event triggers it.

# System of Record
## Mode
Where the state of work moving through this process is modeled, written as a Display Name from System of Record Modes (`Repository Markdown` or `External System`).

## Location
When Mode is `Repository Markdown`, the repository path(s) and governing format(s) that hold the state (for example, `clients/<slug>/` governed by `formats/client.md` and `formats/open-issues.md`). When Mode is `External System`, the name of the external tracking system (such as Jira, Linear, HubSpot, or Salesforce), the full `https://` URL to the project or board, and how repository files link to external record IDs.

# Inputs
A bullet list of the documents, contracts, or signals required before Stage 1 can begin.

# Stages
One `## Stage N: <Stage Name>` section per discrete stage in execution order (starting at `Stage 1`). Every stage must be small enough for a single agent session to execute and hand off via a durable artifact. Each stage contains the five `###` subsections below in exact order:

## Stage 1: <Stage Name>
### Entry Criteria
What must be true, and which artifacts or approvals must exist, before work may enter this stage.

### Description
What happens during this stage, which role owns the work, and what artifact or state change is produced.

### Graduation Criteria
The exact proof, `scripts/check.py` validation, or explicit human approval required to complete this stage and advance to the next stage.

### Branching and Terminal Paths
How work branches when it does not advance linearly to the next stage. Name every branch or terminal state explicitly—for example, advancing to the next stage on approval, branching to remediation on findings, or terminating in `Closed Won`, `Closed Lost`, `Approved`, `Rejected`, `Deferred`, or `Cancelled`—and state what happens on each path. Write `None (advances directly to next stage)` only when no branch exists.

### Implementing Skills
When System of Record Mode is `Repository Markdown`, list the skill slug(s) in `.agents/skills/` that execute this stage (e.g., `create-application`, `setup-client`, `improve-process`), or write `Manual (Gap)` when a human operator currently performs the stage by hand without a skill. When Mode is `External System`, state either the skill slug(s) that sync/operate the stage or `External (<System Name>)`.

# Outputs
A bullet list of the durable repository documents (or external system records) that exist when the process completes.

# Rules
A bullet list of defaults, commercial override rules, and `Never` constraints specific to this process.

# Related
A bullet list naming the formats, skills, scripts, other processes, and any known `Gap` where a stage is still manual.
```

## Rules

- Every stage is governed by its process document and sized so a fresh-context agent can run it from its `Entry Criteria` to its `Graduation Criteria` and stop.
- A process never copies the full field list of a format or the internal step list of a skill; it names the format or skill and states what the business expects from it.
- When a process is modeled in `Repository Markdown`, every skill named under `### Implementing Skills` (unless marked `Manual (Gap)`) must exist in `.agents/skills/<skill-slug>/SKILL.md` and in `.agents/skills/README.md`.
- When a process is modeled in an `External System`, `## Location` under `# System of Record` must include the external system name and an `https://` link (or `Pending setup via create-application` while in template state).
- When a process changes, bump `(version N)` in its title line and update `process/README.md` in the same commit.

## Vocabularies

System of Record Modes:

| Display Name | Description |
| --- | --- |
| Repository Markdown | State and artifacts are stored natively as structured Markdown files in this Git repository. |
| External System | State is tracked in an external system of record (such as Jira, Linear, HubSpot, or Salesforce) linked from `# System of Record` -> `## Location`. |

## Checks

- First line matches `# Process: <slug> (version N)` where `<slug>` equals the filename stem.
- All ten `#` sections (`# Purpose`, `# Scope`, `# Roles`, `# Cadence`, `# System of Record`, `# Inputs`, `# Stages`, `# Outputs`, `# Rules`, `# Related`) are present in exact order.
- `# System of Record` contains `## Mode` and `## Location`, and `## Mode` is `Repository Markdown` or `External System`. If `External System`, `## Location` contains an `https://` URL.
- `# Stages` contains at least one `## Stage N: <Name>` section (numbered sequentially `Stage 1`, `Stage 2`, ...), and every stage contains `### Entry Criteria`, `### Description`, `### Graduation Criteria`, `### Branching and Terminal Paths`, and `### Implementing Skills` in exact order.
- Every skill slug backticked under `### Implementing Skills` (when not `Manual (Gap)` or `External (...)`) resolves to an existing `.agents/skills/<slug>/SKILL.md`.
