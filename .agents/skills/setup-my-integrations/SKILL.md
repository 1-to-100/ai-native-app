---
name: setup-my-integrations
description: Walk one user through connecting their own external-system accounts in the agent environment, without storing secrets.
---

# setup-my-integrations

## When to use

Use this skill when one person needs to connect the external systems this application already lists. This is that person's own accounts and permissions in the agent environment. Shared installation and workspace administration belong to `setup-application`.

## Inputs

- The user email. Ask if it was not supplied, and list emails from `system/users.md` rather than guessing.
- Access to the agent environment where that user will approve the connections.
- Operator email address, asked once if a governed file is updated. This skill normally writes only a temporary report.

## Reads

- `process/user-administration.md` Stage 2.
- `formats/system/external-systems.md` and `system/external-systems.md`.
- `system/users.md`, to confirm the person exists and is `Active`.
- `system/AGENTS.md`.

## Procedure

1. **Confirm the user.** The email must be an `Active` heading in `system/users.md`. If the registry is `None` or the email is missing, stop and point the operator to `update-user`.
2. **List the systems.** Read `system/external-systems.md`. If it is `None`, or it has no `Planned` or `Active` record, stop and say there is nothing to connect.
3. **Walk one system at a time.** For each `Active` system, follow `## User Connection` with the user. For each `Planned` system, do not invent a connection. Tell the operator that shared administration is unfinished and point them to `setup-application`.
4. **Record a non-secret outcome.** For each system, record one of `connected`, `skipped`, or `blocked`, plus a short note in the operator's words. If the user pastes a token, password, or key, do not write it down. Tell them to keep it in the agent environment's own credential store and continue without that value.
5. **Write the report.** Write `tmp/setup-my-integrations-<email-slug>.md`, using the email with `@` and `.` replaced by `-`. Include the user email, the date, and one outcome per system. Do not update `system/external-systems.md` unless the operator separately corrects shared guidance, which is a `setup-application` change.

## Writes

- `tmp/setup-my-integrations-<email-slug>.md`.

## Stops when

Every `Active` system has an outcome of connected, skipped, or blocked, every `Planned` system was reported as blocked on shared setup, and the temporary report contains no secret.

## Never

- Never write a credential, token, password, or API key into the repository, including `tmp/`.
- Never mark a system `Active` from this skill. Shared setup status belongs to `setup-application`.
- Never connect a system that is not listed in `system/external-systems.md`.
- Never perform the connection for a user email that is not an `Active` user.
