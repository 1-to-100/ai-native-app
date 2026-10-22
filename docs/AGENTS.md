# AGENTS.md — docs/

This directory holds general documentation for the repository that is not a process (`process/`), a format contract (`formats/`), a skill (`.agents/skills/`), or client data (`clients/`).

- `docs/build-any-ai-application.md` is the master governing document for this framework. Both `setup-application` and `improve-process` consult it as the authoritative blueprint for repository structure, mechanism precedence, and creation order.
- `docs/upgrades/` is where `upgrade-app` writes a step-by-step upgrade plan. That plan stays untracked until an operator explicitly adds it. Interstitial upgrade scratch still belongs in `tmp/`.
- Do not place operational workflows here; workflows belong in `process/` under `formats/system/process.md`.
- Do not place document schemas here; schemas belong in `formats/`.
- Do not place interstitial working files, reports, or drafts here; working files belong in `tmp/`.
- Git ignores every file under `docs/` except `README.md`, `AGENTS.md`, and `build-any-ai-application.md`. A new document enters the repository only when an operator explicitly adds it. In that same commit, add its inventory row to `docs/README.md` and run `python3 scripts/check.py`.
