---
name: setup-application
description: Configure shared system records, complete reserved framework files, and set this repository up from scratch when those files are missing.
---

# setup-application

## When to use

Use this skill to configure the application. With an operator request, change the `system/` files that request requires. With no request, scan the reserved framework files and `system/`, then interview the operator until required setup is complete. A repository with those files missing is set up from scratch. Also use this skill to choose external systems and to finish the shared administration those systems need.

## Boundaries

This skill covers application setup in `system/` and the framework contracts. Client onboarding is `setup-client`. A domain workflow created during setup is its own file in `process/`. A template upgrade is `upgrade-app`. A change to a process, format, skill, or checker is `improve-process`.

- **Entry.** The operator invokes this skill with a configuration request, or with no request, and `docs/build-any-ai-application.md` is readable.
- **Graduation.** Every required framework file exists, every `system/` registry is filled from the operator's answers or explicitly confirmed empty, external-system administration the operator chose to finish is recorded, and `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` exit with zero errors.
- **Configured.** Setup is complete and live operation can start.
- **Mechanism change.** Hand the request to `improve-process` instead of patching it here.
- **Revision needed.** The operator rejects part of a proposed global context, process, or format. Revise that mechanism before continuing down the creation order.
- **Aborted.** The operator cancels before completion. Do not leave a partial unlinted change to be committed.
- Follow creation order for missing framework files: Global Context, Process, Formats, Subtree Agents, Skills, Scripts, then system and client data.
- A system-data edit that does not change a mechanism stays in this skill.
- Interstitial setup reports stay in `tmp/`. Upgrade plans belong in `docs/upgrades/` and are written by `upgrade-app`.

## Inputs

- An optional configuration request. If the operator does not provide one, run the completeness scan.
- Operator email address, asked once if it is not known.
- Target AI environment (`Claude`, `OpenAI`, or `Gemini`) when framework files are missing or the operator is switching vendors.
- The operator's answers for any `None` registry they have not explicitly confirmed as empty.

## Reads

- `docs/build-any-ai-application.md`.
- `process/README.md` and `process/AGENTS.md`, and any domain process the request names.
- `formats/README.md`, `formats/AGENTS.md`, and the format contract for every `system/` file being edited.
- Root `AGENTS.md` and `formats/system/global-context.md`.
- `system/README.md`, `system/AGENTS.md`, and every governed file in `system/`.
- `.agents/skills/README.md`, `.agents/skills/AGENTS.md`, `scripts/README.md`, `scripts/AGENTS.md`, `clients/README.md`, and `clients/AGENTS.md`.

## Procedure

1. **Read the contracts.** Read `docs/build-any-ai-application.md` and the Boundaries above before editing. Ask for the operator email if it is unknown.
2. **Route a supplied request.** When the operator supplied a request, list the `system/` files it changes and wait for the operator to confirm that list.
   - If the request changes a process, format, skill, or `scripts/check.py`, stop and hand it to `improve-process`.
   - If it changes users, roles, or client assignments, follow `update-user` for that part.
   - If it changes the backlog, follow `add-to-backlog`.
   - If it changes external systems, continue with steps 5 and 6.
   - Write only the confirmed system records, then go to step 7.
3. **Scan when no request is supplied.** Check these reserved files: root `AGENTS.md`; `README.md` and `AGENTS.md` in `process/`, `formats/`, `.agents/skills/`, `scripts/`, `clients/`, and `system/`; and every governed file named by `system/README.md`. Run `python3 scripts/check.py` and keep every finding.
4. **Build missing framework files in creation order.** For each missing reserved framework file, interview the operator and write it only after approval at Global Context, Processes, and Formats:
   1. Root `AGENTS.md` under `formats/system/global-context.md`.
   2. Domain process files the operator defines, under `formats/system/process.md`, and `process/README.md`. Do not recreate process documents for the skills that ship with this template.
   3. Format contracts under `formats/system/` or `formats/clients/`, and `formats/README.md`.
   4. Subtree `AGENTS.md` files.
   5. Skills under `.agents/skills/`, preserving `improve-process`, `setup-client`, `review-question-journal`, and the other base skills in `.agents/skills/README.md`.
   6. `scripts/check.py` checks for every format, then `python3 scripts/setup-scripts.py --env <claude|openai|gemini>`.
   Keep `docs/build-any-ai-application.md` and the base skills. Do not remove them to make a domain-specific repository.
5. **Interview for external systems.** When `system/external-systems.md` is `None` and the operator has not confirmed that no external system is wanted, ask which systems agents should coordinate with. Examples the operator may name include a work tracker, a CRM, an email system, or a calendar. For each system, record only what the operator supplies: display name, category, purpose, and coordination guidance. Create a `Planned` record. Do not invent a URL or a setup step.
6. **Walk shared administration.** For each `Planned` system, walk the operator through the shared installation or administration required before any user connects. Write those steps into `## System Administration` and the per-user steps into `## User Connection`, in the operator's words. Set `## Status` to `Active` only when the operator says the shared setup is finished. If the operator defers a step, leave the system `Planned` and record the remaining step. Never write a secret. Per-user connections belong to `setup-my-integrations`, not this step.
7. **Complete empty system registries.** Treat a `None` body as incomplete until the operator either supplies records or explicitly confirms that the registry stays empty. Do not leave users and roles unconfirmed: ask for at least one role and one person. If the operator defers both, leave the registries `None` and record that deferral in the setup report. Assignments, the backlog, and the question journal may stay `None` after an explicit confirmation.
8. **Verify and report.** Update `updated` and `updated_by` on every system file touched. Run `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py`. Fix every error. Write `tmp/setup-application-report.md` with the files written, the registries confirmed empty, and any deferred item.

## Writes

- The `system/` records the request or the scan changed.
- Missing reserved framework files when the scan finds them absent: root `AGENTS.md`, process files, format contracts, subtree `AGENTS.md` files, skills, `scripts/check.py`, and the directory inventories.
- Vendor skill links through `scripts/setup-scripts.py`.
- `tmp/setup-application-report.md`.

## Stops when

The supplied request has been applied to the confirmed `system/` files, or the no-request scan has created every missing reserved file and the operator has either filled or explicitly confirmed each required registry. External-system administration the operator chose to finish is recorded. `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py` pass with zero errors, and `tmp/setup-application-report.md` is written. The operator reviews the diff and commits.

## Never

- Never store a credential, token, password, or unredacted payment number.
- Never invent a business rule, external-system URL, or setup step the operator did not supply.
- Never delete a system record. Retire an external system by status.
- Never apply a process, format, skill, or checker change inside this skill. Hand that change to `improve-process`.
- Never remove `improve-process`, `setup-client`, or `docs/build-any-ai-application.md`.
- Never write the setup report outside `tmp/`.
