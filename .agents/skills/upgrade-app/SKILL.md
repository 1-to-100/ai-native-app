---
name: upgrade-app
description: Plan and apply an upgrade from the current template application, then independently review the result.
---

# upgrade-app

## When to use

Use this skill when the operator wants this repository brought up to the current template application paradigm at `https://github.com/1-to-100/ai-native-app`. The template's `docs/build-any-ai-application.md` is the process to follow.

## Inputs

- Operator confirmation to start the upgrade.
- A worktree with no unrelated uncommitted changes.
- Network access to the template repository.

## Reads

- `process/application-lifecycle.md` Stage 2.
- The local `docs/build-any-ai-application.md`, so the comparison has a starting point.
- After the clone: the template's `docs/build-any-ai-application.md` and the template files that document names, including root `AGENTS.md`, `process/`, `formats/`, `system/`, `.agents/skills/`, and `scripts/`.

## Procedure

1. **Preflight.** Run `git status --short`. If it shows uncommitted changes, stop and tell the operator to commit or stash them first. Do not discard local work. Confirm the template URL `https://github.com/1-to-100/ai-native-app`.
2. **Clone the template.** Clone that URL into a temporary directory outside this repository. Read the template's `docs/build-any-ai-application.md` in full. Then read the template files that process tells an application to contain.
3. **Compare in creation order.** Using the template's creation order, identify the template paradigms this repository must adopt. Do this analysis to prepare the plan. Do not put the analysis of the current repository into the plan document.
4. **Write the upgrade plan.** Write `docs/upgrades/<YYYY-MM-DD>-template-upgrade.md`. The document is a narrow step-by-step procedure for making this repository conform to the template. It does not report the current state of this repository. Leave the plan untracked. Tell the operator they can explicitly add it, and its `docs/README.md` inventory row, when they want it in the repository.
5. **Run two subagents in parallel.**
   - One subagent receives the upgrade plan and executes it.
   - A separate fresh-context subagent receives the upgrade plan and the template structure, and writes `tmp/upgrade-review-plan.md`. That subagent does not edit the repository and does not see the implementation chat.
6. **Review and fix.** When both finish, give a final fresh-context subagent the review plan and the resulting diff. It checks the upgrade against the plan and the template structure, and it fixes gaps. It does not add unrelated redesign.
7. **Verify.** Run `python3 scripts/setup-scripts.py --check` and `python3 scripts/check.py`. Fix every error those checks report.
8. **Report.** Tell the operator the upgrade is complete, and give the path of the upgrade plan.

## Writes

- `docs/upgrades/<YYYY-MM-DD>-template-upgrade.md`, left untracked until the operator explicitly adds it.
- The repository files the upgrade plan names.
- `tmp/upgrade-review-plan.md`.

## Stops when

The preflight stops the run because the worktree is dirty or the template cannot be cloned, or the final review subagent has finished, both verification commands pass, and the operator has been told the upgrade is complete.

## Never

- Never discard uncommitted work to clear the preflight.
- Never write a current-state report into the upgrade plan.
- Never let the implementing context perform the final review.
- Never store template credentials or this repository's secrets in the plan or the temporary clone notes.
- Never delete client, system, or history records as a way to make the tree match the template. Archive or retire them by the repository's own rules.
