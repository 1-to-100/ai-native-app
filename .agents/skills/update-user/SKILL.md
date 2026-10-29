---
name: update-user
description: Add, edit, or retire a user and coordinate that person's primary role and assigned clients.
---

# update-user

## When to use

Use this skill when a person starts using the application, their name or primary role changes, their assigned clients change, or they stop using the application. Use `setup-application` instead when the change is the shared external-system list rather than a person.

## Boundaries

This skill covers `system/users.md` and `system/user-roles.md`. Shared installation of an external system belongs to `setup-application`. Connecting one person's accounts is `setup-my-integrations`. Teaching a person is `train-me`. This skill does not grant repository permissions and does not store secrets.

- **Entry.** The operator can name the person to add, edit, or retire. Role headings used in the change already exist in `system/user-roles.md`, or the operator is prepared to add the role in the same session.
- **Graduation.** The user row matches the operator's answers, the user's `## Assigned Clients` matches that answer, and `python3 scripts/check.py` passes with zero errors.
- **Recorded.** The user row matches the interview and the skill ends.
- **Role missing.** The named role is not in `system/user-roles.md`. Interview for the role's purpose, tasks, processes, and skills, write the role, and then continue the user change.
- **Cancelled.** The operator stops before approval. Do not leave a partial user write in place.

## Inputs

- The action: add, edit, or retire. Ask if the operator did not say which.
- The person's email address. For an edit or retirement, it must already be a heading in `system/users.md`.
- The person's name, primary role, and assigned clients when the action needs them.
- Operator email address, asked once if it is not known.

## Reads

- `formats/system/users.md` and `formats/system/user-roles.md`.
- `system/users.md`, `system/user-roles.md`, and `system/AGENTS.md`.
- `clients/README.md` and the client folder names under `clients/` and `archive/`.

## Procedure

1. **Identify the person and the action.** If the registry is `None`, only an add is possible. Confirm the email, the action, and the operator email.
2. **Interview.** Ask for the name, the primary role heading, and the client slugs the user is assigned (none is allowed). Read the existing record back and ask only for what is missing or changing. Do not invent a name, role, or client.
3. **Add a missing role first.** If the named role is not in `system/user-roles.md`, interview for its display name, purpose, core tasks, process slugs, and skill slugs. Write that role as `Active` before writing the user. Confirm each process and skill slug exists.
4. **Write the user.** For an add, create a `# <email>` record with `## Name`, `## Primary Role`, `## Assigned Clients` (`None` or one slug bullet per client), `## Status` of `Active`, and `## Notes` of `None` unless the operator supplied notes. For an edit, change only the fields the operator changed. Update the file header's `updated` and `updated_by`. Replace a `None` body with the first record rather than leaving `None` above the records.
5. **Assign clients.** Set `## Assigned Clients` to exactly the slugs the operator confirmed, one bullet each, or `None`. Every slug must be an existing folder under `clients/`. Add or remove slugs only as the operator confirmed.
6. **Retire.** Set the user's `## Status` to `Retired`. Set `## Assigned Clients` to `None`. Do not delete the user.
7. **Verify.** Show the operator the user record changed. Run `python3 scripts/check.py` and fix every error before reporting done.

## Writes

- `system/users.md`.
- `system/user-roles.md` when a role had to be created.

## Stops when

The operator confirms the add, edit, or retirement, the user record matches that confirmation, and `python3 scripts/check.py` passes with zero errors.

## Never

- Never delete a user or role.
- Never store a credential in the user notes.
- Never treat a role as a permission grant.
- Never invent a person, role, or client slug.
- Never copy client business facts into `system/users.md`.
- Never leave assigned clients on a `Retired` user.
