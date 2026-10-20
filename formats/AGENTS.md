# AGENTS.md — formats/

The files here are format contracts. Each one is the single source of truth for one kind of document: its header, its sections in order, the vocabularies it selects from, and what `scripts/check.py` enforces on it.

- A format changes only together with every file that follows it. When you change a format, in the same commit: bump the version in the format file's title line (`# Format: <name> (version N)`), update `formats/README.md` if needed, update every active document in the repository that carries that format, and update the matching validation rules in `scripts/check.py`. Frozen historical snapshots (such as `prior-plans/`) keep the version they were written under.
- Vocabularies live in the format that uses them unless shared across multiple formats.
- A format file is prose, fenced templates, and tables. It carries no YAML front matter; its first line is `# Format: <slug> (version N)`.
- The text under each heading in a format's `# Body` template states what that section holds, how it is written, and the rules a checker applies to it.
- Run `python3 scripts/check.py` after any edit here.
