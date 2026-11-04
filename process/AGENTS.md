# AGENTS.md — process/

The files here are lifecycle stage files, each holding the business processes of one customer lifecycle stage. The skills that ship with the template do not have process documents in this directory; their stage rules live in the skill. Every lifecycle stage file must conform to `formats/system/process.md`.

- A lifecycle stage file is prose, process sections, stage definitions, and tables. It carries no YAML front matter. Its first line is `# Lifecycle Stage: <slug> (version N)`, where `<slug>` is the filename stem the operator chose.
- Each `# <Process Name>` section is one process. Process names are Title Case, unique across every file in this directory, and are referenced everywhere by their exact heading text. A process follows the exact `##` section order in `formats/system/process.md`.
- Every process is decomposed into discrete stages (`### Stage 1: ...`, `### Stage 2: ...`), each small enough to hand off between sessions and each declaring `#### Entry Criteria`, `#### Owner`, `#### Description`, `#### Graduation Criteria`, `#### Branching and Terminal Paths`, and `#### Implementing Skills`.
- Every stage is owned. `#### Owner` is a bullet list of `Active` role slugs from `system/user-roles.md` (first owns, the rest back up) or an Automation line (`Automation: On-Demand` or `Automation: Recurring (<schedule>)`). An Automation stage names at least one implementing skill and is never `Manual (Gap)`.
- Every process declares `## Supervisor Role`, one `Active` role slug that checks the process is executed properly.
- Every process declares `## System of Record` (`Repository Markdown` or `External System` with a link). A client's run of the process is tracked as an `# In Flight` row in `clients/<slug>/open-items.md`.
- A process never restates a format's full field schema or a skill's internal step list. It names the format or skill and states the business intent and stage boundaries.
- Numbers in a process (cadences, windows, lead times) are defaults for every client. Client-specific commercial overrides live in `clients/<slug>/client.md`, never here.
- Prefer owning a stage with an existing role over adding a new one. Roles are groups of people who do work, not titles.
- When any process in a file changes, bump `(version N)` in that file's title line and update `process/README.md` in the same commit. When the change alters what a skill must do, update the skill in the same commit via `improve-process`. When it requires a document field that no format holds, update the format in `formats/` first.
- Run `python3 scripts/check.py` after any edit here.
