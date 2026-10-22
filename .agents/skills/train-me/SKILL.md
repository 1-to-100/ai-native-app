---
name: train-me
description: Teach one recorded user the application scope, their role, the format and process concepts, and the operating rules.
---

# train-me

## When to use

Use this skill when a person wants to learn how this application works, or when an operator asks to train a named user. The teaching is specific to the role and client assignments recorded for that person.

## Inputs

- The learner's email address. If it is omitted, list the `Active` emails in `system/users.md` and ask the operator to pick one.
- Acknowledgement of each topic, or an explicit request to stop.

## Reads

- `process/user-administration.md` Stage 3.
- Root `AGENTS.md` and `docs/build-any-ai-application.md`.
- `system/users.md`, `system/user-roles.md`, and the learner's rows in `system/client-assignments.md`.
- `formats/README.md` and the format contracts those roles use.
- `process/README.md` and the process files named by the learner's role.
- `.agents/skills/README.md` for the skills named by the learner's role.

## Procedure

Teach the topics below in order. For each topic, explain it from the files you read, tie it to the learner's primary role and client assignments, then ask the learner to acknowledge it or ask a question. Answer a question from the repository. If the repository cannot answer it, and the question was not one this skill requires, append it to `system/question-journal.md` as an `# Open` row and continue. Do not turn the training session into a mechanism change.

1. **Scope.** What this repository is for, what is in scope, and what is out of scope, from root `AGENTS.md`.
2. **The learner's role.** Their primary role's purpose, core tasks, processes, and skills. Then each `Active` client assignment: the client slug and the role they play for that client. Do not describe assignments for anyone else.
3. **Format concepts.** Namespaced format identifiers, the system header versus the client header, `None`, exact vocabulary display names, and record headings as references.
4. **Processes.** The processes named by the role, plus how a stage's entry criteria, graduation criteria, and branching paths tell an agent where to stop.
5. **Approval gates.** A material change waits for an explicit human approval. Silence is not approval, and an agent is not an actor in a document header.
6. **Source of truth.** When files disagree, authority runs from root `AGENTS.md` to the process, then the format, then subtree rules, then the skill, then `scripts/check.py`, then the data files. The format wins on document structure.
7. **Client isolation.** A client folder does not refer to another client. `system/` may name a client slug on an assignment and must not hold that client's business facts.
8. **Issues, decisions, backlog, and the journal.** A missing client fact goes to `open-issues.md` and, once decided, to `decision-log.md`. A later application change goes to `application-backlog.md`. A question a skill did not require goes to `question-journal.md` and closes only when a change makes it unnecessary.
9. **Integrations and secrets.** Shared system setup is `setup-application`. The learner's own connections are `setup-my-integrations`. Credentials never go in the repository.
10. **Verification.** A governed edit is not finished until `python3 scripts/check.py` passes.
11. **How the application changes.** `improve-process` refines, plans, implements, and independently reviews a mechanism change. `upgrade-app` brings the repository up to the current template paradigm. `add-to-backlog` holds a change the operator does not want to make now.

After the last acknowledgement, or when the learner stops, write `tmp/train-me-<email-slug>.md` with the email, the date, the topics acknowledged, and the topic where they stopped, if any.

## Writes

- `tmp/train-me-<email-slug>.md`.
- An `# Open` row in `system/question-journal.md` only when the learner asks a question this skill did not require and the repository cannot answer it.

## Stops when

The learner has acknowledged every topic, or has stopped at a named topic, and the temporary training report is written. If the email is not in `system/users.md`, the skill stops before teaching and points the operator to `update-user`.

## Never

- Never invent a role task, client fact, or metric to make the lesson feel complete.
- Never teach another person's client assignments.
- Never change a process, format, or skill during the lesson. Capture a real defect as a journal row or tell the operator to run `add-to-backlog`.
- Never store a secret in the training report.
