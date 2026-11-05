---
name: whats-next
description: Find the in-flight process steps across a user's assigned clients that match the user's role, let the user take them on, and walk each one to its graduation criteria.
---

# whats-next

## When to use

Use this skill when a person asks what they should work on next. It reads the user's primary role and assigned clients, scans each assigned client's `open-items.md` for in-flight process runs whose current stage that role owns or backs up, lets the user choose, records them as responsible, and then executes each chosen stage. Use `client-status` to see one client's whole picture without taking anything on, and `review-open-issues` to resolve a client's open issues.

## Boundaries

- **Entry.** The user is an `Active` record in `system/users.md` with an `Active` primary role. At least one lifecycle stage file exists in `process/`, or the skill stops with nothing to offer.
- **Graduation.** Every step the user took on has been executed to its stage's graduation criteria or handed back with a status note, each touched `open-items.md` reflects the result, and `python3 scripts/check.py <slug>` passes for every client written.
- **Nothing matches.** No in-flight row across the user's assigned clients sits on a stage that the user's role owns or backs up, and none is already assigned to the user. Report that, mention how many `# Open` issues each assigned client has, and stop.
- **No assigned clients.** The user's `## Assigned Clients` is `None`. Stop and say the user has no client access.
- **Unknown user.** The email is not in `system/users.md`. Stop and point the operator to `setup-user`.
- **Automation stage.** An in-flight row whose current stage is Automation-owned is reported for information and never offered to a person.
- **Handed back.** The user stops a step before graduation. The row keeps the user as `Responsible` with a `Status Notes` entry saying where it stopped, so the next session resumes there.
- Client work reads only the clients listed in this user's `## Assigned Clients`. Other client slugs on user records are never read or recited.

## Inputs

- The user's email. If omitted, list the `Active` emails in `system/users.md` and ask the operator to pick one. Never guess.
- The user's choice of which offered steps to take on, in the order they want.
- Operator email address, asked once if it is not known. It goes in `updated_by`; the acting user's email goes in `Responsible`.

## Reads

- `system/users.md` (this user's record only), `system/user-roles.md`, and `system/AGENTS.md`.
- `process/README.md` and every lifecycle stage file in `process/`, for the `#### Owner`, `#### Entry Criteria`, `#### Graduation Criteria`, `#### Branching and Terminal Paths`, and `#### Implementing Skills` of each stage cited by an in-flight row.
- `formats/clients/open-items.md`.
- `clients/<slug>/open-items.md`, `clients/<slug>/client.md`, and `clients/<slug>/decision-log.md` for each assigned client.
- `.agents/skills/README.md` and the `SKILL.md` of each implementing skill it invokes.

## Procedure

1. **Resolve the user.** Confirm the email is an `Active` record in `system/users.md`. Note the `## Primary Role` and the `## Assigned Clients`. Stop on the Unknown user or No assigned clients boundary.
2. **Scan the assigned clients.** For each slug in `## Assigned Clients`, read `clients/<slug>/open-items.md` `# In Flight`. For each row, open the cited process in `process/` and its current stage's `#### Owner`. Classify the row as:
   - **Mine** when `Responsible` is this user's email.
   - **Owner match** when `Responsible` is a role slug and the user's primary role is the first role under `#### Owner`.
   - **Backup match** when the user's primary role is a later role under `#### Owner`.
   - **Automation** when the stage is Automation-owned.
   - Otherwise skip it.
3. **Present the list.** Show Mine first, then Owner matches, then Backup matches, each with the client slug, the process, the stage, the `Status Notes`, and the stage's `#### Entry Criteria` in one line. List Automation rows separately as information. Ask which steps the user takes on and in what order. Stop and wait for the answer. If the list is empty, stop on the Nothing matches boundary.
4. **Take each chosen step on.** Set the row's `Responsible` to the user's email and `Updated` to today. Set the file header's `updated` and `updated_by`. Run `python3 scripts/check.py <slug>`.
5. **Execute the stage.** Confirm the `#### Entry Criteria` hold from the client folder; if not, say what is missing and hand the step back with a status note. Otherwise invoke the stage's `#### Implementing Skills` in order for this client. When the stage is `Manual (Gap)`, walk the `#### Description` with the user, reading `decision-log.md` before asking a question the log may already answer, and do the work under `AGENTS.md` and the governing formats.
6. **Graduate or branch.** When the `#### Graduation Criteria` are met, either advance the row to the next `Stage N: <Name>` with `Responsible` reset to that stage's owning role slug (or `Automation`), or, when a terminal path in `#### Branching and Terminal Paths` was reached, move the row to `# Completed` with today's date, the path name as `Outcome`, and the final note. When a branch returns the run to an earlier stage, set `Stage` to that stage and `Responsible` to its owning role. Update `Updated`, `Status Notes`, and the header. Run `python3 scripts/check.py <slug>`.
7. **Continue** with the next chosen step until all are done or the user stops. Then write `tmp/whats-next-<email-slug>.md` (email with `@` and `.` replaced by `-`) listing each step taken on and its outcome, and run `python3 scripts/check.py`.

## Writes

- `clients/<slug>/open-items.md` for each assigned client where a step was taken on, advanced, handed back, or completed.
- Whatever the invoked implementing skills write for that client, under their own contracts.
- `tmp/whats-next-<email-slug>.md`.

## Stops when

The user has no assigned clients, is unknown, or nothing matches their role; or every chosen step has been executed to its graduation criteria or handed back with a status note, the temporary report is written, and `python3 scripts/check.py` passes with zero errors.

## Never

- Never guess the user, the role, or which step to take on.
- Never read or recite a client the user is not assigned, and never compare clients.
- Never offer an Automation-owned stage to a person.
- Never advance a row past a stage whose graduation criteria are not met.
- Never invent a client fact to satisfy entry or graduation criteria. Write `None` and open an issue in that client's `open-items.md`.
- Never delete an in-flight, completed, open, or closed row.
- Never write a client fact into `system/`.
