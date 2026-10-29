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


def populate(repo: Path) -> None:
    write(
        repo / "system" / "user-roles.md",
        system_header("User Roles", "system/user-roles")
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
""",
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
        system_header("External Systems", "system/external-systems")
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
        system_header("Application Backlog", "system/application-backlog")
        + """# APP-0001
## Title
Hold an example
## Status
Proposed
## Opened
2026-10-22
## Request
Keep this for later.
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
""",
    )
    write(
        repo / "clients" / "acme" / "client.md",
        client_header("Acme", "clients/client", 3) + CLIENT_BODY,
    )
    write(
        repo / "clients" / "acme" / "open-issues.md",
        client_header("Acme — Open Issues", "clients/open-issues", 3)
        + """# Open
None

# Closed
| # | Opened | Closed | Area | Issue | Resolution |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-22 | 2026-10-22 | Client | Website was missing. | Written to client.md and decision 1. |
""",
    )
    write(
        repo / "clients" / "acme" / "decision-log.md",
        client_header("Acme — Decision Log", "clients/decision-log", 1)
        + """# Decisions
| # | Date | Area | Decision | Source |
| --- | --- | --- | --- | --- |
| 1 | 2026-10-22 | Client | Website remains unknown. | open-issues #1 |
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
            client_header("Acme — Decision Log", "clients/decision-log", 1) + "# Decisions\nNone\n",
        )
        result = run_check(self.repo)
        self.assertIn("closed issue 1", result.stdout)

    def test_backlog_dependency_cycle_fails(self) -> None:
        populate(self.repo)
        write(
            self.repo / "system" / "application-backlog.md",
            system_header("Application Backlog", "system/application-backlog")
            + """# APP-0001
## Title
First
## Status
Proposed
## Opened
2026-10-22
## Request
First request.
## Refined Requirement
None
## Acceptance Criteria
None
## Plan
None
## Dependencies
- APP-0002
## Resolution
None

# APP-0002
## Title
Second
## Status
Proposed
## Opened
2026-10-22
## Request
Second request.
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
""",
        )
        result = run_check(self.repo)
        self.assertIn("cycle", result.stdout)

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
        path.write_text("# Process: sample-workflow (version 1)\n\n`create-application`\n", encoding="utf-8")
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
        write(order, client_header("Acme — Order Form", "clients/order-form", 1) + ORDER_BODY)
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
            client_header("Acme — Order Form", "clients/order-form", 1) + ORDER_BODY.replace("## Status\nDraft", "## Status\nSigned"),
        )
        self.assertIn("required once status is Signed", run_check(self.repo).stdout)

    def test_order_form_area_is_known(self) -> None:
        populate(self.repo)
        path = self.repo / "clients" / "acme" / "open-issues.md"
        path.write_text(path.read_text(encoding="utf-8").replace("| Client |", "| Order Form |"), encoding="utf-8")
        result = run_check(self.repo)
        self.assertNotIn("is not a known area", result.stdout)

    def test_entitlements_area_is_rejected(self) -> None:
        populate(self.repo)
        path = self.repo / "clients" / "acme" / "open-issues.md"
        path.write_text(path.read_text(encoding="utf-8").replace("| Client |", "| Entitlements |"), encoding="utf-8")
        result = run_check(self.repo)
        self.assertIn("is not a known area", result.stdout)


if __name__ == "__main__":
    unittest.main()
