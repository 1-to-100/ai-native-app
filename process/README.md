# Processes — inventory

The governing process documents for this repository. Every process is broken into discrete, handoff-sized stages governed by `formats/system/process.md`: each stage declares its entry criteria, description, graduation criteria, branching or terminal paths, and the skill or skills that execute it. Read the process before running any skill it names. The rules for this directory live in `process/AGENTS.md`.

## The processes

| Process | Governs | Cadence | System of Record | Runs on |
| --- | --- | --- | --- | --- |
| [`application-lifecycle.md`](application-lifecycle.md) | Configuring this repository, upgrading it to the current template paradigm, and evolving its mechanisms | On operator request for setup or upgrade, and continuously for improvement | `Repository Markdown` | `setup-application`, `upgrade-app`, `improve-process` |
| [`client-lifecycle.md`](client-lifecycle.md) | Onboarding a client and resolving that client's open issues into the decision log | Once per new client, then whenever open issues are reviewed | `Repository Markdown` | `setup-client`, `review-open-issues` |
| [`user-administration.md`](user-administration.md) | Maintaining users and role assignments, connecting a user's integrations, and teaching a user the application | When users, connections, or training are requested | `Repository Markdown` | `update-user`, `setup-my-integrations`, `train-me` |
| [`backlog-management.md`](backlog-management.md) | Capturing later application changes and refining one backlog item until `improve-process` can implement it | Whenever a future change is captured or a backlog item is selected | `Repository Markdown` | `add-to-backlog`, `process-backlog` |
| [`question-review.md`](question-review.md) | Turning questions an agent had to ask into process or prompting changes | When the question journal has open rows | `Repository Markdown` | `review-question-journal` |

## Where a process sits

```text
AGENTS.md        the Global Context and universal boundaries (highest authority)
process/         how the business runs stage by stage        (who, when, entry/graduation criteria, branches)
formats/         what each document holds                    (the format wins on document structure)
system/          application-wide shared records             (users, roles, assignments, integrations, backlog, journal)
.agents/skills/  how an agent executes one stage             (the procedure)
scripts/         what is enforced mechanically               (the lint)
```

A process names the skill that executes each stage and the format each written outcome lands in. A stage without a skill is marked `Manual (Gap)` under `### Implementing Skills` so the gap is explicit.

## Shape of a process

Every process document in this directory conforms to [`formats/system/process.md`](../formats/system/process.md) and carries these ten `#` sections in exact order:

1. `# Purpose`
2. `# Scope`
3. `# Roles`
4. `# Cadence`
5. `# System of Record` (`## Mode`, `## Location`)
6. `# Inputs`
7. `# Stages` (`## Stage N: <Name>` with `### Entry Criteria`, `### Description`, `### Graduation Criteria`, `### Branching and Terminal Paths`, and `### Implementing Skills`)
8. `# Outputs`
9. `# Rules`
10. `# Related`

## Roles

The base role vocabulary every process uses. `system/user-roles.md` records operational roles for agent context and does not replace this vocabulary. `setup-application` and `improve-process` add domain-specific process roles here when a process needs them.

| Role | In a process |
| --- | --- |
| Operator | The person who runs a skill, reviews proposals, approves gates, and edits documents. Writes their own email in `created_by` and `updated_by`. |
| Client | The customer or stakeholder served by the application. Makes client decisions and does not operate the repository directly. |
| Reviewer | A human owner or fresh-context agent that verifies an artifact against its format and process contract without having drafted it. |
| Agent | Claude, OpenAI Codex, or Gemini executing a skill at an Operator's direction. Never an actor in a document header. |
