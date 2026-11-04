# Format: system/process (version 3)

## Purpose

Defines a lifecycle stage file: one file per customer lifecycle stage (for example marketing, sales, onboarding, account management, or delivery) holding one or more business processes. Each process is a sequence of discrete, handoff-sized stages with explicit entry criteria, an owner, a description, graduation criteria, branching or terminal outcomes, and the skills that implement each stage, plus the system of record where the process is modeled and the role that supervises it.

## Location

`process/<lifecycle-slug>.md`, with a row per process in `process/README.md`. The format identifier is `system/process`. Lifecycle stages are optional and named by the operator; the template ships none.

## Header

No YAML front matter. The first line is `# Lifecycle Stage: <slug> (version N)`, where `<slug>` matches the filename without `.md` and `N` is a positive integer. That version is bumped whenever any process in the file changes, and it is independent of this format contract's version.

## Body

One `# <Process Name>` section per process in the lifecycle stage. A process name is Title Case prose, is unique across every file in `process/`, and is the text every other document uses to reference the process. Each process contains the ten `##` sections below in exact order:

```markdown
# <Process Name>
## Purpose
One paragraph stating what this process achieves for the business and why it exists.

## Scope
What this process covers from start to finish, and what it leaves to upstream or downstream processes.

## Supervisor Role
The single role slug (a `#` heading in `system/user-roles.md`, status `Active`) responsible for checking that this process is executed properly. The supervisor does not own the stages; the stage owners do.

## Cadence
When this process runs or what event triggers it.

## System of Record
### Mode
Where the state of work moving through this process is modeled, written as a Display Name from System of Record Modes (`Repository Markdown` or `External System`).

### Location
When Mode is `Repository Markdown`, the repository path(s) and governing format identifier(s) that hold the state; the in-flight row for each client run lives in `clients/<slug>/open-items.md`. When Mode is `External System`, the name of the external tracking system, the full `https://` URL to the project or board, and how repository files link to external record IDs.

## Inputs
A bullet list of the documents, contracts, or signals required before Stage 1 can begin.

## Stages
One `### Stage N: <Stage Name>` section per discrete stage in execution order (starting at `Stage 1`). Every stage must be small enough for a single session to execute and hand off via a durable artifact. Each stage contains the six `####` subsections below in exact order:

### Stage 1: <Stage Name>
#### Entry Criteria
What must be true, and which artifacts or approvals must exist, before work may enter this stage.

#### Owner
Who owns this stage. Either a bullet list of role slugs, one `- <role-slug>` per line, each an `Active` heading in `system/user-roles.md`, where the first role owns the stage and users of that role are its default assignees, and every later role is a backup the owning role coordinates outside the system; or the single line `Automation: On-Demand` or `Automation: Recurring (<schedule>)`, where the stage is executed by an agent with no human interaction, on request or on the written schedule.

#### Description
What happens during this stage, what decisions are made, and what artifact or state change is produced.

#### Graduation Criteria
The exact proof, `scripts/check.py` validation, or explicit human approval required to complete this stage and advance to the next stage.

#### Branching and Terminal Paths
How work branches when it does not advance linearly to the next stage. Name every branch or terminal state explicitly and state what happens on each path. Write `None (advances directly to next stage)` only when no branch exists.

#### Implementing Skills
When System of Record Mode is `Repository Markdown`, list the skill slug(s) in `.agents/skills/` that execute this stage, or write `Manual (Gap)` when a human currently performs the stage by hand. When Mode is `External System`, state either the skill slug(s) that operate the stage or `External (<System Name>)`. An Automation-owned stage always names at least one skill.

## Outputs
A bullet list of the durable repository documents or external system records that exist when the process completes.

## Rules
A bullet list of defaults, override rules, and `Never` constraints specific to this process.

## Related
A bullet list naming the formats, skills, scripts, other processes, and any known gap where a stage is still manual.
```

## Rules

- A lifecycle stage file holds one or more processes. A process name is unique across all of `process/` and is referenced by its exact heading text in `system/user-roles.md` (`## Processes`), `system/question-journal.md` (`Process`), and `clients/<slug>/open-items.md` (`Process`).
- Every stage is governed by its process section and sized so a fresh-context agent can run it from its `Entry Criteria` to its `Graduation Criteria` and stop.
- The first role under `#### Owner` owns the stage. Users whose `## Primary Role` is that role are the default assignees, and `whats-next` offers the stage to them first. Later roles are backups and are offered second. The owning role coordinates backups outside the system.
- `## Supervisor Role` names the one role that checks the process is executed properly. It may also own stages.
- An Automation stage is executed by an agent independently. `On-Demand` runs when a person or a preceding stage calls for it. `Recurring` runs on the schedule written in the parentheses, carried by the agent environment's scheduled task; the repository records the schedule and does not run it. An Automation stage cannot be `Manual (Gap)`.
- A process never copies the full field list of a format or the internal step list of a skill. It names the format or skill and states the business intent.
- When a process is modeled in `Repository Markdown`, every skill slug under `#### Implementing Skills` (unless marked `Manual (Gap)`) must exist in `.agents/skills/<skill-slug>/SKILL.md` and in `.agents/skills/README.md`.
- When a process is modeled in an `External System`, `### Location` under `## System of Record` must include an `https://` link.
- When any process in the file changes, bump `(version N)` in the file's title line and update `process/README.md` in the same commit.
- Fewer, well-defined roles are better. Before introducing a new role to own a stage, check whether an existing role in `system/user-roles.md` already does that work.

## Vocabularies

System of Record Modes:

| Display Name | Description |
| --- | --- |
| Repository Markdown | State and artifacts are stored natively as structured Markdown files in this Git repository. |
| External System | State is tracked in an external system of record linked from `## System of Record` -> `### Location`. |

Automation Modes:

| Display Name | Written as | Description |
| --- | --- | --- |
| On-Demand | `Automation: On-Demand` | The agent executes the stage when a person or a preceding stage calls for it. |
| Recurring | `Automation: Recurring (<schedule>)` | The agent executes the stage on the schedule in the parentheses, run as a scheduled task in the agent environment. |

## Checks

- First line matches `# Lifecycle Stage: <slug> (version N)` where `<slug>` equals the filename stem.
- The body holds at least one `# <Process Name>` section, and every process name is unique across all files in `process/`.
- Every process holds all ten `##` sections (`## Purpose`, `## Scope`, `## Supervisor Role`, `## Cadence`, `## System of Record`, `## Inputs`, `## Stages`, `## Outputs`, `## Rules`, `## Related`) in exact order.
- `## Supervisor Role` is one role slug that resolves to an `Active` record in `system/user-roles.md`.
- `## System of Record` contains `### Mode` and `### Location`, and `### Mode` is `Repository Markdown` or `External System`. If `External System`, `### Location` contains an `https://` URL.
- `## Stages` contains at least one `### Stage N: <Name>` section, numbered sequentially from `Stage 1`, and every stage contains `#### Entry Criteria`, `#### Owner`, `#### Description`, `#### Graduation Criteria`, `#### Branching and Terminal Paths`, and `#### Implementing Skills` in exact order, none empty.
- `#### Owner` is a bullet list of unique role slugs that each resolve to an `Active` record in `system/user-roles.md`, or exactly `Automation: On-Demand`, or `Automation: Recurring (<schedule>)` with a non-empty schedule.
- An Automation-owned stage's `#### Implementing Skills` is not `Manual (Gap)`.
- Every skill slug backticked under `#### Implementing Skills` resolves to an existing `.agents/skills/<slug>/SKILL.md`.
