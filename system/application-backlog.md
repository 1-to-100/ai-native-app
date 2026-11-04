---
title: Application Backlog
format: system/application-backlog
format_version: 3
created: 2026-10-22
created_by: springer@1to100.com
updated: 2026-11-04
updated_by: springer@1to100.com
---

# APP-0001
## Title
Move application data storage to a Google shared drive

## Status
Proposed

## Opened
2026-11-03

## Request
### Statement
Move over system and client storage from Github in the repository into a Google Drive folder. The work here would include setting up a standard shared drive (https://knowledge.workspace.google.com/admin/drive/set-up-shared-drives-for-your-organization) in Google drive for the application, having that drive contain a standard set of folders specific to the app, and then storing all the application data there. The idea is that this allows users to view all the content directly in Google docs and edit it through Google docs in addition to through the edits in the application directly. Introduces an integration dependency and setup per user for Google Drive which we are happy to have.

### Problem and Trigger
All application data (`system/`, `clients/`, `archive/`) lives only as Markdown in the GitHub repository. People who do not use Git or a code editor cannot view it or edit it in Google Docs. Raised by the operator on 2026-11-03. It affects every user of the application, especially sales and customer-success roles.

### Desired Outcome
Someone not in the conversation can check each of these:
1. A Google shared drive exists for the application with `system/`, `clients/` and `archive/` folders at its root, and `system/external-systems.md` holds an `Active` `google-drive` record (category `Files`) whose `## Link` is that drive.
2. Every system record, client document, archived item and inventory (`system/`, `clients/`, `archive/`) is a native Google Doc in the matching folder. Each Doc has a last tab named "Document Control" holding a two-column Key/Value table of its metadata.
3. A person's edit in Google Docs is seen by an agent on its next read.
4. An agent's edit appears in Google Docs.
5. Every skill that writes a governed Drive document ends by re-reading it and applying the format check from its format's `## Checks`. `check.py` lints only the repository's own files, and nothing is exported.
6. `setup-application` verifies that the drive, its standard folders, and the `external-systems` link exist. `setup-my-integrations` verifies that each user's own connector can open the drive's root and that the user has edit rights.

### In Scope
- A one-time setup: a Google Workspace admin creates the shared drive. `setup-application` creates the standard folders through the connector, verifies them, and records the `google-drive` system with its link in `system/external-systems.md`. `formats/system/external-systems.md` gains a `## Link` section (version 2), and `check.py` requires a link on an `Active` Google Drive record.
- Drive becomes the only store for `system/` data, `clients/<slug>/` folders, `archive/<slug>/` items, and the inventories `system/README.md`, `clients/README.md` and `archive/README.md`. These are native Google Docs, and the agents keep the inventories current.
- Agents reach Drive through each user's own Google Drive connector. `setup-my-integrations` walks each user through it. There is no local sync folder.
- Each document's metadata moves into a last tab named "Document Control" holding a Key/Value table (`title`, `format`, `format_version`, `created`, `created_by`, `updated`, `updated_by`, plus `client` for client documents). The body sits in the first tab. `formats/README.md` and every format's Header section describe this, with a version bump on every format.
- `updated` and `updated_by` stay required. They are set from Drive's last-modified date and last-modifying user's email whenever an agent touches or reconciles a document.
- Agents apply a basic format check after every write, and repair minor structural variances from human edits on the next write, telling the operator what changed.
- Before each write the agent re-reads the document and, if its revision changed, re-reads and redoes the edit.
- Drive version history and trash are the audit trail. Agents never trash or overwrite a record without reading it first. Retiring a client moves its folder to `archive/<slug>/`.
- `check.py` and its tests are narrowed. Its checks of `system/`, `clients/`, `archive/` and the cross-record checks are removed. `--staged` applies only to files still in Git.

### Out of Scope
- Per-client Drive permissions (`APP-0002`).
- A Git mirror or two-way sync with the repository.
- Drive for desktop or local sync.
- Sheets or Slides as record forms.
- Automated shared-drive creation.
- Any provider other than Google Drive.
- Moving `process/`, `formats/`, skills, scripts, `docs/` or any `AGENTS.md` out of Git.

### Mechanisms and Records Affected
- **Global context and docs:** root `AGENTS.md`, `system/AGENTS.md`, `clients/AGENTS.md` (both stay in Git with updated rules), `README.md`, and `docs/build-any-ai-application.md` (its Git and Markdown storage sections).
- **Formats:** `formats/README.md` and every format in `formats/system/` and `formats/clients/` (Document Control tab, version bump), plus `external-systems` version 2 with `## Link`.
- **Scripts:** `scripts/check.py` and its tests are narrowed as above. `scripts/README.md` is updated.
- **Skills:** `setup-application`, `setup-my-integrations`, `setup-client`, `update-user`, `add-to-backlog`, `process-backlog`, `improve-process`, `review-open-issues`, `review-question-journal`, `train-me` and `upgrade-app`, plus `.agents/skills/README.md`. The skills that write governed documents gain the format-check step. Skills that commit keep committing only mechanism changes in Git.
- **Records:** a new `google-drive` record in `system/external-systems.md`, and the existing system records move to Drive.
- **Migration:** users, external systems, backlog and journal are empty and there are no client folders, so only the three roles in `system/user-roles.md` carry content. Each empty record is recreated as a Doc. This row and its siblings are recreated in Drive unchanged when the move happens.

### Constraints
- Drive permissions are not per client, so every shared-drive member can open every client folder. Drive membership is limited to people who may see all clients' data and is managed manually by a Workspace admin. "Never reference another client" stays a rule on agent behavior, and `## Assigned Clients` stays routing metadata and does not control Drive access.
- No credential, API key or token is stored anywhere. The shared drive link is not a secret.
- The "never delete" rules still apply to people, roles, backlog rows, journal rows and client folders. The app cannot stop a person from deleting a Doc in Drive. This is recorded as a limitation, and the admin steps advise that only managers can delete.
- Header, `None`, Display Name and heading-level rules stay the same. Only where the metadata is held changes.
- `created_by` and `updated_by` always hold a human's email address.

### Why Held
It waits until the operator prioritizes it, and it is cheaper the earlier it lands because no data exists yet. It becomes urgent when the first client is onboarded with `setup-client` or the first non-developer needs to edit application data.

### Open Points
- Whether the Google Docs connector can create, name, order and read a "Document Control" last tab. A test document created and read back through the connector would answer this.
- How agents write headings, tables and bullets into native Docs with the format's structure intact (conversion on upload versus batch updates). A test document written both ways and read back would answer this.

## Refined Requirement
None

## Acceptance Criteria
None

## Plan
None

## Dependencies
None

## Resolution
None

# APP-0002
## Title
Enforce per-client Drive folder permissions

## Status
Proposed

## Opened
2026-11-03

## Request
### Statement
We can not enforce this for now as, invariably, the permissions will get a lot out of synch. Add that requirement as a future backlog item. ("This" is the question of whether Drive permissions should enforce that a user only sees the clients in their `## Assigned Clients`.)

### Problem and Trigger
Under `APP-0001`, Drive permissions are not per client, so every shared-drive member can open every client folder. This was raised on 2026-11-03 when the operator declined to enforce per-client access because permissions would drift out of step with assignments. It affects any user who should see only some clients.

### Desired Outcome
Each `clients/<slug>/` folder is restricted to users whose `## Assigned Clients` include the slug, plus drive managers. Someone can check this by listing a client folder's permissions and comparing them to the assignments.

### In Scope
- Restricted, non-inheriting per-client folders.
- `update-user`, `setup-client` and the retire step keeping access in line with assignments.
- A drift report comparing folder permissions to `## Assigned Clients`.

### Out of Scope
- Per-document permissions.
- Shared-drive membership management.
- The `system/` folder.

### Mechanisms and Records Affected
`update-user`, `setup-client`, `setup-my-integrations`, the `google-drive` record in `system/external-systems.md`, and `AGENTS.md`.

### Constraints
`## Assigned Clients` stays routing metadata, and no client fact enters `system/`.

### Why Held
Permissions drift out of sync with assignments. It becomes urgent when people who must not see all clients, such as outside collaborators, need access to the drive.

### Open Points
- How to keep Drive permissions in step with `## Assigned Clients` without drift. A design of the sync or drift-check mechanism would answer this.

## Refined Requirement
None

## Acceptance Criteria
None

## Plan
None

## Dependencies
- APP-0001

## Resolution
None
