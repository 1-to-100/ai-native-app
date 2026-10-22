# Format: system/global-context (version 2)

## Purpose

Defines the structure of the root `AGENTS.md` file, which sets the global business and technical context for the entire application. Every agent session loads the root `AGENTS.md` first and respects its rules across every directory in the repository.

## Location

`AGENTS.md` at the repository root.

## Header

No YAML front matter. The first line is `# AGENTS.md — global context (version N)`, where `N` matches the version in this format's title line.

## Body

```markdown
# Application Overview
What this application is, who operates it, what business problem it solves, and what outputs it produces. Written in direct, plain prose so every agent session understands the mission of the repository immediately.

# Scope and Out of Scope
## In Scope
A bullet list of the workflows, decisions, data records, and deliverables governed inside this repository.

## Out of Scope
A bullet list of upstream, downstream, or external activities that do not belong in this repository, plus what is explicitly forbidden from being modeled here.

# Target AI Environment
## Vendor
The single AI environment this repository is optimized for, written as a Display Name from Vendors (`Claude`, `OpenAI`, or `Gemini`).

## Skill Invocation
How the operator invokes skills in the chosen environment (for example, `/<skill-name>` in Claude Code, `$<skill-name>` in OpenAI Codex, `@<skill-name>` in Gemini) and how `scripts/setup-scripts.py` wires them.

## Native Capabilities
How this application uses the chosen vendor's native features (such as Claude Artifacts, subagents, Codex terminal sandboxes, or Gemini Workspace integrations).

# Before You Act
A numbered list giving the exact reading order an agent must follow before executing work (`process/README.md`, then `.agents/skills/README.md`, then `formats/README.md`, then the nearest subtree `AGENTS.md`, then `scripts/README.md`, and `docs/build-any-ai-application.md` when bootstrapping or evolving the system).

# Every File
A bullet list of universal file, header, attribution, sentinel (`None`), reference, `tmp/`, and format-precedence rules that apply to every file in the repository. It distinguishes system records under `system/` from client records under `clients/<slug>/`.

# Never
A flat bullet list of systemic invariants that no agent or operator may ever violate (no deleting records, no rewriting history tables, no inventing facts, quotes, or terms, no storing secrets or payment details, no cross-client comparisons, and no client business facts in `system/`).
```

## Rules

- There is exactly one root `AGENTS.md` file in the repository.
- When `setup-application` interviews the operator, it writes or completes this file before creating or updating processes, formats, skills, or scripts.
- Nested `<directory>/AGENTS.md` files may add stricter rules for their directory. They never relax or contradict the root `AGENTS.md`.
- The version in the root file's first line changes only when this format's version changes.

## Vocabularies

Vendors:

| Display Name | Environment Slug | Description |
| --- | --- | --- |
| Claude | `claude` | Anthropic Claude Code and Claude Desktop environment, using `.claude/skills/` symlinks and Claude Artifacts. |
| OpenAI | `openai` | OpenAI ChatGPT and Codex environment, reading `.agents/skills/` and `AGENTS.md` natively. |
| Gemini | `gemini` | Google Gemini CLI and Workspace environment, using `GEMINI.md` and `.gemini/skills/` symlinks. |

## Checks

- First line matches `# AGENTS.md — global context (version N)`, where `N` is this format's version.
- All six `#` sections (`# Application Overview`, `# Scope and Out of Scope`, `# Target AI Environment`, `# Before You Act`, `# Every File`, `# Never`) are present in exact order.
- `# Scope and Out of Scope` contains `## In Scope` and `## Out of Scope`.
- `# Target AI Environment` contains `## Vendor`, `## Skill Invocation`, and `## Native Capabilities`, and `## Vendor` is a valid Display Name from Vendors.
