# Format: system/user-roles (version 2)

## Purpose

The discrete operational roles a person can hold. A role is a group of people who do the same kind of work. It tells an agent what that person is doing: which processes and skills they use, which process stages they own or back up, which processes they supervise, and which tasks they take on. It is context for the agent, not a permissions model and not an access-control list.

Fewer, well-defined roles are better. A role is not a job title, and the application does not need a role for every title in the organization. Several titles share one role when they do the same work; one person with several titles still holds one primary role. Add a role only when no existing role can own the work.

## Location

`system/user-roles.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md` with `format: system/user-roles` and `format_version: 2`. No `client` key.

## Body

When no role is recorded yet, the body is the single line `None`. Otherwise each record uses a lowercase kebab-case `#` heading and these `##` sections in order:

```markdown
# operator
## Display Name
The human-readable role name.

## Purpose
What responsibility this role carries in the application.

## Core Tasks
The recurring tasks and activities this role takes on. Write `None` only when the role has been named but its work is not yet described.

## Processes
A bullet list of the processes this role takes part in, one `- <Process Name>` per line using the exact `# <Process Name>` heading from a lifecycle stage file under `process/`, or `None`.

## Skills
A bullet list of skill slugs this role uses, one `- <slug>` per line, or `None`.

## Status
A Display Name from Role Statuses (`Active` or `Retired`).
```

## Rules

- A role slug is what a process stage's `#### Owner` and a process's `## Supervisor Role` name. Users whose `## Primary Role` is the first owner of a stage are that stage's default assignees.
- A role does not grant or deny repository, Git host, or external-system access.
- A `Retired` role remains in the file and cannot be newly assigned, cannot own or back up a stage, and cannot supervise a process.
- `## Processes` and `## Skills` name work the role performs. They are not a permission matrix.
- Keep the number of roles small. Before adding a role, `update-user` and `setup-application` check whether an existing role already covers the work.

## Vocabularies

Role Statuses:

| Display Name | Meaning |
| --- | --- |
| Active | The role can be assigned as a primary role and can own, back up, or supervise process stages. |
| Retired | The role remains for history and cannot be newly assigned. |

## Checks

- System header with `format: system/user-roles` and `format_version: 2`.
- The body is `None`, or every `#` heading is a unique lowercase kebab-case slug and contains `## Display Name`, `## Purpose`, `## Core Tasks`, `## Processes`, `## Skills`, and `## Status` in that order.
- `## Display Name` and `## Purpose` are not `None`. `## Status` is a Role Status Display Name.
- Every process bullet matches a `# <Process Name>` heading in a lifecycle stage file under `process/`. Every skill bullet resolves to `.agents/skills/<slug>/SKILL.md`.
