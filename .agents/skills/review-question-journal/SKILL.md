---
name: review-question-journal
description: Review open question-journal rows and turn each approved remedy into a process or prompting change.
---

# review-question-journal

## When to use

Use this skill when `system/question-journal.md` has `# Open` rows, or when the operator asks to review questions agents had to ask beyond what a skill required. Run it at repository level, not inside one client folder.

## Inputs

- Operator approval, rejection, or deferral for each proposed remedy.
- Operator email address, asked once if it is not known.

## Reads

- `process/question-review.md`.
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
