---
name: review-question-journal
description: Review open question-journal rows and turn each approved remedy into a process or prompting change.
---

# review-question-journal

## When to use

Use this skill when `system/question-journal.md` has `# Open` rows, or when the operator asks to review questions agents had to ask beyond what a skill required. Run it at repository level, not inside one client folder.

## Boundaries

This skill covers `system/question-journal.md` and the handoff of an approved remedy to `improve-process`. It does not close a question because the operator answered it in the session. Missing client facts belong in `review-open-issues`, not in this journal.

- **Entry.** The operator invokes this skill, and `# Open` contains at least one row. Each row names the question, the skill or `—`, the process or `—`, the stage, and the model that asked.
- **Graduation.** Every presented row was approved and closed by a recorded change, or explicitly left open. `python3 scripts/check.py` passes with zero errors. A closed row cites the change that absorbed it.
- **Absorbed.** The approved remedy was applied through `improve-process`, and the journal row moved to `# Closed`.
- **Left open.** The operator rejects the remedy or defers it. The row stays on `# Open`.
- **Empty journal.** `# Open` is `None`. Stop without inventing a question.
- **Recurrence.** A new question cites an earlier closed `#`. The new row stays open, and the earlier change is treated as defective input to `improve-process`.
- Never apply a remedy before the operator approves it.
- Remedy proposals stay in `tmp/` until `improve-process` applies an approved change.

## Inputs

- Operator approval, rejection, or deferral for each proposed remedy.
- Operator email address, asked once if it is not known.

## Reads

- `formats/system/question-journal.md` and `system/question-journal.md`.
- The skill, process, and stage named on each open row.
- `.agents/skills/improve-process/SKILL.md`.

## Procedure

1. **Read `# Open`.** If it is `None`, stop. There is nothing to review.
2. **Review one row at a time.** State why the process or skill could not answer the question from the record. Propose one remedy:
   - **Process change** — a missing field, vocabulary value, stage, branch, or check, so the information is in the record before the stage begins.
   - **Prompting change** — the skill should have asked for this at the start instead of mid-stage.
3. **Write the proposal.** Append the analysis to `tmp/review-question-journal-proposal.md` and present it. Wait for an explicit approval before any mechanism edit.
4. **On approval.** Invoke `improve-process` with that remedy. Do not move the journal row yet. After `improve-process` has applied the change and `python3 scripts/check.py` passes, move the row from `# Open` to `# Closed`. Keep the original question text. Set `Closed` to today and `Change` to the process, format, skill, or script change that absorbed it.
5. **On rejection or deferral.** Leave the row on `# Open`.
6. **On a recurrence.** If the question cites an earlier closed number, keep the new row open and treat the earlier change as defective input to `improve-process`.

## Writes

- `tmp/review-question-journal-proposal.md`.
- `system/question-journal.md` after an approved remedy has actually been applied.
- Mechanism files only through `improve-process`.

## Stops when

Every presented row was absorbed and moved to `# Closed`, or the operator left it open. A closed row names the change that absorbed it. `python3 scripts/check.py` passes with zero errors.

## Never

- Never close a row because the operator answered the question in the session.
- Never close a row before the absorbing change exists in the repository.
- Never delete or rewrite a journal row.
- Never record a client-only missing fact here. That belongs in `clients/<slug>/open-issues.md`.
