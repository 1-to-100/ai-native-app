---
name: improve-process
description: Refine a mechanism change until it can be planned, then implement the approved plan and have an independent subagent review the result.
---

# improve-process

## When to use

Use this skill when the operator wants to change how the application works, add or modify a workflow stage, capture a new field, tighten a guardrail, or turn a manual gap into a skill. Also use it when `process-backlog` or `review-question-journal` hands over a requirement that changes processes, formats, skills, or scripts. A change that only edits records in `system/` without changing a mechanism belongs to `setup-application` or `update-user`.

## Boundaries

- **Entry.** The operator invokes this skill with a change request, or `process-backlog` hands over one backlog item whose requirement and plan are ready for implementation.
- **Graduation.** The operator approved the plan, the final review subagent finished, affected mechanisms and active documents agree, and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` exit with zero errors.
- **Accepted and applied.** The working tree is ready for the operator to review and commit.
- **Plan revised.** The operator changes the plan at the approval gate. Implementation does not start until the revised plan is approved.
- **Proposal rejected.** The operator declines the plan. Governed files stay as they were before this run.
- Never modify a format contract without bumping `format_version`, migrating active files, and updating `scripts/check.py` in the same change.
- Interstitial requirement, plan, and review files stay in `tmp/`.

## Inputs

- The operator's change request, or the refined requirement and plan path handed over by `process-backlog` or `review-question-journal`.
- Operator email address, asked once if it is not known.
- Explicit approval of the implementation plan before any governed file is edited.

## Reads

- `docs/build-any-ai-application.md`, especially the precedence and creation order.
- Root `AGENTS.md`, `process/README.md`, `formats/README.md`, `.agents/skills/README.md`, `scripts/README.md`, `system/README.md`, and `clients/README.md`.
- The process, format, skill, subtree `AGENTS.md`, and active client or system document touched by the change.
- `scripts/check.py`.
- `system/question-journal.md` when the change is meant to absorb a journaled question.

## Procedure

1. **Refine the requirement.** Interview the operator until the change is specific enough to plan. Ask what outcome must be true when the work is done, which records change, and which cases are out of scope. Read the repository before asking for a fact it already holds. Write the requirement and acceptance criteria into `tmp/improve-process-requirement.md`. When a calling skill already supplied a requirement, check it against the same bar and ask only about gaps. Stop and keep interviewing while a missing answer would change the plan.
2. **Write the implementation plan.** Walk the mechanisms in authority order and name every file the change touches:
   1. Global Context (`AGENTS.md`), including a version bump when scope or a universal rule changes.
   2. Processes (`process/*.md`), including a process version bump and `process/README.md` when a stage, gate, or skill reference changes.
   3. Formats (`formats/system/` or `formats/clients/`). If a new section, column, or vocabulary value is required, the format changes first and its title version increments.
   4. Active data. Every active document of a changed format is migrated in the same change. Unknown values stay `None`, with a client issue when the document is a client file. Do not edit `archive/` or frozen history.
   5. Subtree `AGENTS.md` files.
   6. Skills (`.agents/skills/<name>/SKILL.md`) and `.agents/skills/README.md`.
   7. `scripts/check.py` and `scripts/README.md`.
   Write the plan to `tmp/improve-process-plan.md`. The plan lists files, schema or stage changes, and the order of edits. Present it in chat. **Wait for explicit approval.** Silence, partial agreement, and a request to keep talking are not approval. On rejection, stop with no governed file changed. On revision, update the plan and ask again.
3. **Prepare the parallel review.** After approval, give a fresh-context subagent only the approved requirement and the approved plan. That subagent writes `tmp/improve-process-review-plan.md`: the checks it will use to decide whether the requirement was implemented. It does not edit governed files and it does not see the implementation chat.
4. **Implement the plan.** While that review plan is being written, apply the approved plan in this session. Edit formats before the documents that follow them, bump versions, migrate active files, update inventories, and update `scripts/check.py`. Set `updated` to today and `updated_by` to the operator email on every governed data file touched. Do not expand into work the plan did not approve.
5. **Run the review and fix gaps.** When implementation and the review plan are both complete, give a second fresh-context subagent the review plan and the resulting diff. That subagent checks the result against the plan and fixes verified misses. It does not add scope. Repeat the review once if its fixes could have missed a related file. Then run `python3 scripts/setup-scripts.py` and `python3 scripts/check.py` until both exit 0.
6. **Report.** Summarize the requirement, the plan path, the files changed, and any review fix. Leave the working tree for the operator to review and commit. Do not commit unless the operator asked for a commit in this session.

## Writes

- `tmp/improve-process-requirement.md`, `tmp/improve-process-plan.md`, and `tmp/improve-process-review-plan.md`.
- After approval: the governed files named in the plan, including migrated active documents and inventories.

## Stops when

The operator rejects the plan, in which case no governed file from this run has been edited. Or the operator approved the plan, the final review subagent finished, and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` pass with zero errors.

## Never

- Never edit a governed file before the operator approves the plan in step 2.
- Never let the subagent that writes the review plan be the same context that implements the plan.
- Never let the implementing context grade its own result. The final review runs in a fresh context.
- Never change a skill to write a section or vocabulary value its format does not allow. Update the format first.
- Never bump a format version without updating `scripts/check.py` and migrating active documents of that format in the same run.
- Never invent a value while migrating a client document. Write `None` and open a row in `clients/<slug>/open-issues.md`.
- Never edit `archive/` or rewrite a closed history row.
