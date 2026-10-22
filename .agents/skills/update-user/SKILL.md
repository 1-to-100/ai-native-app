---
name: update-user
description: Add, edit, or retire a user and coordinate that person's primary role and client assignments.
---

# update-user

## When to use

Use this skill when a person starts using the application, their name or primary role changes, their client assignments change, or they stop using the application. Use `setup-application` instead when the change is the shared external-system list rather than a person.

## Inputs

- The action: add, edit, or retire. Ask if the operator did not say which.
- The person's email address. For an edit or retirement, it must already be a heading in `system/users.md`.
- The person's name, primary role, and client assignments when the action needs them.
- Operator email address, asked once if it is not known.

## Reads

- `process/user-administration.md` Stage 1.
- `formats/system/users.md`, `formats/system/user-roles.md`, and `formats/system/client-assignments.md`.
- `system/users.md`, `system/user-roles.md`, `system/client-assignments.md`, and `system/AGENTS.md`.
- `clients/README.md` and the client folder names under `clients/` and `archive/`.

## Procedure

1. **Identify the person and the action.** If the registry is `None`, only an add is possible. Confirm the email, the action, and the operator email.
2. **Interview.** Ask for the name, the primary role heading, and each client assignment as a client slug plus a role heading. Read the existing rows back and ask only for what is missing or changing. Do not invent a name, role, or client.
3. **Add a missing role first.** If the named role is not in `system/user-roles.md`, interview for its display name, purpose, core tasks, process slugs, and skill slugs. Write that role as `Active` before writing the user. Confirm each process and skill slug exists.
4. **Write the user.** For an add, create a `# <email>` record with `## Name`, `## Primary Role`, `## Status` of `Active`, and `## Notes` of `None` unless the operator supplied notes. For an edit, change only the fields the operator changed. Update the file header's `updated` and `updated_by`. Replace a `None` body with the first record rather than leaving `None` above the records.
5. **Coordinate assignments.** For each client assignment the operator confirmed:
   - If no `Active` row exists for that user and client, append the next unused `A-NNNN` row with `## Status` of `Active`, `## Started` of today, and `## Ended` of `None`.
   - If an `Active` row exists for the same user, client, and role, leave it.
   - If an `Active` row exists for the same user and client with a different role, set that row to `Ended` with `## Ended` of today and append a new `Active` row. Do not rewrite the old row's role.
   The client slug must be an existing folder under `clients/`.
6. **Retire.** Set the user's `## Status` to `Retired`. End every `Active` assignment for that email with today's date. Do not delete the user or the assignment rows.
7. **Verify.** Show the operator the user row and the assignment rows changed. Run `python3 scripts/check.py` and fix every error before reporting done.

## Writes

- `system/users.md`.
- `system/user-roles.md` when a role had to be created.
- `system/client-assignments.md` when assignments were added or ended.

## Stops when

The operator confirms the add, edit, or retirement, the user and assignment rows match that confirmation, and `python3 scripts/check.py` passes with zero errors.

## Never

- Never delete a user, role, or assignment row.
- Never store a credential in the user or assignment notes.
- Never treat a role as a permission grant.
- Never invent a person, role, client slug, or assignment.
- Never copy client business facts into `system/client-assignments.md`.
- Never leave an `Active` assignment in place for a `Retired` user.
