# Format: system/external-systems (version 1)

## Purpose

The list of external systems this application coordinates with, such as a work tracker, CRM, email system, or calendar. Each record says what the system is for and how agents should coordinate with it. It does not store credentials or per-user grants.

## Location

`system/external-systems.md`. One repository-wide registry.

## Header

The system header defined in `formats/README.md` with `format: system/external-systems` and `format_version: 1`. No `client` key.

## Body

When no external system is recorded yet, the body is the single line `None`. Otherwise each record uses a lowercase kebab-case `#` heading and these `##` sections in order:

```markdown
# jira
## Display Name
The product or service name.

## Category
A Display Name from System Categories.

## Status
A Display Name from System Statuses (`Planned`, `Active`, or `Retired`).

## Purpose
Why agents in this application coordinate with this system.

## Coordination Guidance
How an agent should use the system: what belongs there, what stays in this repository, and any boundary the operator stated. Write `None` until the operator supplies it.

## System Administration
The shared installation or administration steps required before any user can connect, such as installing an integration, approving an app, or choosing a workspace. Write `None` until those steps are known. Never include a secret value.

## User Connection
How one user connects their own account and permissions in the agent environment. `setup-my-integrations` follows this guidance. Write `None` until the operator supplies it. Never include a secret value.

## Owner
The email heading of a user in `system/users.md` who owns the shared setup, or `None`.
```

## Rules

- `setup-application` records the systems the operator wants and completes `## System Administration` for shared setup.
- `setup-my-integrations` follows `## User Connection` for one person and does not write tokens, passwords, or API keys back into this file.
- A `Retired` system stays in the file. Agents do not start new coordination with it.
- Client-specific account identifiers, if a domain later needs them, belong in a client format. They are not copied here.

## Vocabularies

System Categories:

| Display Name | Meaning |
| --- | --- |
| Work Management | Trackers and project systems such as Jira or Asana. |
| CRM | Customer or pipeline systems such as Salesforce. |
| Email | Email sending, receiving, or mailbox systems. |
| Calendar | Calendar and scheduling systems. |
| Files | External file or document stores. |
| Analytics | Measurement or reporting systems. |
| Identity | Login, directory, or single-sign-on systems. |
| Other | A system that fits none of the categories above. |

System Statuses:

| Display Name | Meaning |
| --- | --- |
| Planned | The operator wants coordination, and shared setup is not finished. |
| Active | Shared setup is complete enough for user connections and agent coordination. |
| Retired | The application no longer coordinates with this system. |

## Checks

- System header with `format: system/external-systems` and `format_version: 1`.
- The body is `None`, or every `#` heading is a unique lowercase kebab-case slug and contains `## Display Name`, `## Category`, `## Status`, `## Purpose`, `## Coordination Guidance`, `## System Administration`, `## User Connection`, and `## Owner` in that order.
- `## Display Name` and `## Purpose` are not `None`. `## Category` and `## Status` match their vocabularies.
- `## Owner` is `None` or an email heading in `system/users.md`.
- No section contains a credential-like value (`password`, `api_key`, `secret`, `token`, or a private-key block).
