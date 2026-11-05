---
name: remove-user
description: Remove a user fully from the system, the complement of setup-user: retire the record, clear assigned clients, hand over ownership and in-flight work, and have the operator confirm the user's external accounts are removed.
---

# remove-user

## When to use

Use this skill when a person stops using the application. It is the complement of `setup-user`: that skill sets a person up, and this one takes them out completely. To change a person's name, role, or clients while they stay, use `setup-user`.

## Boundaries

This skill covers `system/users.md`, the `## Owner` of records in `system/external-systems.md`, the `Responsible` cell of the user's in-flight rows in the assigned clients' `open-items.md`, and a non-secret confirmation that the user's external accounts are removed. A user record is never deleted: it is retired, because `AGENTS.md` forbids deleting a user and history keeps resolving the email. The skill does not remove accounts itself; the operator or the system's owner does, and the operator confirms.

- **Entry.** The operator names an `Active` user in `system/users.md` and gives their own email.
- **Graduation.** The user is `Retired` with `## Assigned Clients` of `None`, no `## Owner` in `system/external-systems.md` names the user, no in-flight row names the user as `Responsible`, every `Planned`, `Active`, or `Retired` external system has an account outcome, and `python3 scripts/check.py` passes with zero errors.
- **Removed.** Everything above holds and the skill ends.
- **Accounts pending.** The operator says an account is not yet removed. The record is still retired and the report lists the account as `pending` for the operator to finish.
- **Not found or already retired.** The email is not an `Active` user. Say so and stop.
- **Cancelled.** The operator does not approve the impact summary. No governed file is changed.

## Inputs

- The user email. Ask if it was not supplied, and list `Active` emails from `system/users.md` rather than guessing.
- Operator email address, asked once if it is not known.
- Approval of the impact summary, and the operator's choice of successor for each owned external system and each in-flight stage.
- For each external system, the operator's confirmation of the account outcome.

## Reads

- `formats/system/users.md`, `formats/system/external-systems.md`, and `formats/clients/open-items.md`.
- `system/users.md`, `system/user-roles.md`, `system/external-systems.md`, and `system/AGENTS.md`.
- For each slug in the user's `## Assigned Clients`, that client's `open-items.md` only, to find rows where `Responsible` is the user's email. No other client folder is read.
- `process/` stage files, to find the owning role slug of a stage a row is in.

## Procedure

1. **Confirm the user.** The email must be an `Active` heading in `system/users.md`. Otherwise stop.
2. **Scan the impact.** Build a summary with:
   - the user's primary role, and a warning when no other `Active` user holds that role;
   - each external system whose `## Owner` is this user;
   - each `# In Flight` row in an assigned client's `open-items.md` whose `Responsible` is this email, with its process, stage, and the stage's owning role slug (or `Automation`);
   - each `Planned`, `Active`, or `Retired` external system, with the account and access this user probably holds, derived from its `## Purpose`, `## Coordination Guidance`, `## User Connection`, and the user's role and clients.
3. **Get approval and choices.** Present the summary. Ask the operator to approve the removal and to choose, for each owned system, an `Active` user from `system/users.md` or `None` as the new owner. Each in-flight row returns to its stage's owning role slug, or `Automation` for an automation stage; the operator may instead name an `Active` user to take it. Do not write anything before approval.
4. **Walk the external accounts.** For each external system, one at a time, tell the operator which account and access to remove or disable (for example "remove the user from the workspace and revoke their API access"), then ask for the outcome: `removed`, `not applicable` (the user never had an account), or `pending` (the operator will finish it). Never ask for, accept, or write a password, token, or key. If one is pasted, ignore it.
5. **Retire the record.** In `system/users.md` set the user's `## Status` to `Retired`, `## Assigned Clients` to `None`, and add one line to `## Notes` that records the removal date (`Removed YYYY-MM-DD`) and, if any account is `pending`, that it is pending. Keep `## Primary Role`. Update the file header's `updated` and `updated_by`.
6. **Hand over ownership.** For each system the user owned, set `## Owner` to the operator's choice (an `Active` user's email heading, or `None`) and update that file's header.
7. **Hand back in-flight work.** For each approved row, set `Responsible` to the owning role slug, `Automation`, or the named `Active` user's email, set `Updated` to today, and update that client file's header. Edit only the user's rows, only in that user's assigned clients.
8. **Report and verify.** Write `tmp/remove-user-<email-slug>.md` (the email with `@` and `.` replaced by `-`) with the user email, the date, each owner change, each in-flight change, and one account outcome per system. Run `python3 scripts/check.py` and fix every error before reporting done. Tell the operator about any `pending` account.

## Writes

- `system/users.md`.
- `system/external-systems.md` when the user owned a system.
- `clients/<slug>/open-items.md` for assigned clients where the user held in-flight rows.
- `tmp/remove-user-<email-slug>.md`.

## Stops when

The operator approved, the user is `Retired` with `None` assigned clients, no owner or in-flight reference to the user remains, every external system has an account outcome in the temporary report, and `python3 scripts/check.py` passes with zero errors.

## Never

- Never delete the user record, a history row, or a decision-log row; retire by status.
- Never write before the operator approves the impact summary.
- Never store a credential in the repository, including `tmp/`.
- Never read or edit a client folder that is not in the user's `## Assigned Clients`.
- Never reassign an owner or in-flight row to a `Retired` user.
- Never report an account `removed` that the operator did not confirm.
