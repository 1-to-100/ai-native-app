# Process: question-review (version 1)

# Purpose
Governs how questions that an agent had to ask the operator, beyond the questions a skill already requires, become a process or prompting change so the same question is not asked again.

# Scope
Covers `system/question-journal.md` and the handoff of an approved remedy to `improve-process`. It does not close a question merely because the operator answered it in the session. Missing client facts belong in `client-lifecycle`, not in this journal.

# Roles
- Operator: Approves or rejects each proposed remedy.
- Agent: Executes `review-question-journal` and, for an approved remedy, `improve-process`.

# Cadence
Stage 1 runs when `system/question-journal.md` has one or more `# Open` rows, or when the operator asks to review the journal.

# System of Record
## Mode
Repository Markdown

## Location
`system/question-journal.md` governed by `system/question-journal`. Remedy proposals stay in `tmp/` until `improve-process` applies an approved change.

# Inputs
- `system/question-journal.md`.
- The skill, process, and stage named on each open row.
- Operator approval of each remedy.

# Stages
## Stage 1: Review Open Questions
### Entry Criteria
The operator invokes `review-question-journal`, and `# Open` contains at least one row. Each row names the question, the skill or `—`, the process or `—`, the stage, and the model that asked.

### Description
The Agent takes one open row at a time, explains why the record could not answer it, and proposes either a process change or a prompting change. The proposal is written to `tmp/review-question-journal-proposal.md`. On approval, the Agent invokes `improve-process` for that remedy and moves the row to `# Closed` with the change named in `Change`. On rejection, the row stays open.

### Graduation Criteria
Every presented row was approved and closed by a recorded change, or explicitly left open. `python3 scripts/check.py` passes with zero errors. A closed row cites the change that absorbed it.

### Branching and Terminal Paths
- **Absorbed:** The approved remedy was applied through `improve-process`, and the journal row moved to `# Closed`.
- **Left Open:** The operator rejects the remedy or defers it. The row stays on `# Open`.
- **Empty Journal:** `# Open` is `None`. The stage stops without inventing a question.
- **Recurrence:** A new question cites an earlier closed `#`. The new row stays open, and the earlier change is treated as defective input to `improve-process`.

### Implementing Skills
`review-question-journal`

# Outputs
- Updated `# Open` and `# Closed` tables in `system/question-journal.md`.
- `tmp/review-question-journal-proposal.md`.
- Mechanism changes only when `improve-process` applies an approved remedy.

# Rules
- Never close a journal row because the operator answered the question in chat.
- Never delete or rewrite a journal row. A recurrence is a new row.
- Never apply a remedy before the operator approves it.
- Never record a client-only missing fact in this journal.

# Related
- Format: `system/question-journal`.
- Skills: `review-question-journal`, `improve-process`.
- Process: `application-lifecycle`.
- Gaps: None.
