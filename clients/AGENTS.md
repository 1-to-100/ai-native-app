# AGENTS.md — clients/

One folder per client or primary entity, named by its slug (lowercase kebab-case). Filenames inside each folder mirror the format contracts in `formats/`.

- A client folder references only itself and shared repository catalogs. Never link, copy, or compare across client folders.
- `client.md` is the authoritative source for client identity, business overview, and commercial entitlements. Read it first, and do not restate those values in another document.
- `client.md` and the redacted `order-form.pdf` beside it (when commercial contracts apply) are the only places contact details appear.
- `open-issues.md` is the one place a client's unresolved questions and missing facts live. Closing an issue in `open-issues.md` means writing its answer into the document its `Area` names in the same commit.
- A client who leaves is retired by moving the entire folder to `archive/<slug>/` at the repository root with a one-line `ARCHIVED.md` inside giving the date and reason. Nothing is deleted.
- Run `python3 scripts/check.py <slug>` before committing any change under a client folder.
