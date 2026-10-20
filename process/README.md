# Processes — inventory

The governing process documents for this repository. Every process is broken into discrete, handoff-sized stages governed by `formats/process.md`: each stage declares its entry criteria, description, graduation criteria, branching/terminal paths, and the skill(s) that execute it. Read the process before running any skill it names. The rules for this directory live in `process/AGENTS.md`.

## The processes

| Process | Governs | Cadence | System of Record | Runs on |
| --- | --- | --- | --- | --- |
| [`application-lifecycle.md`](application-lifecycle.md) | Bootstrapping this repository into a tailored AI application, onboarding clients or entities onto the line, and continuously evolving the mechanisms as operational friction is discovered | Once at bootstrap (`Stage 1`), per new client/entity (`Stage 2`), and continuously on operator feedback (`Stage 3`) | `Repository Markdown` | `create-application`, `setup-client`, `improve-process` |

## Where a process sits

```text
AGENTS.md        the Global Context and universal boundaries (highest authority)
process/         how the business runs stage by stage        (who, when, entry/graduation criteria, branches)
formats/         what each document holds                    (the format wins on document structure)
.agents/skills/  how an agent executes one stage             (the procedure)
scripts/         what is enforced mechanically               (the lint)
```

A process names the skill that executes each stage and the format each written outcome lands in. A stage without a skill is marked `Manual (Gap)` under `### Implementing Skills` so the gap is explicit and never improvised around silently.

## Shape of a process

Every process document in this directory conforms to [`formats/process.md`](../formats/process.md) and carries these ten `#` sections in exact order:
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

The base role vocabulary every process uses (`create-application` and `improve-process` add domain-specific roles here when needed):

| Role | In a process |
| --- | --- |
| Operator | The founder or team member who runs a skill, reviews proposals, approves gates, and edits documents. Writes their own email in `created_by` and `updated_by`. |
| Client | The customer or stakeholder served by the application. Makes client decisions; never operates the repository directly. |
| Reviewer | A human owner or fresh-context agent that verifies an artifact against its format and process contract without having drafted it. |
| Agent | Claude, OpenAI Codex, or Gemini executing a skill at an Operator's direction. Never an actor in a document header. |
