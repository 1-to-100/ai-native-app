---
name: add-to-backlog
description: Add one application feature request or issue to system/application-backlog.md without implementing it.
---

# add-to-backlog

## When to use

Use this skill when the operator wants to keep an application change or enhancement for later. Use `review-open-issues` when the item is a missing or disputed fact about one client. Use `improve-process` when the operator wants the change implemented now.

## Inputs

- The feature request or issue, in the operator's words.
- A short title. Ask for one if the operator did not provide it.
- Operator email address, asked once if it is not known.

## Reads

- `process/backlog-management.md` Stage 1.
- `formats/system/application-backlog.md` and `system/application-backlog.md`.
- `system/AGENTS.md`.

## Procedure

1. **Classify the request.** If it is a missing fact, conflict, or decision about one named client, stop and tell the operator to use `review-open-issues` for that client. Do not add a backlog row.
2. **If the operator wants it implemented now,** stop and tell them to run `improve-process` with the same request. Do not add a row unless they still want it held.
3. **Assign the next heading.** Use `APP-0001` when the body is `None`. Otherwise use the next four-digit number after the highest existing `APP-NNNN`. Never reuse a heading.
4. **Write the row.** Set `## Title` and `## Request` from the operator. Set `## Status` to `Proposed`, `## Opened` to today, and `## Refined Requirement`, `## Acceptance Criteria`, `## Plan`, `## Dependencies`, and `## Resolution` to `None`. Update the file header.
5. **Verify.** Run `python3 scripts/check.py` and report the new heading.

## Writes

- `system/application-backlog.md`.

## Stops when

The new `Proposed` row is written and `python3 scripts/check.py` passes with zero errors, or the request was redirected to `review-open-issues` or `improve-process` before any write.

## Never

- Never implement the request in this skill.
- Never invent acceptance criteria or a plan. Those belong to `process-backlog`.
- Never delete or renumber an existing backlog row.
- Never put a client-only fact on the application backlog.
