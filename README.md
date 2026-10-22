# ai-native-app

The base factory repository for building and running any AI-native application. People and agents read and write the same structured Markdown documents under explicit contracts—global context (`AGENTS.md`), stage-by-stage business processes (`process/`), document schemas (`formats/system/` and `formats/clients/`), shared application data (`system/`), procedural skills (`.agents/skills/`), and deterministic verification scripts (`scripts/`).

Read [`docs/build-any-ai-application.md`](docs/build-any-ai-application.md) for the complete blueprint behind this repository.

## Layout

```text
AGENTS.md            the Global Context and repository contract (read first)
docs/                general repository documentation, including build-any-ai-application.md; README.md is the inventory
process/             domain workflows added for this business; shipped skills carry their own stage rules; README.md is the inventory
formats/             format contracts split into system/ and clients/; README.md holds shared conventions and the inventory
system/              application-wide shared records (users, roles, assignments, external systems, backlog, question journal)
clients/<slug>/      one isolated folder per client or entity
archive/             retired client folders and catalog items (nothing is ever deleted)
.agents/skills/      the procedural skills; README.md is the inventory
.claude/skills/      symlinks exposing .agents/skills/ as /<skill> slash commands in Claude Code
scripts/             check.py (the deterministic lint) and setup-scripts.py; README.md is the inventory
tmp/                 git-ignored working folder for interstitial agent files, proposals, and reports
```

## Starting points

- Configure this repository, or set it up from scratch when required files are missing: `/setup-application`
- Onboard a client or entity from a handoff file: `/setup-client <path-to-handoff.md>`
- Add, edit, or retire a user and their client assignments: `/update-user`
- Connect one user's external-system accounts: `/setup-my-integrations`
- Teach a user the system and their role: `/train-me`
- Save a later application change: `/add-to-backlog`
- Refine one backlog item and hand it to process improvement: `/process-backlog`
- Resolve a client's open issues into the decision log: `/review-open-issues <client-slug>`
- Turn journaled operator questions into process or prompting changes: `/review-question-journal`
- Propose, implement, and independently review a mechanism change: `/improve-process "<what needs to change>"`
- Upgrade this repository to the current template paradigm: `/upgrade-app`
- Configure or check skill links for the chosen AI environment (`claude`, `openai`, `gemini`): `python3 scripts/setup-scripts.py [--env claude|openai|gemini] [--check]`
- Lint the entire repository before committing: `python3 scripts/check.py`

## Where things are defined

| Question | Answer lives in |
| --- | --- |
| How the overall AI-native application framework works | `docs/build-any-ai-application.md` |
| The global scope, target AI environment, and universal repository rules | `AGENTS.md` |
| How the business runs its workflows stage by stage | `process/` |
| What goes in the header and body of every governed document | `formats/README.md` and the namespaced contract under `formats/system/` or `formats/clients/` |
| Which people, roles, assignments, external systems, and backlog items are shared | `system/` |
| What procedures an agent can execute | `.agents/skills/README.md` |
| What the deterministic linter enforces | `scripts/README.md` and `scripts/check.py` |
| Where interstitial working files and reports are written | `tmp/` |
| Where a template upgrade plan is written | `docs/upgrades/` |
