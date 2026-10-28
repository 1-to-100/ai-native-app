# System — inventory

Repository-wide records that are shared across the application live here. Client business facts stay in `clients/<slug>/`. The rules for this directory live in `system/AGENTS.md`.

| Record | Format | Holds |
| --- | --- | --- |
| [`users.md`](users.md) | `system/users` | People who use the application, by email, and each person's primary role. |
| [`user-roles.md`](user-roles.md) | `system/user-roles` | Operational roles, the processes and skills each role uses, and the tasks that role takes on. |
| [`client-assignments.md`](client-assignments.md) | `system/client-assignments` | Which user acts as which role for which client. |
| [`external-systems.md`](external-systems.md) | `system/external-systems` | External systems agents coordinate with, plus shared setup and per-user connection guidance. |
| [`application-backlog.md`](application-backlog.md) | `system/application-backlog` | Application changes and enhancements to implement later. |
| [`question-journal.md`](question-journal.md) | `system/question-journal` | Operator questions that a skill did not already require, and the change that absorbed each one. |

`products-and-services.md` (format `system/products-and-services`) is an optional record: the catalog of products and services the organization can sell. It is created through `setup-application` and, once present, gains a row in the table above.

## Adding a record

Add a format contract under `formats/system/` first, then add the data file here and a row in the table above in the same change. Update `scripts/check.py` so the new file is required and validated. Run `python3 scripts/check.py`.
