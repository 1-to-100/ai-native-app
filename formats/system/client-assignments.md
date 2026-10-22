# Format: system/client-assignments (version 1)

## Purpose

The role-specific assignment of users to clients. Each row tells an agent to treat one user as one role in the context of one client. The record stores routing metadata only: who, which role, and which client slug.

## Location

`system/client-assignments.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md` with `format: system/client-assignments` and `format_version: 1`. No `client` key.

## Body

When no assignment exists yet, the body is the single line `None`. Otherwise each record uses an `# A-NNNN` heading, with `NNNN` a four-digit integer, and these `##` sections in order:

```markdown
# A-0001
## User
The exact email heading of a record in `system/users.md`.

## Role
The exact `#` heading of a record in `system/user-roles.md`.

## Client
The client slug, matching a folder under `clients/` or, for an ended assignment, under `archive/`.

## Status
A Display Name from Assignment Statuses (`Active` or `Ended`).

## Started
The date the assignment began, `YYYY-MM-DD`.

## Ended
The date the assignment ended, `YYYY-MM-DD`, or `None` while it is `Active`.

## Notes
Assignment-specific operating context, or `None`. Notes contain no client business facts, commercial terms, or comparison with another client.
```

## Rules

- Assignment headings are never reused or deleted. A role change ends the current row and adds a new `A-NNNN` row.
- At most one `Active` assignment exists for a given user and client pair.
- An `Active` assignment references an `Active` user, an `Active` role, a folder in `clients/<slug>/`, and `## Ended` of `None`.
- An `Ended` assignment has a date in `## Ended`. Its client slug may resolve to `clients/<slug>/` or `archive/<slug>/`.
- Client-specific work may read the assignment rows for the client being served. It does not list or describe assignments for other clients.
- This file does not copy client identity, entitlements, contacts, deliverables, or decisions from `clients/<slug>/`.

## Vocabularies

Assignment Statuses:

| Display Name | Meaning |
| --- | --- |
| Active | Treat the user as this role for this client now. |
| Ended | The assignment is historical and is no longer applied. |

## Checks

- System header with `format: system/client-assignments` and `format_version: 1`.
- The body is `None`, or every `#` heading matches `A-` plus four digits, is unique, and contains `## User`, `## Role`, `## Client`, `## Status`, `## Started`, `## Ended`, and `## Notes` in that order.
- `## User` matches a heading in `system/users.md`. `## Role` matches a heading in `system/user-roles.md`. `## Client` is a lowercase kebab-case slug that resolves to `clients/<slug>/` or `archive/<slug>/`.
- `## Status` is an Assignment Status Display Name. `## Started` is `YYYY-MM-DD`. `Active` rows have `## Ended` of `None`; `Ended` rows have a `YYYY-MM-DD` end date.
- No two `Active` rows share the same user and client. An `Active` row does not reference a `Retired` user or role, and its client folder is under `clients/`.
