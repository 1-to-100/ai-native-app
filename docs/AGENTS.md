# AGENTS.md — docs/

This directory holds general documentation for the repository that is not a process (`process/`), a format contract (`formats/`), a skill (`.agents/skills/`), or client data (`clients/`).

- `docs/build-any-ai-application.md` is the master governing document for this framework. Both `create-application` and `improve-process` consult it as the authoritative blueprint for repository structure, mechanism precedence, and creation order.
- Do not place operational workflows here; workflows belong in `process/` under `formats/process.md`.
- Do not place document schemas here; schemas belong in `formats/`.
- Do not place interstitial working files, reports, or drafts here; working files belong in `tmp/`.
- Whenever a document is added, renamed, or moved to `archive/`, update `docs/README.md` in the same commit and run `python3 scripts/check.py`.
