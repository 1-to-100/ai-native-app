#!/usr/bin/env python3
"""Regression tests for scripts/check.py against temporary repository copies."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts" / "check.py"
OPERATOR = "operator@example.com"


def run_check(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(CHECK), "--root", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def copy_repo(destination: Path) -> None:
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(".git", "tmp", ".claude", "__pycache__", "*.pyc", ".DS_Store"),
        dirs_exist_ok=False,
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def system_header(title: str, format_id: str, version: int = 1) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        f"format: {format_id}\n"
        f"format_version: {version}\n"
        "created: 2026-10-22\n"
        f"created_by: {OPERATOR}\n"
        "updated: 2026-10-22\n"
        f"updated_by: {OPERATOR}\n"
        "---\n\n"
    )


def client_header(title: str, format_id: str, version: int) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        f"format: {format_id}\n"
        f"format_version: {version}\n"
        "client: acme\n"
        "created: 2026-10-22\n"
        f"created_by: {OPERATOR}\n"
        "updated: 2026-10-22\n"
        f"updated_by: {OPERATOR}\n"
        "---\n\n"
    )


CLIENT_BODY = """# General Information
## Name
Acme
## Organization
None
## Website
None
## Time Zone
America/New_York
## Engagement Started
2026-10-22
## Contact
- Name: Ada
- Email: ada@example.com

# Business Overview
None

# Business Problem
None

# Solution
None

# Notes
None
"""


PRODUCT_BODY = """# Managed Onboarding
## Overview
Guided onboarding for new customers.
## Specification
Vendor provides guided onboarding. Weekly check-ins included.
## Pricing Model
Per Unit
## Pricing Unit
per month
## List Price
1500.00 USD
## Frequency
Monthly
## Status
Active
"""

ORDER_BODY = """# Order Details
## Order Number
OF-0001
## Status
Draft
## Plan Name
Standard
## Order Date
2026-10-22
## Effective Date
None
## Term End
None
## Renewal
Auto-Renew

# Parties
## Customer Legal Name
Acme Corporation
## Customer Signatory
- Name: Ada
- Email: ada@example.com
## Sales Representative
None

# Line Items
| Product or Service | Specification | Quantity | Unit | Unit Price | Frequency |
| --- | --- | --- | --- | --- | --- |
| Managed Onboarding | Vendor provides guided onboarding. Weekly check-ins included. | 1 | per month | 1500.00 | Monthly |

# Commercial Terms
## Currency
USD
## Billing Contact
None
## Payment Terms
Net 30
## Discounts and Adjustments
None

# Execution
## Signed Date
None
## Signed Copy
None

