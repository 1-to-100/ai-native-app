---
name: create-application
description: Interview the operator and bootstrap this repository into a tailored AI-native application in strict creation order.
---

# create-application

## When to use

Run once when bootstrapping a new AI-native application from this base template repository, or when resetting the application's core domain definition. This skill interviews the operator, configures the repository for their chosen AI vendor environment (`Claude`, `OpenAI`, or `Gemini`), and builds the application's mechanisms in strict creation and precedence order: Global Context (`AGENTS.md`) -> Processes (`process/`) -> Formats (`formats/`) -> Subtree Agents (`<dir>/AGENTS.md`) -> Skills (`.agents/skills/`) -> Scripts (`scripts/check.py`).

## Inputs

- Target AI environment: `Claude`, `OpenAI`, or `Gemini` (asked first if not provided).
- Operator email address (asked once if not known).
- Operator's answers during the structured interview covering:
  1. Application mission, in-scope workflows, out-of-scope boundaries, and systemic `Never` rules.
  2. Core business workflows, their stages, entry/graduation criteria, branching paths (such as `Closed Won` / `Closed Lost` or `Approved` / `Rejected`), and system of record (`Repository Markdown` vs. `External System` like Jira, Linear, or HubSpot).
  3. The documents, client/entity files, and shared catalogs those processes read and write.

## Reads

- `docs/build-any-ai-application.md` (the master governing blueprint).
- `AGENTS.md` and `formats/global-context.md`.
- `process/README.md`, `process/AGENTS.md`, `process/application-lifecycle.md`, and `formats/process.md`.
- `formats/README.md`, `formats/AGENTS.md`, `formats/client.md`, `formats/open-issues.md`, and `formats/handoff.md`.
- `.agents/skills/README.md`, `scripts/README.md`, `scripts/check.py`, and `scripts/setup-scripts.py`.

## Procedure

1. **Read the blueprint.** Read `docs/build-any-ai-application.md` and `formats/global-context.md` and `formats/process.md` in full so every file generated conforms to the factory standard.
2. **Select and optimize for the target AI environment.** Ask the operator which AI vendor environment they are building for (`Claude`, `OpenAI`, or `Gemini`) and ask for their operator email address. Explain the vendor-specific configuration from Section 7.2 of `docs/build-any-ai-application.md` and run `python3 scripts/setup-scripts.py --env <claude|openai|gemini>` to wire the environment.
3. **Station 1 — Global Context (`AGENTS.md`).** Interview the operator to capture:
   - What the application is, who operates it, and what business outcomes it produces (`# Application Overview`).
   - What workflows and records are in scope (`## In Scope`) and what stays outside the repository (`## Out of Scope`).
   - How the chosen AI environment's native capabilities will be used (`# Target AI Environment`).
   - Any domain-specific universal file rules (`# Every File`) or systemic hard lines (`# Never`) to add to the base rules.
   Present the proposed root `AGENTS.md` in chat and wait for the operator's explicit approval before writing `AGENTS.md`.
4. **Station 2 — Processes (`process/`).** Interview the operator to identify the core workflows the application runs. For each workflow:
   - Determine its slug, purpose, scope, participating roles, and cadence/triggers.
   - Determine its `# System of Record`: whether items are tracked natively in `Repository Markdown` (and in which folders/formats) or in an `External System` (such as Jira, Linear, HubSpot, or Salesforce, with its `https://` URL).
   - Break the workflow into discrete, handoff-sized stages (`## Stage 1: ...`, `## Stage 2: ...`). For every stage, define `### Entry Criteria`, `### Description`, `### Graduation Criteria`, `### Branching and Terminal Paths` (naming every branch such as `Closed Won`, `Closed Lost`, `Approved`, `Rejected`, `Deferred`, or `Cancelled`), and `### Implementing Skills` (naming the skill slug or `Manual (Gap)`).
   Present the stage breakdown for each process to the operator for approval, then write `process/<slug>.md` conforming to `formats/process.md` and update `process/README.md`. Keep `process/application-lifecycle.md` in place so the bootstrap, onboarding, and improvement stages remain governed.
5. **Station 3 — Formats (`formats/`).** From the inputs and outputs of the approved processes, list every document type and shared catalog the application needs:
   - Review whether `formats/client.md`, `formats/open-issues.md`, and `formats/handoff.md` need additional domain sections or vocabulary rows.
   - Define a new `formats/<name>.md` contract for each additional document type or catalog, with `# Purpose`, `# Location`, `# Header`, `# Body`, `# Rules`, `# Vocabularies`, and `# Checks`.
   Present the format inventory and section structures to the operator for approval, then write the format files, update `formats/handoff.md` if new client files were added, and update `formats/README.md`.
6. **Station 4 — Subtree Agents (`<directory>/AGENTS.md`).** Create any new shared catalog directories (with their `README.md` inventory and local `AGENTS.md` contract) and update `clients/AGENTS.md`, `process/AGENTS.md`, or `formats/AGENTS.md` if domain-specific folder rules are required.
7. **Station 5 — Skills (`.agents/skills/`).** For every stage in `process/*.md` that names an implementing skill:
   - Keep `create-application` and `improve-process` intact.
   - Update `.agents/skills/setup-client/SKILL.md` if new client document formats were added to the handoff.
   - Create `.agents/skills/<skill-name>/SKILL.md` for each new domain skill with YAML front matter (`name`, `description`) and the seven mandatory sections (`## When to use`, `## Inputs`, `## Reads`, `## Procedure`, `## Writes`, `## Stops when`, `## Never`).
   - Update `.agents/skills/README.md` and run `python3 scripts/setup-scripts.py --env <claude|openai|gemini>` so every skill is exposed in the target AI environment.
8. **Station 6 — Deterministic Verification (`scripts/check.py`).** Update `scripts/check.py` so it validates any newly added or modified format contracts in `formats/` and any new catalog directories. Run `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` and fix any findings until both exit with zero errors.
9. **Write the bootstrap report.** Update root `README.md` with the new domain skills and directories, and write a complete summary of what was created to `tmp/create-application-report.md` (uncommitted).

## Writes

- Root `AGENTS.md` and `README.md`.
- `process/<slug>.md` and `process/README.md`.
- `formats/<name>.md` and `formats/README.md`.
- Any new catalog directories with `<catalog>/README.md` and `<catalog>/AGENTS.md`.
- `.agents/skills/<skill-name>/SKILL.md`, `.agents/skills/README.md`, and vendor skill symlinks via `scripts/setup-scripts.py`.
- `scripts/check.py` (when new format checks are added).
- `tmp/create-application-report.md` (uncommitted interstitial report).

## Stops when

All six creation stations are completed with operator approval at Global Context, Processes, and Formats; `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` pass with zero errors; and `tmp/create-application-report.md` is written. The operator reviews `git status` and commits.

## Never

- Never skip the creation order (`Global Context` -> `Process` -> `Formats` -> `Subtree Agents` -> `Skills` -> `Scripts`).
- Never write processes, formats, or skills before the operator has selected a target AI environment and approved the Global Context.
- Never invent business rules, commercial terms, or external system URLs the operator did not supply; ask the operator or mark unresolved items explicitly.
- Never remove `improve-process`, `setup-client`, `docs/build-any-ai-application.md`, or `process/application-lifecycle.md`.
- Never write interstitial drafts or reports outside `tmp/`.
