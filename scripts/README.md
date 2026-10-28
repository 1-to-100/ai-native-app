# Scripts — inventory

Read this before running a script. `check.py` only reports and never edits a document. `setup-scripts.py` only manages skill exposure symlinks for the chosen AI environment and never edits a skill or document.

| Script | Does | Run |
| --- | --- | --- |
| [`setup-scripts.py`](setup-scripts.py) | Wires and verifies skill exposure for the repository's target AI environment (`Claude`, `OpenAI`, or `Gemini`). Reads `# Target AI Environment` -> `## Vendor` from `AGENTS.md` by default, or accepts `--env claude\|openai\|gemini`. For `Claude`, creates `.claude/skills/<name>` as a relative symlink to `../../.agents/skills/<name>` so every skill is a `/<name>` slash command. For `OpenAI`, verifies `.agents/skills/<name>/SKILL.md` and `AGENTS.md` are in place natively. For `Gemini`, creates `.gemini/skills/<name>` symlinks and links `GEMINI.md` to `AGENTS.md`. Also verifies every `SKILL.md` has valid front matter (`name` matching folder name and `description`). | `python3 scripts/setup-scripts.py` after adding, renaming, or removing a skill; `python3 scripts/setup-scripts.py --env <claude\|openai\|gemini>` when configuring the target AI environment; `python3 scripts/setup-scripts.py --check` to report only (exits non-zero on any problem). |
| [`check.py`](check.py) | Lints the entire repository against its contracts: root `AGENTS.md` against `formats/system/global-context.md`; every process in `process/` against `formats/system/process.md`; every namespaced format contract under `formats/system/` and `formats/clients/`; directory inventories against the files on disk; every required record in `system/`; the optional `system/products-and-services.md`; every client folder against `formats/clients/client.md`, `formats/clients/open-issues.md`, `formats/clients/decision-log.md`, and the optional `formats/clients/order-form.md`; cross-record references; and staged git changes via `--staged`. Prints one line per finding as `ERROR` or `WARN` and exits non-zero on any error. | `python3 scripts/check.py` for the whole repository; `python3 scripts/check.py <client-slug>` for one client folder; `python3 scripts/check.py --staged` before committing modified system or client documents. |

Requirements: Python 3.9 or later, standard library only.

Regression tests for `check.py` live in `scripts/tests/` and are not inventory scripts. Run them with `python3 -m unittest scripts/tests/test_check.py`.

## When to run

- At the end of every skill, as each `SKILL.md` specifies.
- Before every commit (`python3 scripts/check.py` and `python3 scripts/setup-scripts.py --check`).
- In CI on every pull request (a failing check blocks the merge).

## Adding a script

Keep it standard-library Python, read-only on governed documents, and add a row to the table above in the same commit. The inventory and the directory must always agree.