# Notes
None
"""


BACKLOG_REQUEST = """### Statement
Keep this for later.
### Problem and Trigger
Something is missing.
### Desired Outcome
It works and can be checked.
### In Scope
The example change.
### Out of Scope
None
### Mechanisms and Records Affected
One skill.
### Constraints
None
### Why Held
None
### Open Points
None
"""


def backlog_row(heading: str, status: str, request: str = BACKLOG_REQUEST, dependencies: str = "None") -> str:
    later = "None" if status == "Proposed" else "Something concrete."
    return (
        f"# {heading}\n## Title\nExample\n## Status\n{status}\n## Opened\n2026-10-22\n"
        f"## Request\n{request}## Refined Requirement\n{later}\n## Acceptance Criteria\n{later}\n"
        f"## Plan\n{later}\n## Dependencies\n{dependencies}\n## Resolution\nNone\n"
    )


def backlog_file(*rows: str) -> str:
    return system_header("Application Backlog", "system/application-backlog", 3) + "\n".join(rows)


def stage(number: int, name: str, owner: str, skills: str = "`setup-client`") -> str:
    return (
        f"### Stage {number}: {name}\n#### Entry Criteria\nThe client folder exists.\n"
        f"#### Owner\n{owner}\n#### Description\nDo the work.\n#### Graduation Criteria\ncheck.py passes.\n"
        f"#### Branching and Terminal Paths\nDone: the run completes.\n#### Implementing Skills\n{skills}\n"
    )


def process(name: str, stages: str, supervisor: str = "operator") -> str:
    return (
        f"# {name}\n## Purpose\nQualify work.\n## Scope\nFrom lead to order.\n## Supervisor Role\n{supervisor}\n"
        "## Cadence\nOn demand.\n## System of Record\n### Mode\nRepository Markdown\n### Location\n"
        "`clients/<slug>/open-items.md`\n## Inputs\n- client.md\n## Stages\n"
        f"{stages}## Outputs\n- order-form.md\n## Rules\n- None invented.\n## Related\n- `clients/open-items`\n"
    )


LIFECYCLE = (
    "# Lifecycle Stage: sales (version 1)\n\n"
    + process(
        "Lead Qualification",
        stage(1, "Qualify", "- operator") + stage(2, "Confirm", "Automation: On-Demand"),
    )
    + "\n"
    + process("Order Preparation", stage(1, "Draft", "- operator\n- reviewer"))
)

OPEN_ITEMS = """# In Flight
| # | Opened | Process | Stage | Responsible | Updated | Status Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 2026-10-22 | Lead Qualification | Stage 1: Qualify | operator | 2026-10-22 | Started. |
| 3 | 2026-10-22 | Lead Qualification | Stage 2: Confirm | Automation | 2026-10-22 | Queued. |
| 4 | 2026-10-22 | Order Preparation | Stage 1: Draft | operator@example.com | 2026-10-22 | Drafting. |

# Completed
| # | Opened | Completed | Process | Outcome | Status Notes |
| --- | --- | --- | --- | --- | --- |
| 5 | 2026-10-01 | 2026-10-20 | Order Preparation | Done | Signed. |

# Open
None

# Closed
| # | Opened | Closed | Area | Issue | Resolution |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-22 | 2026-10-22 | Client | Website was missing. | Written to client.md and decision 1. |
"""


def populate(repo: Path) -> None:
    write(
        repo / "system" / "user-roles.md",
        system_header("User Roles", "system/user-roles", 2)
        + """# operator
## Display Name
Operator
## Purpose
Runs the application.
## Core Tasks
Configure shared records.
## Processes
None
## Skills
- setup-application
## Status
Active

# reviewer
## Display Name
Reviewer
## Purpose
Backs up the operator.
## Core Tasks
Review drafts.
## Processes
None
## Skills
None
## Status
Active
""",
    )
    write(repo / "process" / "sales.md", LIFECYCLE)
    process_readme = repo / "process" / "README.md"
    process_readme.write_text(
        process_readme.read_text(encoding="utf-8").replace(
            "| None | — | — | — | — |",
            "| [`sales.md`](sales.md) | Lead Qualification | operator | On demand | Repository Markdown |",
        ),
        encoding="utf-8",
    )
    write(
        repo / "system" / "users.md",
        system_header("Users", "system/users", 2)
        + f"""# {OPERATOR}
## Name
Example Operator
## Primary Role
operator
## Assigned Clients
- acme
## Status
Active
## Notes
None
""",
    )
    write(
        repo / "system" / "external-systems.md",
        system_header("External Systems", "system/external-systems", 2)
        + f"""# jira
## Display Name
Jira
## Category
Work Management
## Status
Active
## Purpose
Track work the operator named.
## Coordination Guidance
Keep decisions in the repository.
## Data Mapping
None
## System Administration
The operator completed the shared installation.
## User Connection
The user approves the connection in the agent environment.
## Owner
{OPERATOR}
""",
    )
    write(
        repo / "system" / "application-backlog.md",
        backlog_file(backlog_row("APP-0001", "Proposed")),
    )
    write(
        repo / "clients" / "acme" / "client.md",
        client_header("Acme", "clients/client", 4) + CLIENT_BODY,
    )
    write(
        repo / "clients" / "acme" / "open-items.md",
        client_header("Acme — Open Items", "clients/open-items", 4) + OPEN_ITEMS,
    )
    write(
        repo / "clients" / "acme" / "decision-log.md",
        client_header("Acme — Decision Log", "clients/decision-log", 2)
        + """# Decisions
