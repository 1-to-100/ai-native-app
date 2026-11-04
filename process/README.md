# Processes — inventory

Domain workflows for this repository, grouped into customer lifecycle stage files. The skills that ship with the template carry their own entry criteria, graduation criteria, and branches, and they do not have process documents here. The rules for this directory live in `process/AGENTS.md`.

## Lifecycle stage files

A lifecycle stage is one phase of the customer lifecycle. Each one the operator defines gets a file at the root of this directory, `process/<lifecycle-slug>.md`, governed by `formats/system/process.md`. Lifecycle stages are optional and named however the operator decides; typical names are `marketing.md`, `sales.md`, `onboarding.md`, `account-management.md`, and `delivery.md`. The template ships none.

Each lifecycle stage file holds one or more `# <Process Name>` sections. A process is a core activity of that lifecycle stage, and its name is unique across every file in this directory: that exact heading text is how roles, the question journal, and each client's `open-items.md` refer to it.

## The processes

| Lifecycle Stage | Process | Supervisor Role | Cadence | System of Record |
| --- | --- | --- | --- | --- |
| None | — | — | — | — |

## Where a process sits

```text
AGENTS.md        the Global Context and universal boundaries (highest authority)
process/         lifecycle stage files holding the business processes (who owns each stage, when, entry/graduation criteria, branches)
formats/         what each document holds                    (the format wins on document structure)
system/          application-wide shared records             (users and their assigned clients, roles, integrations, backlog, journal)
.agents/skills/  how an agent executes the work              (shipped skills include their own stage rules)
scripts/         what is enforced mechanically               (the lint)
```

A process names the skill that executes each stage and the format each written outcome lands in. A stage without a skill is marked `Manual (Gap)` under `#### Implementing Skills` so the gap is explicit.

## Shape of a process

Every process section conforms to [`formats/system/process.md`](../formats/system/process.md) and carries these ten `##` sections in exact order:

1. `## Purpose`
2. `## Scope`
3. `## Supervisor Role`
4. `## Cadence`
5. `## System of Record` (`### Mode`, `### Location`)
6. `## Inputs`
7. `## Stages` (`### Stage N: <Name>` with `#### Entry Criteria`, `#### Owner`, `#### Description`, `#### Graduation Criteria`, `#### Branching and Terminal Paths`, and `#### Implementing Skills`)
8. `## Outputs`
9. `## Rules`
10. `## Related`

## Ownership

A process is a series of stages, and every stage is owned.

- **Role-owned stages.** `#### Owner` lists one or more role slugs from `system/user-roles.md`. The first role owns the stage: users whose primary role it is are the default assignees, and `whats-next` offers the stage to them first. Every later role is a backup, offered second. The owning role coordinates its backups outside the system.
- **Automation-owned stages.** `#### Owner` is `Automation: On-Demand` or `Automation: Recurring (<schedule>)`. An Automation is a standardized, agent-executable approach to the stage. It needs no human interaction and the agent runs it independently: on request for On-Demand, or on the written schedule for Recurring, which the agent environment runs as a scheduled task. An Automation stage always names an implementing skill.
- **Supervisor Role.** Every process names one role responsible for checking that the process is executed properly. The supervisor checks; the stage owners do the work.

Each client's run of a process is tracked as an `# In Flight` row in `clients/<slug>/open-items.md`, holding the current stage and the responsible party. `whats-next` matches those rows to a user's role, and `client-status` reports them for one client.

## Roles

Stage owners, backups, and supervisors are the operational roles in `system/user-roles.md`, referenced by slug. Fewer, well-defined roles are better: a role is a group of people who do the same work, not a job title, and the application does not need a role for every title. Before a process introduces a new role, check whether an existing one already does that work. Prose inside a stage may still speak of the client, a reviewer, or the agent; those are not roles in the system.
