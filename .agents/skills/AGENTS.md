# AGENTS.md — skills/

The folders here are the procedural skills agents execute. Each skill is `.agents/skills/<name>/SKILL.md`.

- A skill has YAML front matter with `name` equal to the folder name and a non-empty `description`, then `## When to use`, `## Inputs`, `## Reads`, `## Procedure`, `## Writes`, `## Stops when`, and `## Never`.
- A skill executes a stage named by a process. It does not restate the format schema or quietly widen the process.
- When a skill and a format disagree, the format wins. Update the skill, or change the format first through `improve-process`.
- Add, rename, or remove a skill only together with a row in `.agents/skills/README.md` and a run of `python3 scripts/setup-scripts.py`.
- A skill that writes a governed data file sets `updated` and `updated_by` to the human operator's email.
- Do not store credentials in a skill, a prompt example, or a file the skill writes.
