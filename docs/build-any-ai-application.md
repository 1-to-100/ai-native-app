# Build Any AI Application

## 1. Overview

Every founder feels the pressure to put AI to work in their business. Most of them are failing at it because they are choosing between two broken approaches. The first mistake is running your business by hand out of a chat window: pasting context into Claude, ChatGPT, or Gemini, tweaking prompts on the fly, getting a passable answer, and watching the entire workflow vanish the moment you close the tab. You're an idiot if you run a company by hand, and prompting in a chat box is just that. The second mistake is hiring an engineering team to build bespoke custom software before you even know what your process is. That choice buys you six months of burn and a brittle application that breaks the first time your workflow changes. What is missing is a repeatable factory pattern that lets a founder with focus and determination turn a business process into a durable AI application without writing traditional software.

This document gives you the production line for building any AI-native application directly inside a repository of structured Markdown files, governed by explicit contracts and enforced by deterministic Python or TypeScript scripts. Instead of building a bespoke database and custom screens by hand, you store your global context, business processes, document formats, client records, and agent skills in a Git repository. Modern coding agents already know how to read, write, search, and version-control a repository. When you give those agents a strict contract, they run the stations on your line while you set the intent and approve the output.

Deploying this approach follows a strict sequence. First, you pick one AI environment - Claude, OpenAI, or Gemini - and optimize your entire repository for it.  (We can give you a long justification on why we don't recommend spening time on vendor neutrality.  Interestingly, this comes later.)  Second, you run the `create-application` skill in this repository. That skill interviews you, writes your global context in the root `AGENTS.md` file, maps your workflows into stage-by-stage process documents in `process/`, defines the data contracts in `formats/`, wires up your folder-level agent rules and operational skills, and generates the verification script in `scripts/check.py`. Third, you run your business through those skills and watching where you have to step in and edit by hand. Every time you catch yourself fixing the same mistake twice, you feed that observation into `improve-process`, which upgrades your processes, formats, skills, and scripts in one coordinated pass.

---

## 2. Philosophy

Anyone can build an AI-native application and run a company on it. You do not need a computer science degree, a technical background, or a venture check. The only requirements are focus and determination; everything else is irrelevant. What separates a toy prompt from a real business system is whether you run a disciplined factory line or improvise by hand. Eleven rules govern the line.

### 2.1. Pick an AI and Optimize for It

Founders love to talk about staying "vendor-neutral" so they can swap Claude for ChatGPT or Gemini next quarter. That's will waste your time at an early stage.   When you choose vendor neutrality, you choose the lowest common denominator: you give up native slash commands, artifact rendering, project memory, subagent orchestration, and workspace integrations just to preserve a theoretical migration you will probably never run. The simplification and speed you get from going all-in on one vendor's environment wildly outweighs the benefit of staying neutral. Pick one AI, commit to its native tools, and let your application will be FAR more impactful FAR sooner.

### 2.2. People: Set Intent, Supply Original Thought, and Approve Results

The model will alwasy provide the first draft and the structure. You are the intent, the original thought, and the final decision. Left to itself, an AI converges on average ideas and safe, repetitive prose. It is great at beating the blank page, sketching options, organizing outlines, checking rules against a style guide, and producing well-defined derivative work. It cannot supply your lived experience, your business judgment, or a point of view you actually stand behind.

Because people remain accountable for what ships, an agent is never an actor in the record. Every governed document in the repository carries the human operator's email address in `created_by` and `updated_by`—never an agent name like `claude` or `codex`. And an agent never approves its own gates. Approval is an explicit human act written into the repository, and silence never counts as a yes.

### 2.3. The Repository Holds the Record

If a decision only exists in a chat thread, a Slack message, or a meeting transcript, it does not exist. Every stage of work must end in a durable, formatted document saved in the repository. Chat sessions are temporary working memory. Slide decks, shared previews, and exported PDFs are derived views. A person or a fresh agent session with zero memory of the conversation that produced a file must be able to pick up the work from the repository artifact alone.

### 2.4. Grounding Over Invention

Left alone, an LLM will happily invent a metric, a customer quote, or a contract term just to make a template look finished. In a business application, hallucination is poison. The rule on our line is absolute: never invent a fact, a reason to believe, a signature phrase, a client reaction, or a commercial term. Every claim requires a source. When a source is silent or two sources disagree, the agent writes `None` in the field and opens a tracked row in `open-issues.md` naming who must supply the answer and what the next step is.

### 2.5. History Is Append-Only; Nothing Is Deleted

You never delete a client folder, a catalog item, a past plan, a built deliverable, or a recorded decision. If a client leaves or a catalog type is retired, you move it to `archive/`. Before you rewrite a rolling plan, you copy the current one unchanged to `prior-plans/<YYYY-MM-DD>.md`. If you reverse a decision in a client's `decision-log.md`, you add a new dated row explaining the reversal; you never delete or rewrite the old row. If a planned deliverable is dropped, its status becomes `cancelled`. Your repository is your institutional memory, and you do not shred the ledger.

### 2.6. A Stage Is Governed by a Process Document, and Every Stage Is Small Enough to Hand Off

You do not ask an agent to "run marketing" or "manage onboarding" in one giant prompt. Every workflow is broken down in a governing process document under `process/` into discrete stages—the same way we break a software product into atomic features mapped to detailed personas and clear outcomes. Each stage declares its entry criteria, what happens inside the stage, its graduation criteria, and where the path branches. And each stage is sized so a fresh agent can read the inputs, execute the skill for that stage, stop at a real stopping point, and hand off a clean artifact to the next station on the line.

### 2.7. One Agent Does the Work, One Checks It

An agent that checks its own work inside the same conversation that wrote it will repeat the exact same blind spots that caused the mistake. So the agent that writes an artifact never grades it.

Instead, a second agent in a clean context inspects the finished artifact against the process and format contracts without seeing the messy drafting chat. The checker never fixes the file itself; it returns findings so the writer fixes them and the checker reviews again.

### 2.8. Improving the Process Is Part of the Job

It is your job to automate your job. When an agent makes the same mistake twice, or when you have to manually rewrite the same section every week, you are looking at a defect in your process, your format contract, or your skill. Do not fix it by hand and move on. Your core operating loop as a founder is watching what works and what creates friction, then feeding that observation straight into the `improve-process` skill. That skill traces which mechanisms need to change, proposes the upgrade, and tightens the factory line so you never make that manual edit again.

### 2.9. Autonomy Is Earned by Evidence

Every material decision starts behind a human approval gate. An agent earns autonomy one stage and one kind of change at a time, only after that exact stage has a proven track record of passing verification and human review without correction.

### 2.10. A Workflow Is Done When Its Outcome Is Measured

A workflow is not finished just because an artifact was generated or published. It is finished when it reaches the real world, its outcome is measured, and those results are written back into the repository to drive the next cycle of planning.

### 2.11. Ask the Record Before You Ask the Operator

Every question an agent asks the operator costs attention and is evidence of a gap in the line. So before an agent asks, it checks the record: a subagent reads the client's `decision-log.md` to see whether a decision already made answers the question or gives enough confidence to proceed without one. Only when the record is silent does the agent ask.

Every question that is asked beyond what the skill explicitly requires is written to the question journal in `system/`. A journaled question is never closed by answering it in the session; it is closed by the process or prompting change that makes the question unnecessary. A question that recurs after it was acted on is a defect in that change.

---

## 3. Using Repositories ("What We Get for Free" with Git and GitHub)

AI labs spent billions of dollars training Claude Code, OpenAI Codex, and Gemini to be world-class software engineers. Because of that training, these agents are natively built to navigate directory trees, search across hundreds of files in milliseconds, make surgical edits to text files, and run Git and GitHub commands.

When you build your business application inside a Git repository hosted on GitHub, you are putting the AI on its home turf. You get a rock-solid enterprise control system—cloud backup, complete change history, line-by-line audit trails, permission controls, and automated quality gates—for free. Best of all, you do not have to become a software engineer or memorize Git commands to use it. You tell the agent what to do through your skills, and the agent handles staging, checking, committing, branching, and pushing for you.

### 3.1. The Few Repository Concepts an Operator Needs to Know

While the agent handles the mechanics, you need to understand four concepts so you know what the machine is doing on your behalf:

* **Working Copy vs. GitHub:** Your **working copy** is the folder of files sitting on your computer right now while you and the agent work. **GitHub** is the master vault in the cloud where the official version of the repository lives. When an agent "pulls," it grabs the latest files from GitHub; when it "pushes," it sends your saved work up to the vault.
* **Commits (Save Points with Receipts):** A **commit** is a permanent snapshot of changes across one or more files. Unlike hitting Save in a word processor, every commit carries a receipt: who made the change, the exact timestamp, a short message explaining what changed, and the exact lines added or removed. Paired with our rule that `check.py --staged` verifies `updated` and `updated_by` in every modified file's header, you always know who changed what and when.
* **Branches and Pull Requests (Safe Sandboxes):** A **branch** is a parallel copy of the repository where an agent can make big changes—like running `improve-process` to overhaul a workflow—without touching your live operations on the `main` branch. A **Pull Request (PR)** is the review screen on GitHub that shows you the exact before-and-after diff and lets you approve and merge the changes once they pass every check.
* **Automated Checks (CI and Diff Review):** GitHub can run `python3 scripts/check.py` automatically on every Pull Request, alongside automated diff reviewers like `.cursor/BUGBOT.md`. If an agent or an operator tries to save a file with a missing section, a misspelled vocabulary value, or a broken reference, the check blocks the merge until it is fixed.

---

## 4. Using Markdown as a Storage Medium

### 4.1. Why Markdown

Traditional software forces you to store data in a SQL database that humans cannot read without custom screens, and then write thousands of lines of glue code so humans and AI models can talk to that database. That is bespoke overhead you do not need.

AI models speak Markdown natively. They were trained on billions of Markdown documents, which means they read, reason over, and write Markdown with higher accuracy and lower token cost than bloated JSON payloads or custom database layers. At the same time, Markdown is plain text that any human founder can read and edit in any text editor. When you use Markdown as your storage medium, you and your agents read and write the exact same files.

### 4.2. Turning Markdown into a Structured Database

Unstructured Markdown notes turn into a swamp fast. To make Markdown work like a relational database, every governed document in the repository follows four strict rules enforced by `formats/` and `scripts/check.py`:

#### The Standard Header (YAML Front Matter)

Every governed document opens with a standardized YAML block at the very top of the file—its database ID card:

```yaml
---
title: Acme Corp — Client Profile
format: client
format_version: 1
client: acme-corp
created: 2026-10-20
created_by: founder@company.com
updated: 2026-10-20
updated_by: founder@company.com
---
```

* `title` is the human-readable name of the document.
* `format` names the exact contract in `formats/<format>.md` that governs this file.
* `format_version` is the integer version of that format contract.
* `client` (when inside a client folder) matches the folder's slug.
* `created`, `created_by`, `updated`, and `updated_by` record the dates (`YYYY-MM-DD`) and the human operator's email address. An agent name is never allowed here.
* Only documents that move through a production pipeline (like a built content piece or deliverable) add a `status` key in front matter.

#### Headings as Database Fields

Below the header, Markdown headings (`#`, `##`, `###`) act as strict database columns in a fixed order:
* In a **single-record document** (like `client.md`), `#` headings are top-level sections (`# General Information`, `# Business Overview`, `# Entitlements`) and `##` headings are individual fields (`## Name`, `## Website`).
* In a **multi-record document** (like a topic catalog, a persona list, or a weekly plan), each `#` heading is a record's unique name, and the format's sections shift down one heading level underneath it.
* Short repeated rows use standard Markdown tables with fixed column headers.

#### Explicit Sentinels (`None` and `—`) and Relational References

You never delete a required heading because you do not have the answer yet. An empty section must hold the single word `None`. An empty cell in a Markdown table must hold `—`. That way, both a human and `check.py` know the difference between "we do not have this fact yet" and "the agent forgot to write the section."

Documents link to each other just like foreign keys in a database:
* **Files** are referenced by their slug (the filename without `.md`).
* **Records inside a multi-record file** are referenced by their exact heading text.
* **Controlled vocabularies** are written using the exact Display Name listed in the governing format's `Vocabularies` table.

#### Format Versioning (`format_version`)

Businesses evolve, and your document schemas will evolve with them. Every format file declares its current version number in its title line (`# Format: client (version 1)`). When you use `improve-process` to add a field to a format, the skill bumps `format_version`, updates all active documents of that format to match, and updates `check.py` in the same commit. Frozen historical snapshots (like files in `prior-plans/`) keep the `format_version` they were written under so you never rewrite history.

---

## 5. Mechanisms: Precedence and Order of Creation

### 5.1. How the Mechanisms Fit Together (Precedence and Creation Order)

An AI application in this framework is built from seven interlocking mechanisms. The order in which `create-application` builds them when you start a repository is the exact order of authority when two files disagree:

| Order | Mechanism | Location | Role on the Factory Line | Precedence Rule |
| --- | --- | --- | --- | --- |
| **1** | **Global Context** | Root `AGENTS.md` | Defines what the application is, what is out of scope, the target AI environment, and the rules that apply everywhere. | Governs the entire repository. No nested file, process, or skill may violate it. |
| **2** | **Processes** | `process/*.md` | Defines the business workflows stage by stage: entry criteria, stage work, graduation criteria, branching paths, system of record, and implementing skills. | States business intent. Governs what skills must do, subject to the data structures allowed by Formats. |
| **3** | **Formats** | `formats/*.md` | Defines the exact schema—headers, sections, vocabularies, and rules—for every document type in the repository. | **The format wins over skills and processes** on what a document holds. If a process needs a new field, update the format first. |
| **4** | **Subtree Agents** | `<dir>/AGENTS.md` | Defines local guardrails for agents working inside a specific directory (`process/`, `formats/`, `clients/`, `system/`, `docs/`). | Adds stricter rules for its folder; never relaxes the root `AGENTS.md`. |
| **5** | **Skills** | `<skills-dir>/<name>/SKILL.md` | Defines the step-by-step procedure an agent runs when invoked to execute a stage of a process. | Operates strictly inside `AGENTS.md`, `process/`, and `formats/`. If a skill disagrees with a format, fix the skill. |
| **6** | **Deterministic Scripts** | `scripts/*.py` (or `.ts`) | Enforces format schemas, reference resolution, header attribution, and skill links mechanically. | The automated gatekeeper. No skill run or commit is complete until `check.py` exits with zero errors. |
| **7** | **Client, Catalog & System Data** | `clients/<slug>/`, catalogs, `system/` | Holds the live business records, entity foundation files, plans, decision logs, open issues, produced deliverables, and the repository-wide question journal. | Must conform 100% to `formats/` and pass `scripts/check.py` at all times. |

### 5.2. Global Context (Root `AGENTS.md`)

The root `AGENTS.md` file is the master contract for your application. Every agent session loads it first, and its rules stay in force for every prompt across every folder.

In our framework, the root `AGENTS.md` is governed by `formats/global-context.md` and contains six mandatory sections:
1. **`# Application Overview`** — A blunt, clear statement of what this application does, who operates it, and the business outcomes it produces.
2. **`# Scope and Out of Scope`** — Two explicit subsections (`## In Scope` and `## Out of Scope`) drawing a hard boundary around what belongs in this repository versus what happens upstream, downstream, or in external systems.
3. **`# Target AI Environment`** — Names the single AI vendor environment this repository is optimized for (`Claude`, `OpenAI`, or `Gemini`), how skills are invoked in that environment, and which native capabilities (like Claude Artifacts, Codex terminal workflows, or Gemini workspace tools) the application uses. This choice also fixes the skills directory. This document writes that directory as the placeholder `<skills-dir>/`; the final path is resolved per target AI environment in the table in Section 7.2.
4. **`# Before You Act`** — The mandatory reading sequence every agent follows before touching a file:
   1. Read `process/README.md` and the governing process document in `process/`.
   2. Read `<skills-dir>/README.md` and invoke the matching skill by name rather than improvising.
   3. Read `formats/README.md` and the governing format contract in `formats/` before writing or editing any document.
   4. Read `scripts/README.md` before running verification scripts.
5. **`# Every File`** — Universal data hygiene rules: standard YAML headers, human operator emails in `created_by` and `updated_by`, `None` for empty sections, resolving references, and running `python3 scripts/check.py` before finishing.
6. **`# Never`** — The systemic hard lines no agent or operator may ever cross (never deleting records instead of archiving, never inventing facts or decisions, never storing credentials or payment details, never cross-referencing between isolated client folders).

### 5.3. Process Definitions (`process/` and `formats/process.md`)

Before you design a database table or write an agent prompt, you have to define how the work actually moves through your business. That is what `process/` holds. Every workflow gets its own file in `process/<slug>.md`, governed by the default process format at `formats/process.md` and indexed in `process/README.md`.

Every process document follows a strict, machine-checked structure built around discrete, handoff-sized stages:

* **`# Purpose`** — What the process achieves.
* **`# Scope`** — Where the process's boundaries start and stop.
* **`# Roles`** — Which human roles (e.g., `Operator`, `Client`, `Reviewer`) take part.
* **`# Cadence`** — What triggers the process or how often it runs.
* **`# System of Record`** — Declares where the state of items moving through this process is modeled:
  * **`Repository Markdown`** when items are tracked natively as Markdown files in this repository (naming the directory and governing formats, such as `clients/<slug>/`).
  * **`External System`** when state lives in an external tracker like Jira, Linear, HubSpot, or Salesforce—including the direct URL to that system and how repository artifacts link to external ticket or record IDs.
* **`# Inputs`** — The exact documents, contracts, or external signals required to start.
* **`# Stages`** — The stage-by-stage factory line. Each stage is a `## Stage N: <Stage Name>` section containing five required fields:
  * **`### Entry Criteria`** — What must be true and which files or approvals must exist before work can enter this stage.
  * **`### Description`** — What happens in this stage, who owns it, and what decisions are made.
  * **`### Graduation Criteria`** — The exact proof, `check.py` validation, or human approval required to mark the stage complete and hand off to the next stage.
  * **`### Branching and Terminal Paths`** — Where work goes when it does not move straight to the next stage. Real business processes branch: a deal moves to `Closed Won` or `Closed Lost`; a proposed deliverable is `Approved`, `Rejected`, or `Deferred`; an onboarding check passes or returns to upstream. Every valid branch and terminal state is named here explicitly.
  * **`### Implementing Skills`** — For processes modeled in repository Markdown, names the exact skill (or set of skills) in `<skills-dir>/` that executes this stage, or states `Manual (Gap)` when a person still performs the stage by hand under `AGENTS.md` and the governing format.
* **`# Outputs`** — What exists when the process finishes.
* **`# Rules`** — The defaults and `Never` rules for this workflow.
* **`# Related`** — The linked formats, skills, scripts, and open gaps.

### 5.4. Format Contracts (`formats/`)

A format contract is the schema for one kind of Markdown document. `formats/README.md` holds the shared rules across the entire repository (the standard header, single-record vs. multi-record heading rules, reference rules, and the table of all formats). Each `formats/<name>.md` file governs one document type and contains:
* **`# Purpose`** — Why the document exists.
* **`# Location`** — Where files of this format live.
* **`# Header`** — Any additions to the standard YAML front matter.
* **`# Body`** — A fenced Markdown template showing the exact `#`, `##`, and `###` headings in order, with instructions under each heading explaining what belongs there and how it is formatted.
* **`# Rules`** — Business and structural invariants for that document type.
* **`# Vocabularies`** — Closed tables of allowed Display Names for fields that select from a fixed list.
* **`# Checks`** — The exact rules `scripts/check.py` enforces on every file carrying `format: <name>`.

When a skill and a format disagree, the format wins. When a process asks for data a format cannot hold, you change the format first (bumping `format_version`) or the process yields.

### 5.5. Subtree Agent Files (`<directory>/AGENTS.md`)

While the root `AGENTS.md` sets the global contract, individual directories have local rules that only matter when an agent is working inside that folder. We place a focused `AGENTS.md` file inside `process/`, `formats/`, `clients/`, `system/`, `docs/`, and any shared catalog directory.

For example:
* `formats/AGENTS.md` enforces the atomic migration rule: you never change a format without bumping `format_version`, updating every active document that uses that format, and updating `scripts/check.py` in the same commit.
* `process/AGENTS.md` enforces that processes state business intent without duplicating format schemas or skill procedures, and that client-specific commercial overrides live in `clients/<slug>/client.md`, never in `process/`.
* `clients/AGENTS.md` enforces strict tenant isolation: a client folder may never link to, copy from, or compare against another client folder.
* `system/AGENTS.md` enforces the access boundary: any agent may append to and commit files in `system/`, but an agent executing a client-specific stage never reads from or writes client facts into `system/`.

### 5.6. Skills (`<skills-dir>/<skill-name>/SKILL.md`)

A skill is an invocable, step-by-step procedure that executes a stage (or a bounded step) of a process. Instead of typing a long prompt and hoping the AI remembers your rules, the operator invokes a skill by name (`/create-application`, `/setup-client`, `/improve-process` in Claude Code; `$create-application`, `$setup-client`, `$improve-process` in OpenAI Codex; or `@create-application` in Gemini).

Every skill lives in `<skills-dir>/<skill-name>/SKILL.md`, is registered in `<skills-dir>/README.md`, and opens with YAML front matter (`name` and `description`) followed by seven mandatory sections:
1. **`## When to use`** — The exact trigger and process stage this skill serves.
2. **`## Inputs`** — What the operator must supply (and how the skill prompts if an input is missing—never guessing).
3. **`## Reads`** — The exact process, format, catalog, and data files the skill loads before acting.
4. **`## Procedure`** — Numbered, deterministic steps including explicit human review gates and `check.py` runs.
5. **`## Writes`** — Every repository file (and any interstitial `tmp/` file) the skill creates or updates.
6. **`## Stops when`** — The exact completion bar where the skill halts and reports back to the operator.
7. **`## Never`** — The actions this skill is forbidden to take.

### 5.7. Deterministic Verification Scripts (`scripts/`)

LLMs are probabilistic engines; they are terrible accountants. You never rely on an LLM's promise that it followed a format contract. You enforce the contract with deterministic Python or TypeScript programs in `scripts/`, documented in `scripts/README.md`:

* **`scripts/check.py`** lints every governed Markdown file in the repository against its format contract: YAML front matter keys and types, `format_version` alignment, exact heading hierarchy and section order, closed vocabulary values, cross-file reference integrity, stage structure in `process/`, inventory synchronization, `--handoff <path>` pre-flight validation, and `--staged` commit checks verifying that `updated` and `updated_by` changed on every modified file. It reports `ERROR` and `WARN` lines and never edits a file itself.
* **`scripts/setup-scripts.py`** configures and verifies the repository's skill exposure and native context pointers for the target AI environment (`--env claude`, `--env openai`, `--env gemini`, or `--check`), ensuring every skill in `<skills-dir>/` is wired up and matches `<skills-dir>/README.md`.

### 5.8. Shared Catalogs (Catalogs and Registries)

Processes, formats, skills, and scripts are the machinery of your factory. Shared Catalogs and Client Data are what run through the machinery.

**Shared Catalogs and Registries** (such as a `content-types/` library, a product catalog, or `SERVICES.md`) sit at the repository root and define the menu of reusable building blocks your business offers across all clients.

### 5.9. Client Data (`clients/<slug>/`)

**Client (or Entity) Data** gives each customer, account, or project its own isolated folder under `clients/<slug>/` whose filenames mirror the format contracts in `formats/`:

* `client.md` (and a redacted `order-form.pdf` when commercial terms apply) is the single source of truth for who the client is and what they are entitled to. No other file restates those facts.
* Domain foundation documents (such as personas, topics, style guides, or requirements) hold the grounded context for that client.
* Active operational files (such as `current-plan.md`, `prior-plans/<YYYY-MM-DD>.md`, and produced deliverables) track the work moving through the stages defined in `process/`.
* `open-issues.md` holds every unresolved question or missing fact (`# Open` and `# Closed` tables), linked by `Area` to the exact document where the answer will land once resolved. Closing an issue requires writing the answer into that target document in the same commit.
* `decision-log.md` is the single, central log of every decision made for this client. It replaces any file-specific `# Decisions` section; no other document in the client folder keeps its own decisions table. Rows are append-only, and a reversal is a new dated row. Before an agent asks the operator a question during client work, it has a subagent read `decision-log.md` first: if an existing decision answers the question or gives enough confidence to decide, the agent proceeds on that decision and cites it rather than asking.

### 5.10. System Records (`system/`)

The `system/` directory is reserved for records that belong to the repository as a whole rather than to any one client. Every agent may append to and commit files in `system/`, but the directory is not accessible to an agent doing client-specific work: it never reads from `system/`, and nothing in `system/` may hold a client fact. That boundary is enforced by `system/AGENTS.md`.

Its first record is the **Question Journal** (`system/question-journal.md`). Every question an agent asks the operator beyond the questions a skill's prompt explicitly requires is appended here as a row carrying:

* **Question** — The question exactly as it was asked.
* **Skill** — The skill that was running when the question arose, or `—` when none applied.
* **Process** — The governing process.
* **Stage** — The process stage the agent was in.
* **LLM** — The model that asked the question.
* **Status** — `Open` until a change absorbs it; then `Closed` with a reference to that change.

An entry is never closed by answering the question in the session. It is closed by the process change or prompting change that makes the question unnecessary, applied through `review-question-journal` and `improve-process`. A question that recurs after it was acted on is a defect in that change and reopens the entry.

---

## 6. Starting Skills

Every repository built on this framework starts with four foundational skills in `<skills-dir>/`. Together they bootstrap the application into existence, bring clients or entities onto the line, upgrade the factory as you operate it, and turn the questions agents ask you into factory upgrades.

### 6.1. `create-application` — Bootstrapping the Application into Existence

When you clone this base repository to build a new AI application, `create-application` is the first skill you run. Its job is to take you from a blank template to a working, vendor-optimized AI application with zero hand-wiring.

**How `create-application` works:**
1. **Reads the Blueprint:** Reads this governing document (`docs/build-any-ai-application.md`) and inspects the current repository state.
2. **Locks in the Target AI Environment:** Asks which AI ecosystem you are optimizing for (`Claude`, `OpenAI`, or `Gemini`) and your operator email address.
3. **Interviews for Global Context:** Interviews you in plain language about what your business does, what this application is responsible for, what is out of scope, and the non-negotiable guardrails. It drafts the root `AGENTS.md` file conforming to `formats/global-context.md` and pauses for your approval.
4. **Maps the Core Processes:** Walks you through the core workflows your application needs to run. For each workflow, it helps you break the work into discrete handoff-sized stages—defining Entry Criteria, Stage Description, Graduation Criteria, Branching/Terminal Stages (like `Closed Won` / `Closed Lost` or `Approved` / `Rejected`), the System of Record (Repository Markdown vs. External System like Jira/Linear/HubSpot), and the skills that will run each stage. It writes each process to `process/<slug>.md` under `formats/process.md` and updates `process/README.md`.
5. **Defines the Data Formats and Catalogs:** From the inputs and outputs of your processes, it identifies every document type and shared catalog your application needs, writes their format contracts in `formats/<name>.md`, and updates `formats/README.md`.
6. **Writes Subtree Agents, Skills, and Verification Rules:** Generates or updates the folder-level `AGENTS.md` files, scaffolds the initial operational skills in `<skills-dir>/` (preserving `improve-process` and `review-question-journal`, and customizing `setup-client` to match your new client/entity formats), updates `scripts/check.py` to enforce every new format contract, runs `python3 scripts/setup-scripts.py --env <vendor>`, verifies that `python3 scripts/check.py` passes with zero errors, and writes a bootstrap summary to `tmp/create-application-report.md`.

### 6.2. `improve-process` — Turning Operational Friction into Factory Upgrades

No process survives first contact with reality unchanged. As you run your application, you will spot steps where you have to edit an agent's output by hand, fields you forgot to capture, new branching outcomes, or manual stages ready to be automated. Instead of hacking files ad hoc and breaking your contracts, you run `improve-process`.

**How `improve-process` works:**
1. **Intake and Diagnosis:** Takes your description of what needs to change—whether a bug in how an agent behaved, a new business requirement, or a stage adjustment—and reads the inventories across `AGENTS.md`, `process/README.md`, `formats/README.md`, `<skills-dir>/README.md`, and `scripts/README.md`.
2. **Top-Down Impact Analysis:** Walks down the strict precedence chain (`Global Context` $\rightarrow$ `Process` $\rightarrow$ `Formats` $\rightarrow$ `Subtree Agents` $\rightarrow$ `Skills` $\rightarrow$ `Scripts` $\rightarrow$ `Existing Data Files`) to identify every mechanism touched by the change:
   * Does the global scope or a universal `Never` rule in root `AGENTS.md` change?
   * Which stage, entry/graduation bar, or branch in `process/<slug>.md` changes (requiring a process version bump)?
   * Does a document need a new section, table column, or vocabulary value in `formats/<name>.md` (requiring a `format_version` bump and migration of existing files)?
   * Do any subtree `AGENTS.md` files need tighter rules?
   * Which `SKILL.md` procedures need updated steps, reads, writes, or stopping points?
   * What new checks must be added to `scripts/check.py`?
3. **Structured Proposal Gate:** Writes the full impact analysis to `tmp/improve-process-proposal.md` and presents the proposed changes in chat, file by file, waiting for your explicit approval before touching a single governed file.
4. **Atomic Execution and Verification:** Once you approve, applies the changes in strict dependency order (`Global Context` $\rightarrow$ `Formats` + active file migrations $\rightarrow$ `Process` $\rightarrow$ `Subtree Agents` $\rightarrow$ `Skills` $\rightarrow$ `Scripts` and `README.md` inventories), runs `python3 scripts/setup-scripts.py` and `python3 scripts/check.py`, and stops only when the entire repository is lint-clean.

### 6.3. `setup-client` — Onboarding Clients and Entities Without Invention

Whenever your application manages clients, customers, deals, or projects, you need a single, disciplined gateway for bringing a new entity into the repository. That gateway is `setup-client`. There is never a second, informal backdoor for creating client folders by hand.

**How `setup-client` works:**
1. **Pre-Flight Validation:** Takes a path to an upstream `handoff.md` file (and any required commercial contract like `order-form.pdf`) and runs `python3 scripts/check.py --handoff <path>` before writing anything to `clients/`. If the handoff is malformed, it stops and returns the exact errors.
2. **Mechanical Scaffolding and Setup Ledger:** Creates `clients/<slug>/`, splits the handoff chapters into their format-governed documents (`client.md`, `open-issues.md`, `decision-log.md`, and any domain files your application defines) with standard YAML headers stamped with your operator email, and opens a running **Setup Ledger**. Every section written as `None`, every placeholder value, every conflict between the handoff text and the commercial order form, and every `check.py` warning is added to the Setup Ledger with its `Area`, `Evidence`, and a `Recommended Approach`—never a guessed fact.
3. **Interactive Ledger Walk:** Walks the Setup Ledger with you in chat, one entry at a time. When you accept a recommendation or supply an answer, the skill writes it into the target document and closes the issue in `open-issues.md`. When you defer an item (because only the client can answer it), the skill ensures an open row exists in `open-issues.md` with a concrete `Next Step`.
4. **Verification and Report:** Runs `python3 scripts/check.py <slug>` after every write, saves the complete ledger record to `tmp/setup-report-<slug>.md` (uncommitted), and stops with a lint-clean client folder ready for commit.

### 6.4. `review-question-journal` — Turning Questions into Fewer Questions

Every row in `system/question-journal.md` is a moment where the line stopped and waited for you. `review-question-journal` works through those rows so the same stop does not happen twice. It runs at the repository level, never inside a client folder.

**How `review-question-journal` works:**
1. **Reads the Journal:** Loads every `Open` entry in `system/question-journal.md` along with the skill, process, and process stage each entry names.
2. **Reviews Each Entry:** For each question, an agent asks why the process could not answer it on its own and proposes one of two remedies:
   * **Process change** — The question exposed a gap in the fixed inputs the process already holds: a missing field, vocabulary value, stage, or branch. The remedy is a change to the process, format, or script so the information is in the record before the stage begins.
   * **Prompting change** — The question exposed an ambiguity in the specification the operator supplied. The remedy is a change to how the skill prompts the operator upfront, so the information is collected at the start of the process rather than mid-stage. This is a change to the way specification documents are authored, not to the data the process holds.
3. **Proposal Gate:** Writes the per-entry analysis and proposed remedy to `tmp/review-question-journal-proposal.md`, presents it in chat, and waits for your explicit approval before anything is changed.
4. **Hands Off to `improve-process`:** For each approved remedy, invokes `improve-process` to apply the change atomically across the affected process, format, skill, and script files.
5. **Closes by Change, Never by Answer:** Marks each absorbed entry `Closed` with a reference to the change that absorbed it. An entry is never closed because the question was answered in a session. If a closed question is asked again later, the new row cites the earlier entry, and the recurrence is treated as a defect in the change that was supposed to absorb it.

---

## 7. Repository Layout

### 7.1. Canonical Directory Map

Every repository built from this base template uses the same top-level layout so both people and agents always know where every rule, process, schema, skill, script, and record lives:

```text
AGENTS.md                   Global Context: application scope, target AI environment, and universal rules
README.md                   Operator quick-start guide, starting skill commands, and repository map
.gitignore                  Excludes OS noise and all files inside tmp/ (keeping tmp/.gitkeep)
docs/                       General repository documentation not covered elsewhere
  README.md                 Inventory of docs/
  AGENTS.md                 Rules for docs/
  build-any-ai-application.md  This master governing blueprint
process/                    Stage-by-stage business process definitions
  README.md                 Inventory of processes and shared role vocabulary
  AGENTS.md                 Rules for writing and versioning process documents
  application-lifecycle.md  Default process governing bootstrap, client setup, and process improvement
formats/                    Format contracts (schemas) for every governed Markdown document
  README.md                 Shared header, body, reference, and naming conventions + format inventory
  AGENTS.md                 Rules for changing formats and bumping format_version atomically
  global-context.md         Format contract for the root AGENTS.md file
  process.md                Format contract for stage-by-stage process documents in process/
  client.md                 Format contract for client/entity profile documents
  open-issues.md            Format contract for per-client open and closed issue ledgers
  decision-log.md           Format contract for the per-client central decision log
  question-journal.md       Format contract for the repository-wide question journal in system/
  handoff.md                Format contract for incoming onboarding handoff files
clients/                    One isolated subfolder per client or entity (clients/<slug>/)
  README.md                 How client folders are structured and operated
  AGENTS.md                 Tenant isolation and client-folder rules
system/                     Repository-wide records any agent may append to; not accessible during client-specific work
  README.md                 Inventory of system records
  AGENTS.md                 Access boundary and append-only rules for system/
  question-journal.md       Every question asked of the operator beyond what a skill requires, and the change that absorbed it
archive/                    Retired client folders and retired catalog items (nothing is ever deleted)
  README.md                 Rules and inventory for archived records
<skills-dir>/               Home for all procedural agent skills (path set by # Target AI Environment; see 7.2)
  README.md                 Inventory of all skills (inputs, reads, writes, stopping points)
  create-application/       Skill: bootstrap and customize this repository for a new AI application
  improve-process/          Skill: analyze friction or change requests and upgrade mechanisms atomically
  setup-client/             Skill: onboard a client/entity from a handoff file and walk the Setup Ledger
  review-question-journal/  Skill: review journaled questions and propose process or prompting changes that absorb them
scripts/                    Deterministic verification and environment setup programs
  README.md                 Inventory of scripts and when to run them
  check.py                  Format, process, header, reference, handoff, and staged-diff linter
  setup-scripts.py          Configures and checks skill exposure for Claude, OpenAI, or Gemini
tmp/                        Git-ignored working directory for interstitial agent files, drafts, and reports
  .gitkeep                  Keeps the empty tmp/ directory present in every clone
```

* **`docs/`** holds general documentation for the repository that does not belong inside a specific process, format, or client folder. In every default repository, `docs/build-any-ai-application.md` lives here so `create-application`, `improve-process`, and human operators always have the governing factory blueprint inside the checkout.
* **`tmp/`** sits off the root of the repository with all files inside it ignored by Git (`tmp/*` in `.gitignore`, preserving only `tmp/.gitkeep`). Agents use `tmp/` to store interstitial working files—setup reports (`tmp/setup-report-<slug>.md`), change proposals (`tmp/improve-process-proposal.md`, `tmp/review-question-journal-proposal.md`), bootstrap summaries (`tmp/create-application-report.md`), and slide deck sources—so working scratchpads never pollute the permanent record or get committed by accident.

### 7.2. Vendor-Optimized Configurations

When `create-application` runs `python3 scripts/setup-scripts.py --env <vendor>`, the repository tailors its skill and context wiring to the chosen AI environment. The `<skills-dir>/` placeholder used throughout this document resolves to the **Skill Discovery Location** for the row matching the `# Target AI Environment` in the root `AGENTS.md`:

| Target AI Environment | Root Context File | Skill Discovery Location (`<skills-dir>/`) | How Operator Invokes a Skill | Native Environment Optimizations |
| --- | --- | --- | --- | --- |
| **Claude** (`claude`) | `AGENTS.md` (read natively by Claude Code) | `.claude/skills/<name>` symlinked to `../../.agents/skills/<name>` | `/<skill-name>` (e.g., `/create-application`) | Uses Claude Artifacts for interactive review decks and client approval drafts; uses subagents for isolated research and fresh-context review. |
| **OpenAI** (`openai`) | `AGENTS.md` (read natively by Codex) | `.agents/skills/<name>/SKILL.md` (native location) | `$<skill-name>` or `@<skill-name>` (e.g., `$create-application`) | Uses Codex terminal execution and sandboxed worktrees for automated verification loops. |
| **Gemini** (`gemini`) | `AGENTS.md` plus `GEMINI.md` symlinked to `AGENTS.md` | `.agents/skills/<name>/SKILL.md` and `.gemini/skills/<name>` symlinks | `@<skill-name>` or `/<skill-name>` | Pairs `GEMINI.md` context loading with Gemini CLI commands and Google Workspace handoff flows. |

### 7.3. The Inventory and Subtree Contract Rule

Every major directory in the repository (`docs/`, `process/`, `formats/`, `clients/`, `system/`, `<skills-dir>/`, `scripts/`) follows a strict two-file pairing rule:
1. **`README.md` is the inventory.** It lists every file or skill in that directory in a structured table, explaining when to use it and what it governs. Whenever a skill or operator adds, renames, or retires a file in that folder, the folder's `README.md` must be updated in the same commit, and `scripts/check.py` verifies that the inventory and the disk agree.
2. **`AGENTS.md` is the local contract.** It states the rules an agent must follow when creating or editing files inside that directory.

That is the entire line. Pick your AI environment, run `create-application` to build your stations, bring your work in through `setup-client`, run `improve-process` every time you see friction, and run `review-question-journal` every time an agent had to stop and ask you something. Stop building by hand.
