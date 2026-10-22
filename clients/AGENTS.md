# AGENTS.md — clients/

One folder per client or primary entity, named by its slug (lowercase kebab-case). Required filenames are `client.md`, `open-issues.md`, and `decision-log.md`. They conform to `formats/clients/client.md`, `formats/clients/open-issues.md`, and `formats/clients/decision-log.md`.

- A client folder references only itself and shared repository catalogs. Never link, copy, or compare across client folders.
- `client.md` is the authoritative source for client identity, business overview, and commercial entitlements. Read it first, and do not restate those values in another document.
- `client.md` and the redacted `order-form.pdf` beside it (when commercial contracts apply) are the only places contact details appear.
- `open-issues.md` is the one place a client's unresolved questions and missing facts live. Closing an issue writes its answer into the document its `Area` names and appends one row to `decision-log.md` in the same change. The decision's `Source` is `open-issues #<id>`.
- `decision-log.md` is the only decisions table for the client. Rows are append-only. Before asking the operator a question during client work, read this log and proceed on a decision that already answers it.
- Client-specific work may read `system/users.md`, `system/user-roles.md`, `system/external-systems.md`, and the rows in `system/client-assignments.md` for this client slug only. It does not read other clients' assignments and does not write client facts into `system/`.
- A client who leaves is retired by moving the entire folder to `archive/<slug>/` at the repository root with a one-line `ARCHIVED.md` inside giving the date and reason. Nothing is deleted. Active assignments for that slug are ended, not deleted.
- Run `python3 scripts/check.py <slug>` before committing any change under a client folder.
