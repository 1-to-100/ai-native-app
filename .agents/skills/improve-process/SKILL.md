---
name: improve-process
description: Diagnose an operator's process change request or friction point, propose coordinated mechanism updates, and apply them atomically on approval.
---

# improve-process

## When to use

Whenever the operator wants to change how the application works, add or modify a workflow stage, capture a new field in a document, tighten a guardrail after a recurring manual correction, or turn a manual process gap into a skill. Instead of editing individual files ad hoc and breaking contracts, run this skill so every affected mechanism updates together.

## Inputs

- The operator's description of the requested change, observed defect, or recurring manual intervention (asks if not provided).
- Operator email address (asked once if not known, required when migrating active data files under `clients/` or catalogs).
- The operator's explicit approval (or revisions) on the proposed change plan at Step 4.

## Reads

- `docs/build-any-ai-application.md` (Section 5 precedence and creation order).
- Root `AGENTS.md`, `process/README.md`, `formats/README.md`, `.agents/skills/README.md`, `scripts/README.md`, and `clients/README.md`.
- Every specific process file in `process/`, format file in `formats/`, skill in `.agents/skills/`, subtree `AGENTS.md`, and active document in `clients/` (or catalogs) that touches the area being changed.
- `scripts/check.py`.

## Procedure

1. **Diagnose the request.** Read the operator's change request and inspect the repository inventories (`AGENTS.md`, `process/README.md`, `formats/README.md`, `.agents/skills/README.md`, `scripts/README.md`). Identify the root cause: is the request changing global scope/boundaries, a stage or branch in a business process, the schema of a document, a folder guardrail, a skill's step-by-step procedure, or a missing check in `scripts/check.py`?
2. **Run top-down impact analysis.** Walk the precedence chain in order and list every file that must change so no two mechanisms disagree:
   1. **Global Context (`AGENTS.md`):** Does the change alter application scope, target AI capabilities, universal file rules, or systemic `Never` rules? If so, note the version bump in `# AGENTS.md — global context (version N)`.
   2. **Processes (`process/*.md`):** Does the change add, remove, or modify a stage, entry criteria, graduation criteria, branching/terminal path, system of record, or implementing skill? If so, note the version bump in `# Process: <slug> (version N)` and any change to `process/README.md`.
   3. **Formats (`formats/*.md`):** Does the process or skill change require a new section, table column, or vocabulary Display Name that the governing format does not currently hold? Remember: **the format wins**. If a new field or vocabulary value is needed, the format must be updated first with a `format_version` bump in `# Format: <name> (version N)` (and `formats/handoff.md` updated if it is a client format).
   4. **Active Data Migration (`clients/<slug>/*` and catalogs):** If any format's `format_version` bumps, list every active document in `clients/` (excluding frozen historical snapshots like `prior-plans/`) and any shared catalog that must be migrated to the new `format_version` in the same commit.
   5. **Subtree Agents (`<dir>/AGENTS.md`):** Do any directory-level `AGENTS.md` files need updated rules?
   6. **Skills (`.agents/skills/<name>/SKILL.md`):** Which existing skills need updated `Inputs`, `Reads`, `Procedure`, `Writes`, `Stops when`, or `Never` sections, or what new skill must be created and added to `.agents/skills/README.md`?
   7. **Deterministic Scripts (`scripts/check.py`):** What schema, vocabulary, reference, or stage validation rules in `scripts/check.py` must be added or updated to enforce the change?
3. **Write and present the proposal.** Write the structured impact analysis to `tmp/improve-process-proposal.md` (uncommitted) and present it clearly to the operator in chat:
   - Summary of the change and why it fixes the friction or satisfies the requirement.
   - Exact list of files to be created or modified, grouped by mechanism (`1. Global Context`, `2. Processes`, `3. Formats & Active Data Migrations`, `4. Subtree Agents`, `5. Skills`, `6. Scripts & Inventories`).
   - Exact schema or stage diffs proposed.
   Ask the operator to approve the proposal, request adjustments, or cancel. **Stop and wait for the operator's answer before editing any governed file.**
4. **Apply changes atomically on approval.** Once the operator approves:
   - Edit `AGENTS.md` (if impacted).
   - Edit `formats/*.md` (bumping `format_version` where changed) and `formats/README.md`, and migrate any active documents in `clients/` (setting `format_version` to the new version and updating `updated` to today and `updated_by` to the operator's email; writing `None` for any newly added section whose value is not yet known and opening a row in `open-issues.md`).
   - Edit `process/*.md` (bumping the process version) and `process/README.md`.
   - Edit any impacted `<dir>/AGENTS.md` files.
   - Edit or create `.agents/skills/<name>/SKILL.md` and update `.agents/skills/README.md`.
   - Update `scripts/check.py` to enforce the new or revised format/process rules.
5. **Verify the repository.** Run `python3 scripts/setup-scripts.py` (to wire any added or renamed skills) and `python3 scripts/check.py`. Fix any errors reported until both exit 0.
6. **Report completion.** Summarize the applied changes by mechanism and leave the working tree ready for the operator to review `git diff` and commit.

## Writes

- `tmp/improve-process-proposal.md` (uncommitted proposal record).
- On operator approval: the impacted files across `AGENTS.md`, `formats/`, active documents in `clients/`, `process/`, subtree `AGENTS.md` files, `.agents/skills/`, `scripts/check.py`, and directory `README.md` inventories.

## Stops when

If the operator rejects the proposal, stops immediately with no governed files modified. If the operator approves, stops when all mechanisms, active documents, and inventories are updated atomically and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` pass with zero errors.

## Never

- Never edit any governed file in the repository before the operator has explicitly approved the proposal from Step 3.
- Never change a skill to write a section or vocabulary value that its governing format in `formats/` does not allow; always update the format first.
- Never bump `format_version` in a format file without updating `scripts/check.py` and migrating all active documents of that format in the same run.
- Never invent values when migrating existing client documents to a new format version; write `None` and open an issue in `clients/<slug>/open-issues.md`.
- Never edit frozen historical snapshots (such as `prior-plans/`) or archived folders under `archive/`.
