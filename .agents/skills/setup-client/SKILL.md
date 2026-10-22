---
name: setup-client
description: Build a complete client folder under clients/ from an onboarding handoff file, walk the Setup Ledger with the operator, and validate with check.py.
---

# setup-client

## When to use

A client or primary business entity is ready to be onboarded, and a handoff file conforming to `formats/clients/handoff.md` is ready. This skill reads the handoff, its sibling folder, and this repository. Run it once per client.

## Boundaries

This skill creates `clients/<slug>/` and walks the Setup Ledger. It does not discover prospects, negotiate commercial terms, or change application mechanisms. Mechanism changes go to `improve-process`. Later review of open issues is `review-open-issues`.

- **Entry.** A handoff file in `clients/handoff` format, plus any sibling asset folder and redacted `order-form.pdf`, for a client slug that does not yet exist in `clients/` or `archive/`.
- **Graduation.** Every Setup Ledger entry is written into its target document or recorded as an `# Open` row. Every `# Closed` row has a matching decision-log row. `clients/README.md` includes the client. `python3 scripts/check.py <slug>` passes with zero errors, and `tmp/setup-report-<slug>.md` is written.
- **Onboarded.** The client folder is lint-clean and can enter the application's operational work.
- **Handoff rejected.** `python3 scripts/check.py --handoff <path>` reports an error. Stop before creating `clients/<slug>/`.
- **Retired later.** When an active client leaves, move the folder to `archive/<slug>/` with an `ARCHIVED.md` note, and end active assignments for that slug through `update-user`.
- Never create a client folder outside this skill.
- Client work reads only this client's assignment rows from `system/client-assignments.md`.

## Inputs

- `handoff_path` — path to the handoff Markdown file. Its sibling asset folder, if any, sits beside it named `<slug>/`.
- The signed order form (`order-form.pdf`), when the handoff names it or the operator attaches it.
- Operator email address, asked once if it is not known.
- The operator's answers during the Setup Ledger walk.

## Reads

- The handoff file and any sibling folder beside it.
- `formats/README.md`, `formats/clients/handoff.md`, `formats/clients/client.md`, `formats/clients/open-issues.md`, `formats/clients/decision-log.md`, and any other client format the handoff table names.
- `clients/README.md` and `clients/AGENTS.md`.

## Setup ledger

The Setup Ledger lists everything that stands between the handoff and a settled client folder. Open it at the start, add to it as soon as an item appears, and walk it with the operator. Add an entry for each of these:

- A section written as `None`, or filled with a placeholder.
- A row already present in the handoff's `# Open Issues` chapter.
- A discrepancy between `order-form.pdf` and the handoff's entitlements.
- A `scripts/check.py` warning, or an error that cannot be resolved from the handoff.

Each entry holds: `#`, `Step`, `Area`, `Item`, `Evidence`, `Recommended Approach`, and `Issue` (the `open-issues.md` row number, once opened). The recommended approach never invents a fact.

## Procedure

1. **Check the slug and open the Setup Ledger.** Read the handoff header. The `client` key is the target slug. Stop if `clients/<slug>/` or `archive/<slug>/` already exists.
2. **Validate the handoff.** Run `python3 scripts/check.py --handoff <handoff_path>`. If it reports any `ERROR`, stop before creating the client folder and return the findings. Record every `WARN` on the Setup Ledger.
3. **Create the client directory.** Create `clients/<slug>/`.
4. **Split chapters into governed documents.** For each chapter in `formats/clients/handoff.md`, in order:
   - Shift headings inside the chapter up one level.
   - Prepend the client YAML header. Set `format` to the governing format identifier (`clients/client`, `clients/open-issues`, or `clients/decision-log`), `format_version` to that contract's current version, and `client` to the slug. Set `created` and `updated` to today's date and both actor fields to the operator email.
   - Write `client.md`, `open-issues.md`, or `decision-log.md` as the handoff table's Produces column names. Do not use the format identifier as the filename.
   - Add a Setup Ledger entry for every `None` or placeholder, and for every open issue carried from the handoff.
5. **Copy the order form and assets.** If the handoff references an order form, redact payment card or bank numbers, save it as `clients/<slug>/order-form.pdf`, and point `client.md` at `order-form.pdf`. Where the handoff and the order form disagree, the order form wins and the discrepancy goes on the Setup Ledger. Copy referenced assets into `clients/<slug>/assets/`.
6. **Lint the new folder.** Add the client to `clients/README.md`. Run `python3 scripts/check.py <slug>`. Fix mechanical formatting. Add anything that cannot be resolved to the Setup Ledger.
7. **Walk the Setup Ledger.** Present one entry at a time with its evidence and recommended approach. The operator accepts it, gives a different answer, or defers it.
   - **On accept or answer:** Write the answer into the document named by `Area`. If the entry has an `# Open` row, move that row to `# Closed` and append one row to `decision-log.md` whose `Source` is `open-issues #<id>` and whose `Area` matches the issue. Update `updated` and `updated_by` on each file written.
   - **On defer:** Keep or add an `# Open` row with a concrete `Next Step`.
   - Run `python3 scripts/check.py <slug>` after every write.
8. **Write the setup report.** Write `tmp/setup-report-<slug>.md` listing every file written and the final outcome of each ledger entry. Run `python3 scripts/check.py`.

## Writes

- `clients/<slug>/client.md`, `clients/<slug>/open-issues.md`, and `clients/<slug>/decision-log.md`.
- Domain client files named by the handoff table, plus `order-form.pdf` and `assets/` when the handoff supplies them.
- `clients/README.md`.
- `tmp/setup-report-<slug>.md`.

## Stops when

The Setup Ledger has been walked, every entry is either written into its target document or tracked on `# Open`, every closed issue has a matching decision-log row, both `python3 scripts/check.py <slug>` and `python3 scripts/check.py` pass with zero errors, and the setup report is written. The operator commits.

## Never

- Never overwrite an existing `clients/<slug>/` or `archive/<slug>/` folder.
- Never create the client folder when the handoff check reports an error.
- Never invent a value for a `None` section.
- Never write a recommended approach into a document unless the operator accepts it.
- Never close an issue without appending the decision in the same change.
- Never read Slack, email, or Drive outside the handoff folder to fill a gap.
- Never commit the handoff or the setup report.
