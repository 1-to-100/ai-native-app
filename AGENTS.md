# AGENTS.md — global context (version 1)

# Application Overview
This repository is an AI-native application built on the 1 to 100 repeatable factory framework defined in `docs/build-any-ai-application.md`. People and agents read and write the same structured Markdown documents under explicit process contracts (`process/`), document schemas (`formats/`), procedural skills (`.agents/skills/`), and deterministic verification scripts (`scripts/`). In its starting state, this repository is ready for the operator to run `create-application` to tailor the application to a specific business domain, or to run `setup-client` and `improve-process` directly.

# Scope and Out of Scope
## In Scope
- Defining and running stage-by-stage business processes in `process/` governed by `formats/process.md`.
- Enforcing structured Markdown schemas in `formats/` across all client and entity folders in `clients/`.
- Executing repeatable stage workflows through skills in `.agents/skills/` and verifying every change with `scripts/check.py`.
- Evolving the application's mechanisms atomically through `improve-process`.

## Out of Scope
- Upstream prospect discovery or external sales execution prior to a valid handoff file, unless added via `create-application` or `improve-process`.
- Storing credentials, secrets, API tokens, or unredacted payment details.
- Bespoke, unversioned chat workflows that leave no durable record in this repository.

# Target AI Environment
## Vendor
Claude

## Skill Invocation
Invoke skills in Claude Code as `/<skill-name>` (exposed via `.claude/skills/<skill-name>` symlinks to `.agents/skills/<skill-name>`). Run `python3 scripts/setup-scripts.py --env <claude|openai|gemini>` during `create-application` if you switch this repository to OpenAI (`$<skill-name>`) or Gemini (`@<skill-name>`).

## Native Capabilities
Optimized for Claude Code slash commands, fresh-context subagents for verification and research, and Claude Artifacts when generating client-facing decks or review drafts from repository data.

# Before You Act
1. Read `process/README.md` to see which process governs the work, and read the process document itself in `process/` for its stages, entry criteria, graduation criteria, branching paths, and where a stage stops.
2. Read `.agents/skills/README.md` to see the inventory of skills before executing one. If a skill covers the stage, invoke it by name (`/create-application`, `/setup-client`, `/improve-process`) rather than improvising the procedure by hand.
3. Read `formats/README.md` and the governing format contract in `formats/` for every document you will write or edit. The format contract is the single source of truth for that document's header, sections, and vocabularies.
4. Read `scripts/README.md` before running a script.
5. When bootstrapping or restructuring the application, read `docs/build-any-ai-application.md`.

# Every File
- Every governed Markdown file under `clients/` (and any shared catalog directory) opens with the standard YAML header defined in `formats/README.md` and nothing else in front matter unless its format contract explicitly adds `status`.
- The `format` key names the format file in `formats/` that governs the document. The document follows that format exactly: the sections, their order, their heading levels, and vocabulary values written as Display Names.
- Keep every file you touch in format as you go. Run `python3 scripts/check.py` before you commit and fix every error it reports.
- `updated` and `updated_by` change in every commit that touches a governed file. `created_by` and `updated_by` always hold the human operator's email address—never a name, handle, or agent identifier.
- A required section with nothing to say holds the single line `None`. Never delete a section the format lists.
- References use slugs for files, exact heading text for records inside a multi-record file, and exact Display Names for vocabulary values. Every reference must resolve.
- Interstitial working files, drafts, proposals, and setup reports go in `tmp/` (which is git-ignored) and are never committed.
- When a skill and a format disagree, the format wins; fix the skill. When a process and a skill disagree, the process states the business intent and the skill is brought to it—unless the format forbids it, in which case the format changes first or the process yields.

# Never
- Never delete a client folder, a catalog item, a prior plan, a built deliverable, or a closed issue. Retire a client folder by moving it to `archive/<slug>/` with an `ARCHIVED.md` note.
- Never remove or reword a row in a `# Decisions` or `# Closed` table. A reversal is a new row.
- Never invent a fact, a metric, a quote, a reason to believe, a client reaction, or a commercial term. Write `None` and open an issue in `open-issues.md` when a source is silent.
- Never store credentials, API keys, passwords, or unredacted payment card/bank numbers anywhere in this repository.
- Never let one client folder under `clients/<slug>/` reference, copy from, or compare against another client folder.
