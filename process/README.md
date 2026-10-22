# Processes — inventory

Domain workflows for this repository. The skills that ship with the template carry their own entry criteria, graduation criteria, and branches, and they do not have process documents here. A workflow added for the business gets `process/<slug>.md`, governed by `formats/system/process.md`. The rules for this directory live in `process/AGENTS.md`.

## The processes

| Process | Governs | Cadence | System of Record | Runs on |
| --- | --- | --- | --- | --- |
| None | — | — | — | — |

## Where a process sits

```text
AGENTS.md        the Global Context and universal boundaries (highest authority)
process/         domain workflows added for this business     (who, when, entry/graduation criteria, branches)
formats/         what each document holds                    (the format wins on document structure)
system/          application-wide shared records             (users, roles, assignments, integrations, backlog, journal)
.agents/skills/  how an agent executes the work              (shipped skills include their own stage rules)
scripts/         what is enforced mechanically               (the lint)
```

A domain process names the skill that executes each stage and the format each written outcome lands in. A stage without a skill is marked `Manual (Gap)` under `### Implementing Skills` so the gap is explicit.

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

The base role vocabulary a domain process uses. `system/user-roles.md` records operational roles for agent context and does not replace this vocabulary. `setup-application` and `improve-process` add domain-specific process roles here when a process needs them.

| Role | In a process |
| --- | --- |
| Operator | The person who runs a skill, reviews proposals, approves gates, and edits documents. Writes their own email in `created_by` and `updated_by`. |
| Client | The customer or stakeholder served by the application. Makes client decisions and does not operate the repository directly. |
| Reviewer | A human owner or fresh-context agent that verifies an artifact against its format and process contract without having drafted it. |
| Agent | Claude, OpenAI Codex, or Gemini executing a skill at an Operator's direction. Never an actor in a document header. |