| # | Date | Area | Decision | Source |
| --- | --- | --- | --- | --- |
| 1 | 2026-10-22 | Client | Website remains unknown. | open-items #1 |
""",
    )
    readme = repo / "clients" / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("`None`", "`acme`"), encoding="utf-8")


class CheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        copy_repo(self.repo)
        subprocess.run(["git", "init"], cwd=self.repo, check=True, capture_output=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_real_repository_passes(self) -> None:
        result = subprocess.run(["python3", str(CHECK)], text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_nested_format_is_discovered(self) -> None:
        write(self.repo / "formats" / "system" / "extra.md", "# Format: wrong (version 1)\n")
        result = run_check(self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("formats/system/extra.md", result.stdout)
        self.assertIn("system/extra.md", result.stdout)

    def test_external_format_is_discovered_and_inventoried(self) -> None:
        write(self.repo / "formats" / "external" / "design-page.md", "# Format: external/design-page (version 1)\n")
        result = run_check(self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("formats/external/design-page.md", result.stdout)
        self.assertIn("external/design-page.md", result.stdout)

    def test_external_system_requires_data_mapping(self) -> None:
        path = self.repo / "system" / "external-systems.md"
        record = (
            "# jira\n## Display Name\nJira\n## Category\nWork Management\n## Status\nPlanned\n"
            "## Purpose\nTrack work.\n## Coordination Guidance\nNone\n## System Administration\nNone\n"
            "## User Connection\nNone\n## Owner\nNone\n"
        )
        path.write_text(path.read_text(encoding="utf-8").replace("\nNone\n", "\n" + record, 1), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("Data Mapping", result.stdout)

    def test_system_header_rejects_client_key(self) -> None:
        path = self.repo / "system" / "users.md"
        path.write_text(path.read_text(encoding="utf-8").replace("format_version: 2\n", "format_version: 2\nclient: acme\n"), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("header keys must be", result.stdout)

    def test_populated_records_and_client_decision_pass(self) -> None:
        populate(self.repo)
        result = run_check(self.repo)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_unknown_role_reference_fails(self) -> None:
        populate(self.repo)
        path = self.repo / "system" / "users.md"
        path.write_text(path.read_text(encoding="utf-8").replace("operator\n", "missing-role\n", 1), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("unknown role", result.stdout)

    def test_unknown_assigned_client_fails(self) -> None:
        populate(self.repo)
        path = self.repo / "system" / "users.md"
        path.write_text(path.read_text(encoding="utf-8").replace("- acme\n", "- missing-client\n", 1), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("does not exist", result.stdout)

    def test_retired_user_with_assigned_clients_fails(self) -> None:
        populate(self.repo)
        path = self.repo / "system" / "users.md"
        path.write_text(path.read_text(encoding="utf-8").replace("## Status\nActive", "## Status\nRetired", 1), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("Retired user must have Assigned Clients of None", result.stdout)

    def test_closed_issue_requires_decision(self) -> None:
        populate(self.repo)
        write(
            self.repo / "clients" / "acme" / "decision-log.md",
            client_header("Acme — Decision Log", "clients/decision-log", 2) + "# Decisions\nNone\n",
        )
        result = run_check(self.repo)
        self.assertIn("closed issue 1", result.stdout)

    def test_backlog_dependency_cycle_fails(self) -> None:
        populate(self.repo)
        write(
            self.repo / "system" / "application-backlog.md",
            backlog_file(
                backlog_row("APP-0001", "Proposed", dependencies="- APP-0002"),
                backlog_row("APP-0002", "Proposed", dependencies="- APP-0001"),
            ),
        )
        result = run_check(self.repo)
        self.assertIn("cycle", result.stdout)

    def test_backlog_request_missing_subsection_fails(self) -> None:
        populate(self.repo)
        request = BACKLOG_REQUEST.replace("### Constraints\nNone\n", "")
        write(self.repo / "system" / "application-backlog.md", backlog_file(backlog_row("APP-0001", "Proposed", request)))
        result = run_check(self.repo)
        self.assertIn("## Request", result.stdout)
        self.assertNotEqual(result.returncode, 0)

    def test_backlog_required_request_subsection_cannot_be_none(self) -> None:
        populate(self.repo)
        request = BACKLOG_REQUEST.replace("### Desired Outcome\nIt works and can be checked.\n", "### Desired Outcome\nNone\n")
        write(self.repo / "system" / "application-backlog.md", backlog_file(backlog_row("APP-0001", "Proposed", request)))
        result = run_check(self.repo)
        self.assertIn("### Desired Outcome: required and cannot be None", result.stdout)

    def test_backlog_ready_item_with_open_points_fails(self) -> None:
        populate(self.repo)
        request = BACKLOG_REQUEST.replace("### Open Points\nNone\n", "### Open Points\n- Who owns it?\n")
        write(self.repo / "system" / "application-backlog.md", backlog_file(backlog_row("APP-0001", "Ready", request)))
        result = run_check(self.repo)
        self.assertIn("### Open Points: must be None once status is Ready", result.stdout)

    def test_stale_inventory_link_fails(self) -> None:
        readme = self.repo / "formats" / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8") + "\n| [`missing.md`](missing.md) | Nothing | System header | repository |\n",
            encoding="utf-8",
        )
        result = run_check(self.repo)
        self.assertIn("missing.md", result.stdout)
        self.assertIn("not on disk", result.stdout)

    def test_renamed_skill_reference_fails(self) -> None:
        path = self.repo / "process" / "sample-workflow.md"
        path.write_text("# Lifecycle Stage: sample-workflow (version 1)\n\n`create-application`\n", encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("create-application", result.stdout)

    def test_flat_format_path_fails(self) -> None:
        path = self.repo / "process" / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nSee formats/client.md.\n", encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("stale flat format path", result.stdout)

    def test_staged_attribution_fails(self) -> None:
        populate(self.repo)
        git = ["git", "-c", "user.email=operator@example.com", "-c", "user.name=Operator"]
        subprocess.run([*git, "init"], cwd=self.repo, check=True, capture_output=True)
        subprocess.run([*git, "add", "."], cwd=self.repo, check=True, capture_output=True)
        subprocess.run([*git, "commit", "-m", "initial"], cwd=self.repo, check=True, capture_output=True)
        target = self.repo / "system" / "users.md"
        target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        subprocess.run([*git, "add", "system/users.md"], cwd=self.repo, check=True, capture_output=True)
        result = run_check(self.repo, "--staged")
        self.assertIn("updated/updated_by did not change", result.stdout)

    def test_removed_handoff_flag_is_not_special(self) -> None:
        populate(self.repo)
        result = run_check(self.repo, "--handoff", "x.md")
        self.assertNotIn("handoff", result.stdout.lower())

    def test_entitlements_section_is_rejected(self) -> None:
        populate(self.repo)
        path = self.repo / "clients" / "acme" / "client.md"
        path.write_text(path.read_text(encoding="utf-8").replace("# Notes", "# Entitlements\nNone\n\n# Notes"), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("# sections must be", result.stdout)

    def test_catalog_is_optional_and_validated(self) -> None:
        populate(self.repo)
        write(self.repo / "system" / "products-and-services.md", system_header("Products and Services", "system/products-and-services") + PRODUCT_BODY)
        readme = self.repo / "system" / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("| [`users.md`]", "| [`products-and-services.md`](products-and-services.md) | `system/products-and-services` | Catalog. |\n| [`users.md`]"), encoding="utf-8")
        self.assertEqual(run_check(self.repo).returncode, 0)
        path = self.repo / "system" / "products-and-services.md"
        path.write_text(path.read_text(encoding="utf-8").replace("Monthly", "Fortnightly"), encoding="utf-8")
        self.assertIn("is not in its vocabulary", run_check(self.repo).stdout)

    def test_order_form_passes_and_resolves_catalog(self) -> None:
        populate(self.repo)
        write(self.repo / "system" / "products-and-services.md", system_header("Products and Services", "system/products-and-services") + PRODUCT_BODY)
        readme = self.repo / "system" / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("| [`users.md`]", "| [`products-and-services.md`](products-and-services.md) | `system/products-and-services` | Catalog. |\n| [`users.md`]"), encoding="utf-8")
        order = self.repo / "clients" / "acme" / "order-form.md"
        write(order, client_header("Acme — Order Form", "clients/order-form", 2) + ORDER_BODY)
        result = run_check(self.repo)
        self.assertEqual(result.returncode, 0, result.stdout)
        order.write_text(order.read_text(encoding="utf-8").replace("Weekly check-ins included.", "Changed words."), encoding="utf-8")
        self.assertIn("Specification differs from the catalog", run_check(self.repo).stdout)
        order.write_text(order.read_text(encoding="utf-8").replace("Managed Onboarding |", "Unknown Thing |"), encoding="utf-8")
        self.assertIn("is not in system/products-and-services.md", run_check(self.repo).stdout)

    def test_signed_order_requires_signed_date(self) -> None:
        populate(self.repo)
        write(
            self.repo / "clients" / "acme" / "order-form.md",
            client_header("Acme — Order Form", "clients/order-form", 2) + ORDER_BODY.replace("## Status\nDraft", "## Status\nSigned"),
        )
        self.assertIn("required once status is Signed", run_check(self.repo).stdout)

    def test_order_form_area_is_known(self) -> None:
        populate(self.repo)
        path = self.repo / "clients" / "acme" / "open-items.md"
        path.write_text(path.read_text(encoding="utf-8").replace("| Client |", "| Order Form |"), encoding="utf-8")
        result = run_check(self.repo)
        self.assertNotIn("is not a known area", result.stdout)

    def test_entitlements_area_is_rejected(self) -> None:
        populate(self.repo)
        path = self.repo / "clients" / "acme" / "open-items.md"
        path.write_text(path.read_text(encoding="utf-8").replace("| Client |", "| Entitlements |"), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("is not a known area", result.stdout)

    def _edit(self, relative: str, old: str, new: str) -> str:
        path = self.repo / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        return run_check(self.repo).stdout

    def test_old_process_title_fails(self) -> None:
        populate(self.repo)
        out = self._edit("process/sales.md", "# Lifecycle Stage: sales (version 1)", "# Process: sales (version 1)")
        self.assertIn("first line must be '# Lifecycle Stage: sales (version N)'", out)

    def test_duplicate_process_name_fails(self) -> None:
        populate(self.repo)
        write(self.repo / "process" / "delivery.md", "# Lifecycle Stage: delivery (version 1)\n\n" + process("Lead Qualification", stage(1, "Deliver", "- operator")))
        readme = self.repo / "process" / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "| [`delivery.md`](delivery.md) | Lead Qualification | operator | Weekly | Repository Markdown |\n", encoding="utf-8")
        self.assertIn("duplicate process name", run_check(self.repo).stdout)

    def test_unknown_owner_role_fails(self) -> None:
        populate(self.repo)
        out = self._edit("process/sales.md", "#### Owner\n- operator\n- reviewer", "#### Owner\n- operator\n- nobody")
        self.assertIn("#### Owner: unknown role 'nobody'", out)

    def test_unknown_supervisor_role_fails(self) -> None:
        populate(self.repo)
        out = self._edit("process/sales.md", "## Supervisor Role\noperator", "## Supervisor Role\nnobody")
        self.assertIn("## Supervisor Role: unknown role 'nobody'", out)

    def test_automation_stage_cannot_be_manual(self) -> None:
        populate(self.repo)
        out = self._edit("process/sales.md", "Automation: On-Demand\n#### Description\nDo the work.\n#### Graduation Criteria\ncheck.py passes.\n#### Branching and Terminal Paths\nDone: the run completes.\n#### Implementing Skills\n`setup-client`", "Automation: On-Demand\n#### Description\nDo the work.\n#### Graduation Criteria\ncheck.py passes.\n#### Branching and Terminal Paths\nDone: the run completes.\n#### Implementing Skills\nManual (Gap)")
        self.assertIn("an Automation stage must name a skill, not Manual (Gap)", out)

    def test_bad_automation_line_fails(self) -> None:
        populate(self.repo)
        out = self._edit("process/sales.md", "Automation: On-Demand", "Automation: Whenever")
        self.assertIn("#### Owner: must be a bullet list of role slugs", out)

    def test_recurring_automation_passes(self) -> None:
        populate(self.repo)
        out = self._edit("process/sales.md", "Automation: On-Demand", "Automation: Recurring (every Monday 09:00 America/New_York)")
        self.assertIn("0 error(s)", out)

    def test_role_process_reference_uses_process_name(self) -> None:
        populate(self.repo)
        out = self._edit("system/user-roles.md", "## Processes\nNone\n## Skills\n- setup-application", "## Processes\n- Lead Qualification\n## Skills\n- setup-application")
        self.assertIn("0 error(s)", out)
        out = self._edit("system/user-roles.md", "- Lead Qualification", "- sales")
        self.assertIn("unknown reference 'sales'", out)

    def test_in_flight_unknown_stage_fails(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/open-items.md", "Stage 1: Qualify", "Stage 9: Qualify")
        self.assertIn("unknown stage 'Stage 9: Qualify'", out)

    def test_in_flight_unknown_process_fails(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/open-items.md", "| Lead Qualification | Stage 1", "| Lead Scoring | Stage 1")
        self.assertIn("unknown process 'Lead Scoring'", out)

    def test_in_flight_responsible_must_be_owning_role(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/open-items.md", "| Stage 1: Qualify | operator |", "| Stage 1: Qualify | reviewer |")
        self.assertIn("Responsible 'reviewer' is not the owning role", out)

    def test_in_flight_responsible_email_must_be_user(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/open-items.md", "| operator@example.com |", "| ghost@example.com |")
        self.assertIn("Responsible 'ghost@example.com' is not in system/users.md", out)

    def test_in_flight_automation_only_on_automation_stage(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/open-items.md", "| Stage 1: Qualify | operator |", "| Stage 1: Qualify | Automation |")
        self.assertIn("is Automation but 'Stage 1: Qualify' is role-owned", out)

    def test_open_items_id_space_is_shared(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/open-items.md", "| 5 | 2026-10-01 |", "| 1 | 2026-10-01 |")
        self.assertIn("# '1' is duplicate across the file", out)

    def test_decision_citing_in_flight_item_fails(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/decision-log.md", "open-items #1", "open-items #2")
        self.assertIn("cites issue 2, which is not closed", out)

    def test_stale_open_issues_reference_fails(self) -> None:
        populate(self.repo)
        out = self._edit("clients/acme/decision-log.md", "open-items #1", "open-issues #1")
        self.assertIn("stale open-issues reference", out)
        self.assertNotIn("review-open-issues", "".join(line for line in out.splitlines() if "stale" in line))


if __name__ == "__main__":
    unittest.main()
