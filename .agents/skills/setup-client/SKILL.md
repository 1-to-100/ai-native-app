---
name: setup-client
description: Build a complete client folder under clients/ from whatever information the operator provides, then interview the operator to fill every blank required field and validate with check.py.
---

# setup-client

## When to use

A client or primary business entity is ready to be onboarded. The operator may provide pasted text, notes, files, a folder, or nothing at all. This skill builds the folder from what it is given and asks for the rest. Run it once per client.

## Boundaries

This skill creates `clients/<slug>/` and interviews the operator until every required field is answered or tracked. It does not discover prospects, negotiate commercial terms, or change application mechanisms. Mechanism changes go to `improve-process`. Later review of open issues is `review-open-issues`.

- **Entry.** The operator names a client to onboard. The slug does not yet exist in `clients/` or `archive/`.
- **Graduation.** Every required field is written into its target document or recorded as an `# Open` row. Every `# Closed` row has a matching decision-log row. `clients/README.md` includes the client. `python3 scripts/check.py <slug>` passes with zero errors, and `tmp/setup-report-<slug>.md` is written.
- **Onboarded.** The client folder is lint-clean and can enter the application's operational work.
- **Slug taken.** `clients/<slug>/` or `archive/<slug>/` exists. Stop and ask for a different slug or hand off to `review-open-issues`.
- **Retired later.** When an active client leaves, move the folder to `archive/<slug>/` with an `ARCHIVED.md` note, and remove that slug from users' assigned clients through `update-user`.
- Never create a client folder outside this skill.
- Client work reads only this client's slug in the users' `## Assigned Clients` in `system/users.md`.

## Inputs

- Whatever the operator supplies: pasted text, notes, file paths, or a folder. It may be nothing.
- The client slug (lowercase kebab-case). Propose one from the client's name and confirm it.
- Operator email address, asked once if it is not known.
- The operator's answers during the interview.

## Reads

- Only the files the operator names. Never search Slack, email, or Drive to fill a gap.
- `formats/README.md`, `formats/clients/client.md`, `formats/clients/order-form.md`, `formats/clients/open-issues.md`, and `formats/clients/decision-log.md`.
- `system/products-and-services.md` when it exists, and `system/users.md`, so order-form items and the sales representative resolve.
- `clients/README.md` and `clients/AGENTS.md`.

## Setup ledger

The Setup Ledger lists everything that stands between what the operator provided and a settled client folder. Open it at the start, add to it as soon as an item appears, and walk it with the operator. Add an entry for each of these:

- A required field the operator's information does not answer.
- A value that conflicts between two things the operator provided.
- A `scripts/check.py` warning, or an error that cannot be resolved from what was provided.

Each entry holds: `#`, `Step`, `Area`, `Item`, `Evidence`, `Recommended Approach`, and `Issue` (the `open-issues.md` row number, once opened). The recommended approach never invents a fact.

## Procedure

1. **Gather what exists.** Ask the operator for anything they have on the client and read the files they name. Propose a slug and confirm it. Stop if `clients/<slug>/` or `archive/<slug>/` exists. Ask whether the client has ordered products or services, and whether an order form exists.
2. **Draft from the information.** Extract only facts the operator's information states. Map them to the fields of `client.md` and, when an order exists, `order-form.md`. Do not infer or fill a field from anything else. Open the Setup Ledger with an entry for every required field still unknown.
3. **Create the client directory.** Create `clients/<slug>/` and write `client.md`, `open-issues.md`, `decision-log.md`, and `order-form.md` when an order exists, each with the client YAML header. Set `format` to the governing identifier, `format_version` to that contract's current version, `client` to the slug, `created` and `updated` to today, and both actor fields to the operator email. Write `None` in every unknown field. Order-form line items come from `system/products-and-services.md` when it exists: use the exact item name and copy its Specification verbatim. If the operator supplies a signed PDF, redact payment card or bank numbers, save it as `clients/<slug>/order-form.pdf`, and set `Signed Copy` to `order-form.pdf`.
4. **Lint.** Add the client to `clients/README.md`. Run `python3 scripts/check.py <slug>`. Fix mechanical formatting and add anything unresolved to the Setup Ledger.
5. **Interview for the blanks.** Walk the Setup Ledger one entry at a time, asking the operator for the missing value with the evidence and a recommended approach. The operator answers, accepts the recommendation, or defers.
   - **On answer:** Write it into the document named by `Area`. If the entry has an `# Open` row, move that row to `# Closed` and append one row to `decision-log.md` whose `Source` is `open-issues #<id>` and whose `Area` matches the issue. Update `updated` and `updated_by` on each file written.
   - **On defer:** Open or keep an `# Open` row with a concrete `Next Step`.
   - Run `python3 scripts/check.py <slug>` after every write.
6. **Write the setup report.** Write `tmp/setup-report-<slug>.md` listing every file written and the final outcome of each ledger entry. Run `python3 scripts/check.py`.

## Writes

- `clients/<slug>/client.md`, `clients/<slug>/open-issues.md`, and `clients/<slug>/decision-log.md`.
- `clients/<slug>/order-form.md`, and `order-form.pdf` when the operator supplies a signed copy.
- `clients/README.md`.
- `tmp/setup-report-<slug>.md`.

## Stops when

The interview has covered every ledger entry, every entry is either written into its target document or tracked on `# Open`, every closed issue has a matching decision-log row, both `python3 scripts/check.py <slug>` and `python3 scripts/check.py` pass with zero errors, and the setup report is written. The operator commits.

## Never

- Never overwrite an existing `clients/<slug>/` or `archive/<slug>/` folder.
- Never invent a value for an unanswered field. Write `None` and open an issue.
- Never write a recommended approach into a document unless the operator accepts it.
- Never close an issue without appending the decision in the same change.
- Never read Slack, email, or Drive outside the files the operator names to fill a gap.
- Never store a payment card or bank number.
- Never commit the setup report.
