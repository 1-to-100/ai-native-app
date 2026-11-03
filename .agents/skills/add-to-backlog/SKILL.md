---
name: add-to-backlog
description: Grill the operator until one application feature request or issue is fully specified in the backlog's typed Request subsections, then add it to system/application-backlog.md without implementing it.
---

# add-to-backlog

## When to use

Use this skill when the operator wants to keep an application change or enhancement for later. Use `review-open-issues` when the item is a missing or disputed fact about one client. Use `improve-process` when the operator wants the change implemented now.

This skill is a requirements interview, not a note-taker. It does not write a row until the typed `### ` subsections of `## Request` are complete, so the item `process-backlog` later picks up already states the problem, the outcome, the scope, the mechanisms affected, and the constraints. It does not plan or implement.

## Boundaries

This skill covers `system/application-backlog.md` only. Triaging the backlog and working each accepted item to a commit is `process-backlog`.

- **Entry.** The operator invokes this skill with a request, or is ready to state one. The request is an application change, not a missing fact about one client.
- **Graduation.** The interview is complete, the operator confirmed the playback, a new `Proposed` row exists, its heading has never been used, and `python3 scripts/check.py` passes with zero errors.
- **Captured.** The row is `Proposed` and the skill ends.
- **Client fact.** The request is a missing or disputed fact about one client. Stop and point the operator to `review-open-issues` for that client.
- **Implement now.** The operator decides not to wait. Stop and point the operator to `improve-process` with the same request and the answers so far.
- **Duplicate.** An existing row already covers the request. Say so and ask whether to stop or still add a separate row that depends on it. Never edit the existing row.
- **Not ready to capture.** The operator cannot yet state the problem, the desired outcome, the scope, or the mechanisms affected, or abandons the interview. Write no row, say which answers are missing, and stop.
- **Completion is required.** The operator saying "that's enough" or "just add it" does not end the interview. Name the branches still open and keep asking. The only ways out are an answer, a confirmed `None` where the format allows it, an open point the operator cannot resolve now (step 6), or the Not ready to capture stop.
- Never delete a backlog row or reuse an `APP-NNNN` heading.
- Never implement the change in this skill.

## Inputs

- The feature request or issue, in the operator's words.
- The operator's answers to each interview round, and their word that the playback is right.
- A short title. Propose one from the interview if the operator did not provide it.
- Operator email address, asked once if it is not known.

## Reads

- `formats/system/application-backlog.md` and `system/application-backlog.md`.
- `system/AGENTS.md`.
- The processes, formats, skills, scripts, and system records the request appears to touch, read before asking about them.

## Procedure

1. **Classify the request.** If it is a missing fact, conflict, or decision about one named client, stop and tell the operator to use `review-open-issues` for that client. Do not add a backlog row.
2. **If the operator wants it implemented now,** stop and tell them to run `improve-process` with the same request. Do not add a row unless they still want it held.
3. **Look up the facts first.** Finding facts is your job, not the operator's. Read the backlog for overlapping or related rows, and read the mechanisms the request appears to touch in authority order: `AGENTS.md`, processes, formats, active data, subtree `AGENTS.md`, skills, scripts. When the lookup is broad, give a fresh-context subagent the request and the question to answer, and keep asking about everything that does not depend on its result. Ask the operator only for decisions and for facts that live in their head.
4. **Map the design tree.** Write the tree to `tmp/add-to-backlog-interview.md`. The branches are the subsections the format requires under `## Request`, and each answer can open or close the branches under it:
   1. **Problem and Trigger.** What is missing or going wrong today, where it was seen, and who it affects.
   2. **Desired Outcome.** What must be observably true when the change is done, and how someone would check it.
   3. **In Scope** and **Out of Scope.** What is included, what is excluded, and which cases are deliberately left out.
   4. **Mechanisms and Records Affected.** Which of global context, processes, formats, skills, scripts, or `system/` records change, which active documents would need migrating, and whether a format changes shape. Propose this from the lookup and have the operator confirm it.
   5. **Constraints.** Rules that must keep holding, such as client isolation, existing `Never` rules, users or roles affected, and compatibility with existing data.
   6. **Relationships.** Existing rows this overlaps with, depends on, or blocks. These become `## Dependencies`.
   7. **Why Held.** Why it waits and what would make it urgent.
   Add branches the request demands. A branch the request already answers is not a question; state the answer as the recommended answer for the operator to confirm.
5. **Grill in rounds.** The frontier is every question whose prerequisites are already settled. Ask the whole frontier in one round, numbered, each with a recommended answer, worded so that "yes" accepts it. A question that depends on another question open in the same round waits for a later round. Then stop and wait for the operator's answers.

   ```
   ❓ **Q1** - **<question title>**: <question, with options where useful>

   ➡️ <recommended answer>
   ```

   Each round of answers settles branches, opens the ones under them, and moves the frontier outward. Recompute it and ask the next round. Do not ask the operator for a fact a read could find.

   Test every answer before accepting it:
   - **Checkable.** Someone who was not in the conversation could tell whether it is true. "Better" and "easier" are not answers; ask how the operator would tell.
   - **Consistent.** It does not contradict an earlier answer, an existing `Never` rule, or the format. Name the conflict and ask which wins.
   - **Complete.** It does not leave an obvious case, record, or role unaddressed.
6. **Close the interview.** The interview is complete only when the frontier is empty and nothing is silently assumed. If the operator cannot answer a question after you looked it up, recommended an answer, and offered options, record it as a bullet under `### Open Points` that names what is missing and what would answer it. Never record an open point for Problem and Trigger, Desired Outcome, In Scope, or Mechanisms and Records Affected; those stop the capture.
7. **Play it back and get confirmation.** Present the complete row as it would be written, with the proposed title, every `###` subsection, the dependencies, and the open points. Stop and wait. Revise and present it again until the operator says in so many words that it is right. Do not write before then.
8. **Assign the next heading.** Use `APP-0001` when the body is `None`. Otherwise use the next four-digit number after the highest existing `APP-NNNN`. Never reuse a heading.
9. **Write the row.** Set `## Title` from the confirmed title. Set `## Request` to the typed subsections the format defines, in order, filled from the confirmed answers; `### Statement` holds the operator's request in their own words. Set `## Status` to `Proposed` and `## Opened` to today. Set `## Dependencies` to the confirmed `- APP-NNNN` lines, or `None`. Set `## Refined Requirement`, `## Acceptance Criteria`, `## Plan`, and `## Resolution` to `None`. Update the file header.
10. **Verify.** Run `python3 scripts/check.py` and report the new heading.

## Writes

- `tmp/add-to-backlog-interview.md`.
- `system/application-backlog.md`.

## Stops when

The playback is confirmed, the new `Proposed` row is written, and `python3 scripts/check.py` passes with zero errors. Or the request was redirected to `review-open-issues` or `improve-process`, stopped as a duplicate, or stopped as not ready to capture, before any write.

## Never

- Never implement the request in this skill.
- Never write to `## Refined Requirement`, `## Acceptance Criteria`, or `## Plan`. Those belong to `process-backlog`.
- Never end the interview because the operator is tired of it. Name what is open and keep going, or stop with no row.
- Never write a requirement, scope line, constraint, or dependency the operator did not state or accept. A recommended answer the operator did not accept stays out.
- Never ask the operator for a fact the repository holds.
- Never write the row before the operator confirms the playback.
- Never delete, renumber, or edit an existing backlog row.
- Never put a client-only fact on the application backlog.
