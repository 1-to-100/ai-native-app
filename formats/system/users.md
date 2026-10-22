# Format: system/users (version 1)

## Purpose

The directory of people who use this application. Each record identifies one person by email and maps that person to one primary operational role so an agent knows who is acting and what role context to apply.

## Location

`system/users.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md`: `title`, `format`, `format_version`, `created`, `created_by`, `updated`, and `updated_by`, with no `client` key. `format` is `system/users` and `format_version` is `1`.

## Body

When nobody is recorded yet, the body is the single line `None`. Otherwise each record is one `#` heading whose text is the person's email address, with these `##` sections in order:

```markdown
# person@example.com
## Name
The person's name as the operator supplied it.

## Primary Role
The exact `#` heading of one record in `system/user-roles.md`.

## Status
A Display Name from User Statuses (`Active` or `Retired`).

## Notes
Operational context that is not a secret, or `None`.
```

## Rules

- The record heading is the person's email address and is unique in this file.
- `## Primary Role` names a role heading, not the role's display name.
- An `Active` user references an `Active` role. A `Retired` user keeps the last role heading and is not deleted.
- Retiring a user is done through `update-user`, which also ends that user's `Active` rows in `system/client-assignments.md`.
- This file stores no password, token, recovery code, or other credential.
- Header emails may exist before the first user row is interviewed. Once this registry has any record, new `updated_by` values on system files should be an email in this file.

## Vocabularies

User Statuses:

| Display Name | Meaning |
| --- | --- |
| Active | The person currently uses the application and may receive new assignments. |
| Retired | The person no longer uses the application. Historical rows remain. |

## Checks

- System header with `format: system/users` and `format_version: 1`.
- The body is `None`, or every `#` heading is a unique email address and contains `## Name`, `## Primary Role`, `## Status`, and `## Notes` in that order.
- `## Name` is not `None`. `## Status` is a User Status Display Name. `## Primary Role` exactly matches a heading in `system/user-roles.md`.
- An `Active` user does not reference a `Retired` role.
- No record contains a credential-like value (`password`, `api_key`, `secret`, `token`, or a private-key block).
