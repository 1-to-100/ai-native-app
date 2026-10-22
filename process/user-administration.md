# Process: user-administration (version 1)

# Purpose
Governs how people are added, edited, and retired, how each person is assigned a role for a client, how one person connects the external systems already configured for the application, and how that person learns the system.

# Scope
Covers `system/users.md`, `system/user-roles.md`, and `system/client-assignments.md`, plus a user's own connections to systems listed in `system/external-systems.md`. Shared installation of an external system belongs to `application-lifecycle` Stage 1. This process does not grant repository permissions and does not store secrets.

# Roles
- Operator: Answers the user, assignment, connection, and training interview, and approves each write.
- Agent: Executes `update-user`, `setup-my-integrations`, and `train-me`.

# Cadence
- Stage 1 runs when a person, primary role, or client assignment needs to be added, edited, or retired.
- Stage 2 runs when one user needs to connect the external systems in their own agent environment.
- Stage 3 runs when a user asks to be taught the application, or when an operator asks to train a named user.

# System of Record
## Mode
Repository Markdown

## Location
`system/users.md` (`system/users`), `system/user-roles.md` (`system/user-roles`), `system/client-assignments.md` (`system/client-assignments`), and `system/external-systems.md` (`system/external-systems`). Training session notes stay in `tmp/`.

# Inputs
- Operator email address.
- For Stage 1, the person's name, email, primary role, and any client assignments the operator wants to record.
- For Stage 2, the user email and access to that user's agent environment.
- For Stage 3, the user email. The skill reads that user's primary role and client assignments.

# Stages
## Stage 1: Maintain Users
### Entry Criteria
The operator invokes `update-user` and can name the person to add, edit, or retire. Role headings used in the change already exist in `system/user-roles.md`, or the operator is prepared to add the role in the same session.

### Description
The Agent interviews for the person's name, email, primary role, and client assignments. It adds or edits the user row and coordinates `system/client-assignments.md`: new assignments are new `A-NNNN` rows, and a retirement or role change ends the affected `Active` rows instead of deleting them.

### Graduation Criteria
The user row matches the operator's answers, every affected assignment is `Active` or `Ended` consistently with that answer, and `python3 scripts/check.py` passes with zero errors.

### Branching and Terminal Paths
- **Recorded:** The user and assignments match the interview and the stage ends.
- **Role Missing:** The named role is not in `system/user-roles.md`. The Agent interviews for the role's purpose, tasks, processes, and skills, writes the role, and then continues the user change.
- **Cancelled:** The operator stops before approval. No partial user or assignment write is left in place.

### Implementing Skills
`update-user`

## Stage 2: Connect User Integrations
### Entry Criteria
`system/external-systems.md` lists the systems the user should connect, shared `## System Administration` for each `Active` system is complete enough to follow, and the operator invokes `setup-my-integrations` for one user email.

### Description
The Agent walks that user through the `## User Connection` guidance for each applicable system inside the user's agent environment. It records which connections the user completed, skipped, or blocked, without writing a secret into the repository.

### Graduation Criteria
`tmp/setup-my-integrations-<user>.md` lists every applicable system and the non-secret outcome of its connection step. No credential was written to the repository.

### Branching and Terminal Paths
- **Connected:** The user finished the connection steps they chose to finish.
- **Skipped:** The user skips a system. The report says so, and the system record is unchanged.
- **Blocked:** A system still needs shared administration. The stage sends that system back to `setup-application` and does not invent a connection.
- **No Systems:** `system/external-systems.md` is `None` or has no `Active` system. The stage stops after saying there is nothing to connect.

### Implementing Skills
`setup-my-integrations`

## Stage 3: Train User
### Entry Criteria
The user exists in `system/users.md`, and the operator invokes `train-me` for that user's email. Stage 1 has recorded the primary role. Client assignments may be `None`.

### Description
The Agent teaches the user the application scope, the role or roles recorded for them, the concepts in the format contracts, the processes, and the operating rules those contracts depend on. The user acknowledges each topic or asks to stop.

### Graduation Criteria
The user has acknowledged every required topic or has stopped at a named topic. `tmp/train-me-<user>.md` records the topics covered and the acknowledgements. No governed file is changed unless the user discovered a defect, which is handed to `question-review` or `backlog-management`.

### Branching and Terminal Paths
- **Completed:** Every required topic was acknowledged.
- **Stopped:** The user stops early. The report names the last completed topic.
- **Unknown User:** The email is not in `system/users.md`. The stage stops and points the operator to Stage 1.

### Implementing Skills
`train-me`

# Outputs
- Updated user, role, and assignment rows.
- A non-secret integration report in `tmp/` after Stage 2.
- A training acknowledgement report in `tmp/` after Stage 3.

# Rules
- Never delete a user, role, or assignment row.
- Never store a credential or permission token in `system/` or `tmp/`.
- Never describe a role as a permission grant.
- Never invent a person's name, role, or client assignment. Ask the operator.

# Related
- Formats: `system/users`, `system/user-roles`, `system/client-assignments`, `system/external-systems`.
- Skills: `update-user`, `setup-my-integrations`, `train-me`.
- Processes: `application-lifecycle`, `client-lifecycle`.
- Gaps: None.
