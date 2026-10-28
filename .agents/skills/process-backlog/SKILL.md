---
name: process-backlog
description: Triage the whole application backlog with the operator, then take each accepted item through a finalized plan, implementation, fresh-context review, closure, and commit.
---

# process-backlog

## When to use

Use this skill when the operator wants to work the application backlog in `system/application-backlog.md`. It runs in two passes. The first pass triages every open item together so the operator can drop, reshape, or accept each one with the whole backlog in view. The second pass takes the accepted items one at a time: a detailed plan, a dialog that finalizes it, implementation through `improve-process`, a fresh-context review, closure of the row, and a commit. Use `add-to-backlog` to capture a new item and `improve-process` for a change the operator wants made now without a backlog row.

## Boundaries

- **Entry.** The operator invokes this skill with a clean working tree. `system/application-backlog.md` holds at least one `Proposed`, `Ready`, or `In Progress` item. Invoking the skill is the operator's request for the commits it makes.
- **Graduation.** Every `Proposed` item was triaged. Each accepted item is `Done` with a resolution and a commit, or stays `Proposed` because the operator deferred it, it is blocked, or it is still vague, or stays `Ready` because implementation stopped. `python3 scripts/check.py` passes with zero errors.
- **Dirty tree.** `git status` shows uncommitted changes at entry. Stop and ask the operator to commit or stash them first, so each item's commit holds only that item.
- **Empty backlog.** The body is `None` or no item is `Proposed`, `Ready`, or `In Progress`. Report that and stop.
- **Resumed.** An item is already `Ready` or `In Progress` from an earlier run. It skips triage and joins the queue with its recorded plan; the operator confirms that plan is still final before implementation.
- **Dropped.** The operator decides at triage not to address an item. Status becomes `Cancelled`, `## Resolution` states the operator's reason, and the row stays.
- **Deferred.** The operator accepts an item in principle but does not want it worked in this run. It stays `Proposed`. Record the decision in the triage file only.
- **Blocked.** A dependency is not `Done` when the item's turn comes. Skip it, name the blocker, and continue with the next item.
- **Still vague.** The operator cannot answer a question the plan depends on. The item stays `Proposed`, the open point is appended to `## Request` in the operator's words, and the skill moves to the next item.
- **Handed off.** Implementation happens through `improve-process`. The finalized plan from the item's dialog is the approval that skill requires before it edits governed files. If its authority walk would change the plan, it asks the operator again before editing.
- **Implementation stopped.** `improve-process` stops, or its review cannot be made to pass. The row returns to `Ready` with its plan intact, nothing is committed for it, and the skill reports why and continues with the next item.
- Never invent acceptance criteria the operator did not confirm.
- Never put a client-only fact on the application backlog.

## Inputs

- The operator's triage decision for every `Proposed` item: address it now, defer it, or drop it, and any change to its scope or approach.
- The operator's answers while each accepted item's plan is finalized, and the operator's explicit word that the plan is final.
- Operator email address, asked once if it is not known.

## Reads

- `formats/system/application-backlog.md` and `system/application-backlog.md`.
- The processes, formats, skills, scripts, and system records each item appears to touch.
- `.agents/skills/improve-process/SKILL.md`.

## Procedure

### Pass 1: triage the backlog as a whole

1. **Check entry and list the open items.** Confirm the working tree is clean; if not, stop and ask the operator to commit or stash. Read every `Proposed` item in heading order, and note any `Ready` or `In Progress` item left by an earlier run. If there are none, report that the backlog has nothing to process and stop.
2. **Present each item.** For every `Proposed` item, write up to one paragraph describing the issue or request in the operator's terms and up to one paragraph recommending an approach: what would change, roughly where, and what it would cost or risk. Read the files the item touches before recommending. Present all items together in one message so the operator sees the whole backlog, and record the same text in `tmp/backlog-triage.md`.
3. **Collect decisions.** For each item ask the operator two things: whether to address it now, defer it, or drop it, and whether to change its scope or approach. Stop and wait for the operator's answers. Do not move on until every item has a decision. Note any ordering the operator wants.
4. **Record the triage.** Write the decisions into `tmp/backlog-triage.md`. For a dropped item set `## Status` to `Cancelled` and write the operator's reason in `## Resolution`. Deferred items stay `Proposed` and are not edited. Update the file header. Run `python3 scripts/check.py`.

