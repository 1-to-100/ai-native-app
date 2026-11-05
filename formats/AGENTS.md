# AGENTS.md — formats/

The files here are format contracts. Each one is the single source of truth for one kind of document: its header, its sections in order, the vocabularies it selects from, and what `scripts/check.py` enforces on it.

- Put a contract in `formats/system/` when it governs root context, a process, or a file in `system/`. Put it in `formats/clients/` when it governs a file in `clients/<slug>/`. Put it in `formats/external/` when it governs a document that lives in an external system (a Claude Design artifact, a Google Doc, any other store). All formats of ours, in this repository or outside it, live under `formats/`.
- The format identifier is the path relative to `formats/` without `.md`, using forward slashes, such as `system/users`, `clients/open-items`, or `external/design-page`. The contract's first line is `# Format: <identifier> (version N)`.
- A format changes only together with every file that follows it. When you change a format, in the same commit: bump the version in the format file's title line, update `formats/README.md` if needed, update every active document that carries that format, and update the matching validation rules in `scripts/check.py`. Frozen historical snapshots keep the version they were written under.
- Moving a contract into a namespace changes its identifier. Bump its version when that move or any schema change lands, and migrate active documents in the same commit.
- Vocabularies live in the format that uses them unless shared across multiple formats.
- An external contract uses the same seven sections, starts at version 1, and its `## Location` names the external system and says the documents are never held in this repository. Changing an external contract migrates nothing in this repository; record what an existing external document now owes as an issue for the operator.
- A format file is prose, fenced templates, and tables. It carries no YAML front matter.
- The text under each heading in a format's `## Body` template states what that section holds, how it is written, and the rules a checker applies to it.
- `formats/README.md` is the only format inventory. Do not add a second inventory inside a namespace folder.
- Run `python3 scripts/check.py` after any edit here.
