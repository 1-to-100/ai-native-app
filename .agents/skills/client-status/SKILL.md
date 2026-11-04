---
name: client-status
description: Report everything in flight, open, and recently completed for one client from its open-items.md, without changing any governed file.
---

# client-status

## When to use

Use this skill before a client meeting, a handoff, or a check-in to see the whole picture for one client: every process run in flight with its stage and responsible party, every open issue, and what recently completed. It reads and reports. Use `whats-next` to take a step on, and `review-open-issues` to resolve an issue.

## Boundaries

- **Entry.** `clients/<slug>/` exists with `open-items.md` created by `setup-client`.
- **Graduation.** The overview has been presented in chat and written to `tmp/client-status-<slug>.md`. No governed file changed.
- **Nothing in flight.** `# In Flight` is `None`. Say so, still report the open issues and recent completions, and stop.
- **Unknown client.** The slug is not a folder under `clients/`. Stop and ask the operator to pick a listed slug.
- **Stale row.** An in-flight row cites a process or stage that no lifecycle stage file defines, or a `Responsible` that does not fit the stage. Report it as a finding; do not fix it here.
- Client work reads only this client's slug in the users' `## Assigned Clients` in `system/users.md`.

## Inputs

- A client slug. If omitted, list the folders under `clients/` and ask the operator to pick one. Never guess.

## Reads

- `formats/clients/open-items.md` and `formats/system/process.md`.
- `clients/<slug>/open-items.md`, `clients/<slug>/client.md`, and `clients/<slug>/decision-log.md`.
- `process/README.md` and the lifecycle stage files that define the processes cited by in-flight rows, for each cited stage's `#### Owner`, `#### Graduation Criteria`, and `#### Implementing Skills`.
- `system/users.md` for the names of users named in `Responsible`, and `system/user-roles.md` for the display names of owning roles. Do not read other client slugs from user records.

## Procedure

1. **Resolve the slug.** If `clients/<slug>/` does not exist, stop and list the available slugs.
2. **Read the open items.** Read `# In Flight`, `# Completed`, and `# Open`. Read `client.md` for the client's name and the engagement start date.
3. **Resolve each in-flight row.** For each row, open the cited process and current stage. Note the lifecycle stage file it lives in, the stage's owning role and backups (or its Automation mode), what graduation requires, and the implementing skill. Resolve `Responsible` to a user's name when it is an email, or to the role's display name when it is a role slug.
4. **Present the overview.** In chat, grouped by lifecycle stage and then by process, list each in-flight run with its stage, responsible party, `Updated` date, status notes, and what graduation requires. Then list each `# Open` issue with its area and next step. Then list `# Completed` rows from the last ninety days, newest first. Flag any stale row as a finding. State the counts on one line each.
5. **Write the report.** Write the same overview to `tmp/client-status-<slug>.md` with the date.

## Writes

- `tmp/client-status-<slug>.md` only.

## Stops when

The overview has been presented and the temporary report written, or the slug is unknown.

## Never

- Never guess the client slug.
- Never edit `open-items.md`, `decision-log.md`, or any other governed file in this skill.
- Never invent a status, a date, or a reason; report what the rows say and name gaps as findings.
- Never read or mention another client's folder or assigned users.
