# Docs — inventory

General documentation for this repository that does not belong to a single process, format contract, skill, or client folder. Every agent and operator reads `docs/build-any-ai-application.md` when configuring the application with `setup-application` or evolving its mechanisms with `improve-process`.

| Document | Purpose |
| --- | --- |
| [`build-any-ai-application.md`](build-any-ai-application.md) | The master governing blueprint for building and operating any AI-native application in this repository: philosophy, using Git repositories and Markdown, the seven mechanisms and their precedence/creation order, starting skills (`setup-application`, `improve-process`, `setup-client`), and repository layout. |

## Adding a document

Place general architecture, reference, or framework documentation here only when it is not a business process (`process/`), a document schema (`formats/`), a skill (`.agents/skills/`), or client data (`clients/`). A new file under `docs/` is gitignored. It enters this repository only when an operator explicitly adds it, updates this inventory in the same commit, and `python3 scripts/check.py` passes.
