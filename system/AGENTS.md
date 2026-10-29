# AGENTS.md — system/

This directory holds application-wide data shared across the repository. Every governed file here conforms to a contract in `formats/system/`.

- `system/` may store people, roles, external-system guidance, the optional products and services catalog, the application backlog, and the question journal.
- `system/users.md` may store, in each user's `## Assigned Clients`, client slugs as routing metadata. It must not store client business facts, commercial terms, contacts, deliverables, order forms, decisions, or comparisons between clients.
- An agent doing client-specific work may read `system/users.md`, `system/user-roles.md`, and `system/external-systems.md`, and only the assigned-client entries that equal the client being served. It does not read or recite other client slugs from a user record.
- `system/products-and-services.md` describes what the organization sells in general. It names no client and holds no price negotiated for one client.
- Client-specific work never writes a client fact into `system/`.
- Users, roles, backlog items, and journal rows are not deleted. Retire a user or role, remove an assigned client, or close a backlog or journal row.
- Never store a credential, API key, token, password, or unredacted payment number in this directory. External-system guidance names the setup step, not the secret.
- `updated` and `updated_by` change on every edit to a governed file here. `created_by` and `updated_by` are the human operator's email.
- Run `python3 scripts/check.py` after any edit here.
