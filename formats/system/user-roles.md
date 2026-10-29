# Format: system/user-roles (version 1)

## Purpose

The discrete operational roles a person can hold. A role tells an agent what that person is doing: which processes and skills they use, and which tasks they take on. It is context for the agent, not a permissions model and not an access-control list.

## Location

`system/user-roles.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md` with `format: system/user-roles` and `format_version: 1`. No `client` key.

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
A bullet list of process slugs this role uses, one `- <slug>` per line, or `None`.

## Skills
A bullet list of skill slugs this role uses, one `- <slug>` per line, or `None`.

## Status
A Display Name from Role Statuses (`Active` or `Retired`).
```

## Rules

- These roles are separate from the process-participant vocabulary in `process/README.md`. Process documents still say Operator, Client, Reviewer, and Agent.
- A role does not grant or deny repository, Git host, or external-system access.
- A `Retired` role remains in the file and cannot be newly assigned.
- `## Processes` and `## Skills` name work the role performs. They are not a permission matrix.

## Vocabularies

Role Statuses:

| Display Name | Meaning |
| --- | --- |
| Active | The role can be assigned as a primary role. |
| Retired | The role remains for history and cannot be newly assigned. |

## Checks

- System header with `format: system/user-roles` and `format_version: 1`.
- The body is `None`, or every `#` heading is a unique lowercase kebab-case slug and contains `## Display Name`, `## Purpose`, `## Core Tasks`, `## Processes`, `## Skills`, and `## Status` in that order.
- `## Display Name` and `## Purpose` are not `None`. `## Status` is a Role Status Display Name.
- Every process bullet resolves to `process/<slug>.md`. Every skill bullet resolves to `.agents/skills/<slug>/SKILL.md`.
