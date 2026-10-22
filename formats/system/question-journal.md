# Format: system/question-journal (version 1)

## Purpose

The repository-wide journal of questions an agent asked the operator beyond the questions a skill explicitly requires. An entry closes only when a process or prompting change makes that question unnecessary. Answering it in the session does not close it.

## Location

`system/question-journal.md`. One repository-wide journal.

## Header

The system header defined in `formats/README.md` with `format: system/question-journal` and `format_version: 1`. No `client` key.

## Body

```markdown
# Open
| # | Asked | Question | Skill | Process | Stage | LLM |
| --- | --- | --- | --- | --- | --- | --- |

One row per question that no change has absorbed yet, or the single line `None`.

# Closed
| # | Asked | Closed | Question | Skill | Process | Stage | LLM | Change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

One row per absorbed question, or the single line `None`. `Change` names the process, format, skill, or script change that made the question unnecessary.
```

## Rules

- `#` is a positive integer, unique across `# Open` and `# Closed`, and never reused.
- A row moves from `# Open` to `# Closed`. It is never deleted, and its question text is not rewritten to hide what was asked.
- `Skill` is a skill slug or `—` when no skill was running. `Process` is a process slug or `—`.
- `review-question-journal` proposes the absorbing change. `improve-process` applies an approved change. The journal entry closes only after that change exists.
- A question asked again after it was closed is a new row that cites the earlier `#` in the Question text. The recurrence is a defect in the earlier change.
- This journal is repository-wide. Client facts that are merely missing belong in `clients/<slug>/open-issues.md`, not here.

## Vocabularies

None. `Skill` and `Process` are references, not a closed display vocabulary. `LLM` records the model name the operator or agent reported.

## Checks

- System header with `format: system/question-journal` and `format_version: 1`.
- `# Open` and `# Closed` are present in that order. Each is `None` or a Markdown table with the columns defined above.
- Every `#` is a unique positive integer across both tables. `Asked` and `Closed` are `YYYY-MM-DD`.
- `Skill` is `—` or resolves to `.agents/skills/<slug>/SKILL.md`. `Process` is `—` or resolves to `process/<slug>.md`.
- `# Closed` rows have a non-empty `Change` value other than `—`.
