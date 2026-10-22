---
name: review-open-issues
description: Walk one client's open issues one at a time, recommend a resolution from the client folder, and record accepted decisions.
---

# review-open-issues

## When to use

Use this skill before or during a client meeting to resolve rows on `clients/<slug>/open-issues.md`. Each accepted resolution is written into the target document and appended to that client's decision log in the same change.

## Boundaries

- **Entry.** `clients/<slug>/` exists, and `open-issues.md` and `decision-log.md` were created by `setup-client`.
- **Graduation.** The operator has accepted or deferred each issue that was presented. Every accepted issue has its answer in the target document and one new decision-log row. `python3 scripts/check.py <slug>` passes with zero errors.
- **Resolved.** The presented issues are closed and the decision log holds them.
- **Deferred.** An issue stays on `# Open` with the next step the operator stated.
- **No open issues.** `# Open` is `None`. Stop immediately.
- **Unknown client.** The slug is not a folder under `clients/`. Stop and ask the operator to pick a listed slug.
- Closing an issue writes the target document and the decision log in the same change.
- Client work reads only this client's assignment rows from `system/client-assignments.md`.

## Inputs

- A client slug. If omitted, list the folders under `clients/` and ask the operator to pick one. Never guess.
- The operator's accept, revise, or defer decision for each issue presented.
- Operator email address, asked once if it is not known.

## Reads

- `formats/clients/open-issues.md`, `formats/clients/decision-log.md`, and `formats/clients/client.md`.
- `clients/<slug>/open-issues.md`, `clients/<slug>/decision-log.md`, `clients/<slug>/client.md`, and the other files in that client folder.
- Assignment rows in `system/client-assignments.md` whose client slug is this client, plus the named users and roles. Do not read assignment rows for other clients.

## Procedure

1. **Resolve the slug.** If `clients/<slug>/` does not exist, stop and list the available slugs.
2. **Read the open list.** If `# Open` is `None`, stop and say there is nothing to review.
3. **Present one issue.** For the next `# Open` row, quote the issue and its `Next Step`. Recommend a resolution only from facts already in this client folder or from an assignment row for this client. Cite the heading or section used. If the folder does not support a recommendation, say so and ask the operator. Do not invent a fact to fill the gap.
4. **On accept or a revised answer.** Write the answer into the document named by `Area`. Move the issue row to `# Closed` with today's date and a `Resolution` that names the section written and the new decision-log row. Append one `# Decisions` row with the same `Area`, the decision, and `Source` of `open-issues #<id>`. Update `updated` and `updated_by` on each file. Run `python3 scripts/check.py <slug>`.
5. **On defer.** Leave the row on `# Open`. Change `Next Step` only to the next step the operator stated.
6. **Continue** until the operator stops or no open rows remain. Then run `python3 scripts/check.py`.

## Writes

- `clients/<slug>/open-issues.md`.
- The client document named by `Area` when an issue is accepted.
- `clients/<slug>/decision-log.md` when an issue is accepted.

## Stops when

The operator has accepted or deferred each presented issue, or `# Open` is `None`. Every accepted issue has its answer in the target document and exactly one new decision-log source. `python3 scripts/check.py <slug>` passes with zero errors.

## Never

- Never guess the client slug.
- Never invent a client fact, metric, or commercial term.
- Never close an issue without the target write and the decision-log row in the same change.
- Never delete or reword a closed issue or an existing decision.
- Never read or mention another client's assignments or folder.