### Pass 2: work each accepted item in turn

5. **Order the queue.** Take the accepted items in the operator's order, or in heading order with dependencies first. An item already `Ready` or `In Progress` joins the queue with its recorded plan and starts at step 7. When an item's turn comes, confirm its dependencies are `Done`. If one is not, skip the item, say why, and continue.
6. **Write the detailed plan.** For the current item write up to three paragraphs: the refined requirement and what must be true when it is done, the ordered file changes walked in authority order (`AGENTS.md`, processes, formats, active data, subtree `AGENTS.md`, skills, scripts), and the acceptance criteria with anything out of scope. Keep the full ordered file list in `tmp/backlog-plan-<id>.md`. Present the paragraphs in chat.
7. **Finalize with the operator.** Ask what the operator wants changed. Stop and wait for the answer. Revise the plan and the file and present it again until the operator says in so many words that it is final. If the operator cannot answer a question the plan depends on, append the open point to `## Request`, leave the item `Proposed`, and move to the next item.
8. **Record the item as ready.** Fill `## Refined Requirement`, `## Acceptance Criteria`, and `## Plan` on the row from the finalized plan. Do not put the temporary path in backticks. Set `## Status` to `Ready`. Update the file header. Run `python3 scripts/check.py`.
9. **Implement.** Invoke `improve-process` with the finalized requirement and `tmp/backlog-plan-<id>.md`, stating that the operator finalized the plan in this skill's dialog. That skill treats the finalized plan as approved, asks the operator only when its own walk of the mechanisms finds a gap or would change the plan, prepares its review plan in a fresh context, applies the plan, and runs its fresh-context review, which fixes verified misses. Set the row to `In Progress` when implementation starts. Make any further change the review turns up that stays inside the finalized plan; a change beyond it needs the operator's word first. Then run `python3 scripts/setup-scripts.py` and `python3 scripts/check.py` until both exit 0. If `improve-process` stops or the review cannot pass, set the row back to `Ready`, report why, and continue with the next item.
10. **Close and commit.** Set `## Status` to `Done` and write `## Resolution` naming the files that changed. Update the file header and run `python3 scripts/check.py`. Stage only the files this item changed plus `system/application-backlog.md`, and commit them on the current branch with a message that opens with the item heading and title. Do not push. Then take the next item.
11. **Report.** When the queue is empty, summarize each item: done with its commit, dropped with its reason, deferred, blocked, still vague, or stopped at `Ready`.

## Writes

- `system/application-backlog.md`.
- `tmp/backlog-triage.md` and `tmp/backlog-plan-<id>.md`.
- Governed mechanism files only through `improve-process`, after the operator finalized the item's plan.
- One commit per completed item on the current branch.

## Stops when

The working tree is dirty at entry, the backlog has no open item, or every `Proposed` item was triaged and each accepted item is `Done` and committed, deferred, blocked, left `Proposed` with its open point recorded, or left `Ready` because implementation stopped. `python3 scripts/check.py` passes with zero errors after every backlog edit.

## Never

- Never implement an item before the operator has said its plan is final.
- Never skip the fresh-context review before closing an item.
- Never implement the mechanism change inside this skill; it goes through `improve-process`.
- Never invent an acceptance criterion the operator did not confirm.
- Never delete a backlog row. A completed item leaves the active backlog by becoming `Done`; a dropped item by becoming `Cancelled`.
- Never commit a file an item did not change.
- Never push a commit this skill made.
