---
name: setup-user
description: Add or edit a user, coordinate that person's primary role and assigned clients, and have the operator validate that the user's external-system accounts exist. Front end for setting up a user.
---

# setup-user

## When to use

Use this skill when a person starts using the application, their name or primary role changes, or their assigned clients change. It is the front end for setting up a user and their accounts. To stop a person using the application, use `remove-user`. Use `setup-application` instead when the change is the shared external-system list rather than a person.

## Boundaries

This skill covers `system/users.md` and `system/user-roles.md`, and a non-secret check of the user's external accounts. Shared installation of an external system belongs to `setup-application`. Connecting one person's own accounts in the agent environment is `setup-my-integrations`. Teaching a person is `train-me`. Removing a person is `remove-user`. This skill does not grant repository permissions, does not create the external accounts itself, and does not store secrets.

- **Entry.** The operator can name the person to add or edit. Role headings used in the change already exist in `system/user-roles.md`, or the operator is prepared to add the role in the same session.
- **Graduation.** The user row matches the operator's answers, the user's `## Assigned Clients` matches that answer, every `Planned` or `Active` external system has an account outcome, and `python3 scripts/check.py` passes with zero errors.
- **Recorded.** The user row matches the interview, the account check is done, and the skill ends.
- **Role missing.** The named role is not in `system/user-roles.md`. Interview for the role's purpose, tasks, processes, and skills, write the role, and then continue the user change.
- **Retirement requested.** Hand the operator to `remove-user` and stop. This skill never retires a user.
- **Accounts pending.** The operator says a needed account does not exist yet. The report lists it as `needs creating`, and the skill still ends once the user row is recorded.
- **Cancelled.** The operator stops before approval. Do not leave a partial user write in place.

## Inputs

- The action: add or edit. Ask if the operator did not say which.
- The person's email address. For an edit, it must already be a heading in `system/users.md`.
- The person's name, primary role, and assigned clients when the action needs them.
- For each external system, the operator's confirmation of whether the user's account exists.
- Operator email address, asked once if it is not known.

## Reads

- `formats/system/users.md`, `formats/system/user-roles.md`, and `formats/system/external-systems.md`.
- `system/users.md`, `system/user-roles.md`, `system/external-systems.md`, and `system/AGENTS.md`.
- `clients/README.md` and the client folder names under `clients/` and `archive/`.

## Procedure

1. **Identify the person and the action.** If the registry is `None`, only an add is possible. Confirm the email, the action, and the operator email. If the operator asks to retire the person, point them to `remove-user` and stop.
2. **Interview.** Ask for the name, the primary role heading, and the client slugs the user is assigned (none is allowed). Read the existing record back and ask only for what is missing or changing. Do not invent a name, role, or client.
3. **Add a missing role first.** If the named role is not in `system/user-roles.md`, first ask whether an existing `Active` role already covers the work; fewer, well-defined roles are better, and a role is a group of people who do the same work, not a job title. Only when none fits, interview for its display name, purpose, core tasks, process names, and skill slugs. Write that role as `Active` before writing the user. Confirm each process name matches a `# <Process Name>` heading in `process/` and each skill slug exists.
4. **Write the user.** For an add, create a `# <email>` record with `## Name`, `## Primary Role`, `## Assigned Clients` (`None` or one slug bullet per client), `## Status` of `Active`, and `## Notes` of `None` unless the operator supplied notes. For an edit, change only the fields the operator changed. Update the file header's `updated` and `updated_by`. Replace a `None` body with the first record rather than leaving `None` above the records.
5. **Assign clients.** Set `## Assigned Clients` to exactly the slugs the operator confirmed, one bullet each, or `None`. Every slug must be an existing folder under `clients/`. Add or remove slugs only as the operator confirmed.
6. **Validate external accounts.** Read `system/external-systems.md`. If it is `None` or has no `Planned` or `Active` record, say there is nothing to validate and go to step 7. Otherwise, for each `Planned` or `Active` system, one at a time:
   1. Using the system's `## Purpose`, `## Coordination Guidance`, `## Data Mapping`, `## User Connection`, and the user's primary role and assigned clients, state in plain words which account and access this user needs in that system, or that none is needed.
   2. Ask the operator to validate it: `confirmed` (the account exists with that access), `needs creating` (it does not exist yet, so the operator or the system's owner creates it), or `not needed`. For a `Planned` system, record the account need and note that shared administration is unfinished and belongs to `setup-application`.
   3. Never ask for, accept, or write a password, token, or key. If one is pasted, ignore it and tell the user to keep it in the agent environment's credential store.
   Write `tmp/setup-user-<email-slug>.md` (the email with `@` and `.` replaced by `-`) with the user email, the date, and one outcome and short note per system.
7. **Verify and hand off.** Show the operator the user record changed and the account outcomes. Run `python3 scripts/check.py` and fix every error before reporting done. Then tell the operator the next steps: `setup-my-integrations` for the user's own connections (and for each `needs creating` account once it exists) and `train-me` for the new user.

## Writes

- `system/users.md`.
- `system/user-roles.md` when a role had to be created.
- `tmp/setup-user-<email-slug>.md`.

## Stops when

The operator confirms the add or edit, the user record matches that confirmation, every `Planned` or `Active` external system has an account outcome in the temporary report (or there were none), and `python3 scripts/check.py` passes with zero errors.

## Never

- Never delete or retire a user here; retirement belongs to `remove-user`.
- Never store a credential in the user notes or the temporary report.
- Never treat a role as a permission grant.
- Never create a role for a title when an existing role already does that work.
- Never invent a person, role, client slug, or external account.
- Never copy client business facts into `system/users.md`.
- Never mark an external system `Active`, or edit its record, from this skill.
