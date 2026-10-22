---
name: process-backlog
description: Refine one application backlog item until it can be planned, then hand the requirement and plan to improve-process.
---

# process-backlog

## When to use

Use this skill when the operator is ready to take one item on `system/application-backlog.md` from a captured request to an implementable plan. The implementation itself belongs to `improve-process`.

## Inputs

- An `APP-NNNN` heading. If omitted, list the `Proposed` items and ask the operator to pick one.
- The operator's answers while the requirement is refined.
- Operator email address, asked once if it is not known.

## Reads

- `process/backlog-management.md` Stage 2.
- `formats/system/application-backlog.md` and `system/application-backlog.md`.
- The processes, formats, skills, and system records the item appears to touch.
- `.agents/skills/improve-process/SKILL.md`.

## Procedure

1. **Select one item.** Confirm the heading exists and its status is `Proposed`. If a dependency heading is not `Done`, stop and name the blocker. Do not refine past it.
2. **Grill the requirement.** Ask what must be true when the item is done, which files change, what is out of scope, and how the operator will know it worked. Continue until the requirement and acceptance criteria are specific enough to plan. If the operator cannot answer a question the plan depends on, leave the item `Proposed`, add that open point to `## Request`, and stop.
3. **Write the plan.** Write `tmp/backlog-plan-<id>.md` with the ordered file changes. Update the backlog row: `## Refined Requirement`, `## Acceptance Criteria`, and `## Plan` as a summary of that plan. Do not put the temporary path in backticks. Set `## Status` to `Ready`. Update the file header. Run `python3 scripts/check.py`.
4. **Hand off.** Invoke `improve-process` with the refined requirement and `tmp/backlog-plan-<id>.md`. That skill still gets the operator's approval before it edits governed mechanism files. When `improve-process` starts implementation, set this item to `In Progress`. When it finishes and the review passes, set this item to `Done` and write `## Resolution` naming the files that changed.
5. **If the operator cancels,** set `## Status` to `Cancelled` and write the operator's reason in `## Resolution`. Keep the row.

## Writes

- `system/application-backlog.md`.
- `tmp/backlog-plan-<id>.md`.
- Governed mechanism files only through `improve-process`, after that skill's approval gate.

## Stops when

The item stays `Proposed` because it is blocked or still vague, the operator cancels it, or `improve-process` has finished and the backlog row is `Done` with a resolution. `python3 scripts/check.py` passes with zero errors after every backlog edit.

## Never

- Never implement the mechanism change inside this skill.
- Never skip `improve-process`'s approval gate.
- Never invent an acceptance criterion the operator did not confirm.
- Never delete the backlog row.
