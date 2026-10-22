# AGENTS.md — global context (version 2)

# Application Overview
This repository is an AI-native application built on the 1 to 100 repeatable factory framework defined in `docs/build-any-ai-application.md`. People and agents read and write the same structured Markdown documents under explicit process contracts (`process/`), document schemas (`formats/`), procedural skills (`.agents/skills/`), and deterministic verification scripts (`scripts/`). Shared application data lives in `system/`. Client-specific data lives in `clients/<slug>/`. In its starting state, this repository is ready for the operator to run `setup-application` to configure it, or to run `setup-client` and `improve-process` directly.

# Scope and Out of Scope
## In Scope
- Defining and running stage-by-stage business processes in `process/` governed by `formats/system/process.md`.
- Enforcing structured Markdown schemas in `formats/system/` and `formats/clients/`.
- Storing people, roles, client-role assignments, external-system guidance, the application backlog, and the question journal in `system/`.
- Executing repeatable stage workflows through skills in `.agents/skills/` and verifying every change with `scripts/check.py`.
- Evolving the application's mechanisms atomically through `improve-process`, and upgrading the repository to the current template paradigm through `upgrade-app`.

## Out of Scope
- Upstream prospect discovery or external sales execution prior to a valid handoff file, unless added via `setup-application` or `improve-process`.
- Storing credentials, secrets, API tokens, or unredacted payment details.
- Bespoke, unversioned chat workflows that leave no durable record in this repository.
- Client business facts, commercial terms, contacts, or cross-client comparisons inside `system/`.

# Target AI Environment
## Vendor
Claude

## Skill Invocation
Invoke skills in Claude Code as `/<skill-name>` (exposed via `.claude/skills/<skill-name>` symlinks to `.agents/skills/<skill-name>`). Run `python3 scripts/setup-scripts.py --env <claude|openai|gemini>` during `setup-application` if you switch this repository to OpenAI (`$<skill-name>`) or Gemini (`@<skill-name>`).

## Native Capabilities
Optimized for Claude Code slash commands, fresh-context subagents for verification and research, and Claude Artifacts when generating client-facing decks or review drafts from repository data.

# Before You Act
1. Read `process/README.md` to see which process governs the work, and read the process document itself in `process/` for its stages, entry criteria, graduation criteria, branching paths, and where a stage stops.
2. Read `.agents/skills/README.md` to see the inventory of skills before executing one. If a skill covers the stage, invoke it by name (`/setup-application`, `/setup-client`, `/improve-process`) rather than improvising the procedure by hand.
3. Read `formats/README.md` and the governing format contract in `formats/system/` or `formats/clients/` for every document you will write or edit. The format contract is the single source of truth for that document's header, sections, and vocabularies.
4. Read the nearest subtree `AGENTS.md` before editing files in that directory. During client-specific work, follow `system/AGENTS.md`: read users, roles, external-system guidance, and the assignment rows for the client being served.
5. Read `scripts/README.md` before running a script.
6. When bootstrapping, configuring, or restructuring the application, read `docs/build-any-ai-application.md`.

# Every File
- Every governed Markdown file under `system/` opens with the system YAML header defined in `formats/README.md`. Every governed Markdown file under `clients/` opens with the client YAML header. Neither header adds keys unless its format contract explicitly adds `status`.
- The `format` key is the namespaced identifier of the contract under `formats/`, such as `system/users` or `clients/client`. The document follows that format exactly: the sections, their order, their heading levels, and vocabulary values written as Display Names.
- Keep every file you touch in format as you go. Run `python3 scripts/check.py` before you commit and fix every error it reports.
- `updated` and `updated_by` change in every commit that touches a governed file. `created_by` and `updated_by` always hold the human operator's email address—never a name, handle, or agent identifier.
- A required section with nothing to say holds the single line `None`. An empty multi-record registry is the single line `None`. Never delete a section the format lists.
- References use namespaced format identifiers, exact heading text for records inside a multi-record file, and exact Display Names for vocabulary values. Every reference must resolve.
- Interstitial working files, drafts, proposals, and setup reports go in `tmp/` (which is git-ignored) and are never committed. Upgrade plans written for `upgrade-app` go in `docs/upgrades/`.
- When a skill and a format disagree, the format wins; fix the skill. When a process and a skill disagree, the process states the business intent and the skill is brought to it—unless the format forbids it, in which case the format changes first or the process yields.

# Never
- Never delete a client folder, a catalog item, a prior plan, a built deliverable, a user, a role, an assignment, a backlog item, a journal row, or a closed issue. Retire a client folder by moving it to `archive/<slug>/` with an `ARCHIVED.md` note. Retire a person or role by status. End an assignment by status and date.
- Never remove or reword a row in a `# Decisions`, `# Closed`, or other history table. A reversal is a new row.
- Never invent a fact, a metric, a quote, a reason to believe, a client reaction, or a commercial term. Write `None` and open an issue in `clients/<slug>/open-issues.md` when a client source is silent.
- Never store credentials, API keys, passwords, or unredacted payment card or bank numbers anywhere in this repository.
- Never let one client folder under `clients/<slug>/` reference, copy from, or compare against another client folder.
- Never store a client business fact in `system/`. A client slug in `system/client-assignments.md` is routing metadata only.
