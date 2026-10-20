---
name: setup-client
description: Build a complete client folder under clients/ from an onboarding handoff file, walk the Setup Ledger with the operator, and validate with check.py.
---

# setup-client

## When to use

A client (or primary business entity) has completed upstream onboarding—or is migrating from an legacy workflow—and a handoff file conforming to `formats/handoff.md` is ready. A valid handoff is sufficient on its own: this skill reads nothing outside the handoff, its sibling folder, and this repository. Run once per client.

## Inputs

- `handoff_path` — path to the handoff Markdown file (for example `tmp/handoff/<slug>.md`). Its sibling asset/contract folder, if any, sits beside it named `<slug>/`.
- The signed order form (`order-form.pdf`), when named in the handoff under `# Client` -> `## Entitlements` -> `### Order Form` or attached by the operator.
- Operator email address, asked once if not known.
- The operator's answers to the Setup Ledger in chat at Step 7.

## Reads

- The handoff file at `handoff_path` and any sibling folder `<slug>/` beside it.
- `formats/README.md`, `formats/handoff.md`, `formats/client.md`, `formats/open-issues.md`, and every other client document format listed in `formats/handoff.md`.
- `clients/README.md` and `clients/AGENTS.md`.

## Setup ledger

The Setup Ledger is the running list of everything that stands between the handoff and a completely settled client folder. It is opened in Step 1, grows as the procedure runs, and is walked with the operator in Step 7; nothing on it is ever silently dropped. Add an entry the moment the procedure encounters:
- A section written as `None`, or filled with a placeholder/stand-in value;
- A row already present in the handoff's `# Open Issues` chapter;
- A discrepancy between `order-form.pdf` and the handoff's `# Client` -> `## Entitlements` section;
- A `scripts/check.py` warning (`WARN`) or an error that cannot be resolved mechanically from the handoff.

Each ledger entry holds, in order:
1. `#` (sequential integer in the order raised)
2. `Step` (the procedure step that raised it)
3. `Area` (a Display Name from `formats/open-issues.md` -> `Areas`)
4. `Item` (what is missing, conflicting, or unconfirmed, and why setup is incomplete without it)
5. `Evidence` (what the handoff or order form says, cited by section)
6. `Recommended Approach` (which of two conflicting values to keep and why, which document the answer lands in, who can supply what is missing, and what stands in the meantime—never an invented fact)
7. `Issue` (the `open-issues.md` row `#`, once opened)

## Procedure

1. **Check slug and open the Setup Ledger.** Read the handoff's YAML header. The `client` key is the target `<slug>`. Refuse and stop if `clients/<slug>/` or `archive/<slug>/` already exists. Open the Setup Ledger.
2. **Pre-flight validate the handoff.** Run `python3 scripts/check.py --handoff <handoff_path>`. If it reports any `ERROR`, stop before creating `clients/<slug>/` and return the findings so the handoff can be fixed upstream. Record every `WARN` on the Setup Ledger.
3. **Create the client directory.** Create `clients/<slug>/` (plus `assets/` or subdirectories required by the application's formats).
4. **Split chapters into governed documents.** For each `#` chapter in the handoff (in the order defined by `formats/handoff.md`):
   - Shift all headings inside the chapter up one level (`##` becomes `#`, `###` becomes `##`, and so on).
   - Prepend the standard YAML header (`title` as `<Client Name> — <Document>` or `<Client Name>` for `client.md`, `format` set to the governing format slug, `format_version` set to that format's current version, `client: <slug>`, `created` and `updated` set to today's `YYYY-MM-DD`, and `created_by` and `updated_by` set to the operator's email).
   - Write the file into `clients/<slug>/<format>.md`.
   - Add a Setup Ledger entry for every section holding `None` or a placeholder, and for every row carried from `# Open Issues`.
5. **Copy the order form and assets.** If the handoff references `<slug>/order-form.pdf` (or the operator attached it), redact any payment card or bank account numbers, save it as `clients/<slug>/order-form.pdf`, and set `client.md` -> `# Entitlements` -> `## Order Form` to `order-form.pdf`. Where the handoff's `# Entitlements` values and the order form disagree, the order form wins and the discrepancy goes on the Setup Ledger. Copy any referenced assets into `clients/<slug>/assets/` and rewrite paths to be relative to the client folder.
6. **Run initial lint.** Update `clients/README.md` to add a row for `<slug>`, then run `python3 scripts/check.py <slug>`. Fix any mechanical formatting issue; add any unresolvable finding to the Setup Ledger.
7. **Walk the Setup Ledger with the operator.** Present the Setup Ledger entries to the operator in chat, one entry at a time (or in a grouped batch if the operator requests): show `#`, `Area`, `Item`, `Evidence`, and `Recommended Approach`, and ask the operator to **accept the recommendation**, **give a different answer**, or **defer**.
   - **On accept or answer:** Write the operator's answer into the target section of the document named by `Area`, update `updated` and `updated_by` on that document, and if the entry had an `# Open` row in `clients/<slug>/open-issues.md`, move that row to `# Closed` with today's date and a `Resolution` naming what was decided and where it was written.
   - **On defer:** Ensure the entry has a row in `clients/<slug>/open-issues.md` under `# Open` with a unique integer `#`, today's `Opened` date, `Area`, `Issue`, and `Next Step` stating who does what next.
   - Run `python3 scripts/check.py <slug>` after every write.
8. **Write the setup report and finish.** Write `tmp/setup-report-<slug>.md` (uncommitted) listing every file written and the complete Setup Ledger with each entry's final outcome (answered and closed, or deferred to `open-issues.md` row `#`). Run a final `python3 scripts/check.py` across the repository.

## Writes

- `clients/<slug>/client.md`, `clients/<slug>/open-issues.md`, and any domain-specific client files defined in `formats/handoff.md`.
- `clients/<slug>/order-form.pdf` and `clients/<slug>/assets/` (when present in the handoff).
- `clients/README.md` (adding the new client row).
- `tmp/setup-report-<slug>.md` (uncommitted setup report).

## Stops when

The Setup Ledger has been walked to its end (or deferred by the operator), every entry is either written into its target document or tracked as an `# Open` row in `clients/<slug>/open-issues.md`, `python3 scripts/check.py <slug>` and `python3 scripts/check.py` pass with zero errors, and `tmp/setup-report-<slug>.md` is written. The operator commits.

## Never

- Never overwrite an existing `clients/<slug>/` or `archive/<slug>/` folder.
- Never create `clients/<slug>/` if `python3 scripts/check.py --handoff <handoff_path>` reports an `ERROR`.
- Never invent a value to fill a `None` section; put it on the Setup Ledger and open a row in `open-issues.md` if deferred.
- Never write a `Recommended Approach` into a document as fact unless the operator explicitly accepts it.
- Never drop a Setup Ledger entry silently.
- Never read external Slack, email, or Drive outside the handoff folder to fill a gap.
- Never commit the handoff file or `tmp/setup-report-<slug>.md` to the repository.
