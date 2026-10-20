# ai-native-app

The base factory repository for building and running any AI-native application. People and agents read and write the same structured Markdown documents under explicit contracts—global context (`AGENTS.md`), stage-by-stage business processes (`process/`), document schemas (`formats/`), procedural skills (`.agents/skills/`), and deterministic verification scripts (`scripts/`).

Read [`docs/build-any-ai-application.md`](docs/build-any-ai-application.md) for the complete blueprint behind this repository.

## Layout

```text
AGENTS.md            the Global Context and repository contract (read first)
docs/                general repository documentation, including build-any-ai-application.md; README.md is the inventory
process/             the governing stage-by-stage processes; README.md is the inventory
formats/             one format contract per document kind; README.md holds shared conventions and the inventory
clients/<slug>/      one isolated folder per client or entity, filenames mirroring format names
archive/             retired client folders and catalog items (nothing is ever deleted)
.agents/skills/      the procedural skills; README.md is the inventory
.claude/skills/      symlinks exposing .agents/skills/ as /<skill> slash commands in Claude Code
scripts/             check.py (the deterministic lint) and setup-scripts.py; README.md is the inventory
tmp/                 git-ignored working folder for interstitial agent files, proposals, and reports
```

## Starting points

- Bootstrap and customize this repository into your specific AI application: `/create-application` (or `$create-application`)
- Onboard a client or entity from a handoff file: `/setup-client <path-to-handoff.md>`
- Propose and apply an upgrade to your processes, formats, skills, and checks: `/improve-process "<what needs to change>"`
- Configure or check skill links for your chosen AI environment (`claude`, `openai`, `gemini`): `python3 scripts/setup-scripts.py [--env claude|openai|gemini] [--check]`
- Lint the entire repository before committing: `python3 scripts/check.py`

## Where things are defined

| Question | Answer lives in |
| --- | --- |
| How the overall AI-native application framework works | `docs/build-any-ai-application.md` |
| The global scope, target AI environment, and universal repository rules | `AGENTS.md` |
| How the business runs its workflows stage by stage | `process/` |
| What goes in the header and body of every governed document | `formats/README.md` and `formats/<format>.md` |
| What procedures an agent can execute | `.agents/skills/README.md` |
| What the deterministic linter enforces | `scripts/README.md` and `scripts/check.py` |
| Where interstitial working files and reports are written | `tmp/` |
