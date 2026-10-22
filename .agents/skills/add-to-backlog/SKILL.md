---
name: add-to-backlog
description: Add one application feature request or issue to system/application-backlog.md without implementing it.
---

# add-to-backlog

## When to use

Use this skill when the operator wants to keep an application change or enhancement for later. Use `review-open-issues` when the item is a missing or disputed fact about one client. Use `improve-process` when the operator wants the change implemented now.

## Boundaries

This skill covers `system/application-backlog.md` only. Refining and handing one item to `improve-process` is `process-backlog`.

- **Entry.** The operator invokes this skill with a request, or is ready to state one. The request is an application change, not a missing fact about one client.
- **Graduation.** A new `Proposed` row exists, its heading has never been used, and `python3 scripts/check.py` passes with zero errors.
- **Captured.** The row is `Proposed` and the skill ends.
- **Client fact.** The request is a missing or disputed fact about one client. Stop and point the operator to `review-open-issues` for that client.
- **Implement now.** The operator decides not to wait. Stop and point the operator to `improve-process` with the same request.
- Never delete a backlog row or reuse an `APP-NNNN` heading.
- Never implement the change in this skill.

## Inputs

- The feature request or issue, in the operator's words.
- A short title. Ask for one if the operator did not provide it.
- Operator email address, asked once if it is not known.

## Reads

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
