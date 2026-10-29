# Format: system/users (version 2)

## Purpose

The directory of people who use this application. Each record identifies one person by email and maps that person to one primary operational role and, optionally, to the clients that person works on, so an agent knows who is acting, what role context to apply, and which client folders that person may serve.

## Location

`system/users.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md`: `title`, `format`, `format_version`, `created`, `created_by`, `updated`, and `updated_by`, with no `client` key. `format` is `system/users` and `format_version` is `2`.

## Body

When nobody is recorded yet, the body is the single line `None`. Otherwise each record is one `#` heading whose text is the person's email address, with these `##` sections in order:

```markdown
# person@example.com
## Name
The person's name as the operator supplied it.

## Primary Role
The exact `#` heading of one record in `system/user-roles.md`.

## Assigned Clients
The single line `None`, or a bullet list with one client slug per line, each matching a folder under `clients/`. The list is the user's access to those clients.

## Status
A Display Name from User Statuses (`Active` or `Retired`).

## Notes
Operational context that is not a secret, or `None`.
```

## Rules

- The record heading is the person's email address and is unique in this file.
- `## Primary Role` names a role heading, not the role's display name.
- An `Active` user references an `Active` role. A `Retired` user keeps the last role heading and is not deleted.
- `## Assigned Clients` is routing metadata only: client slugs and nothing else about those clients. A slug appears at most once per user.
- A user serves a client in their primary role. A user with `None` assigned clients has no client access.
- Retiring a user is done through `update-user`, which also sets that user's `## Assigned Clients` to `None`. Archiving a client removes its slug from every user's list.
- This file stores no password, token, recovery code, or other credential.
- Header emails may exist before the first user row is interviewed. Once this registry has any record, new `updated_by` values on system files should be an email in this file.

## Vocabularies

User Statuses:

| Display Name | Meaning |
| --- | --- |
| Active | The person currently uses the application and may be assigned clients. |
| Retired | The person no longer uses the application. Historical rows remain. |

## Checks

- System header with `format: system/users` and `format_version: 1`.
- The body is `None`, or every `#` heading is a unique email address and contains `## Name`, `## Primary Role`, `## Assigned Clients`, `## Status`, and `## Notes` in that order.
- `## Name` is not `None`. `## Status` is a User Status Display Name. `## Primary Role` exactly matches a heading in `system/user-roles.md`.
- An `Active` user does not reference a `Retired` role.
- `## Assigned Clients` is `None` or a bullet list of unique, lowercase kebab-case slugs, each resolving to `clients/<slug>/`. A `Retired` user has `None`.
- No record contains a credential-like value (`password`, `api_key`, `secret`, `token`, or a private-key block).
