# AGENTS.md — process/

The files here are the governing processes for the business scope of this repository. Every process document must conform to `formats/system/process.md`.

- A process is prose, stage definitions, and tables. It carries no YAML front matter. Its first line is `# Process: <slug> (version N)`, and it follows the exact section order in `formats/system/process.md`.
- Every workflow is decomposed into discrete stages (`## Stage 1: ...`, `## Stage 2: ...`), each small enough to hand off between sessions and each declaring `### Entry Criteria`, `### Description`, `### Graduation Criteria`, `### Branching and Terminal Paths`, and `### Implementing Skills`.
- Every process declares `# System of Record` (`Repository Markdown` or `External System` with a link).
- A process never restates a format's full field schema or a skill's internal step list. It names the format or skill and states the business intent and stage boundaries.
- Operational roles in `system/user-roles.md` tell an agent what a person does. They do not replace the process-participant vocabulary in `process/README.md`.
- Numbers in a process (cadences, windows, lead times) are defaults for every client. Client-specific commercial overrides live in `clients/<slug>/client.md`, never here.
- When a process changes, bump `(version N)` in its title line and update `process/README.md` in the same commit. When the change alters what a skill must do, update the skill in the same commit via `improve-process`. When it requires a document field that no format holds, update the format in `formats/` first.
- Run `python3 scripts/check.py` after any edit here.
