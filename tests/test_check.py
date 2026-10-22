#!/usr/bin/env python3
"""Regression tests for scripts/check.py against temporary repository copies."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
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

# Entitlements
## Order Form
None
## Plan Name
None
## Starts
None
## Renews
None
## Deliverables
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
- application-lifecycle
## Skills
- setup-application
## Status
Active
""",
    )
    write(
        repo / "system" / "users.md",
        system_header("Users", "system/users")
        + f"""# {OPERATOR}
## Name
Example Operator
## Primary Role
operator
## Status
Active
## Notes
None
""",
    )
    write(
        repo / "system" / "client-assignments.md",
        system_header("Client Assignments", "system/client-assignments")
        + f"""# A-0001
## User
{OPERATOR}
## Role
operator
## Client
acme
## Status
Active
## Started
2026-10-22
## Ended
None
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
        client_header("Acme", "clients/client", 2) + CLIENT_BODY,
    )
    write(
        repo / "clients" / "acme" / "open-issues.md",
        client_header("Acme — Open Issues", "clients/open-issues", 2)
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
        path.write_text(path.read_text(encoding="utf-8").replace("format_version: 1\n", "format_version: 1\nclient: acme\n"), encoding="utf-8")
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
        path = self.repo / "process" / "client-lifecycle.md"
        path.write_text(path.read_text(encoding="utf-8").replace("`setup-client`", "`create-application`"), encoding="utf-8")
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

    def test_handoff_requires_decision_chapter(self) -> None:
        handoff = Path(self.temp.name) / "handoff.md"
        write(handoff, client_header("Acme — Handoff", "clients/handoff", 2) + "# Client\nNone\n")
        result = run_check(self.repo, "--handoff", str(handoff))
        self.assertIn("Decision Log", result.stdout)

    def test_valid_handoff_passes(self) -> None:
        shifted = ["#" + line if line.startswith("#") else line for line in CLIENT_BODY.splitlines()]
        handoff = Path(self.temp.name) / "handoff.md"
        write(
            handoff,
            client_header("Acme — Handoff", "clients/handoff", 2)
            + "# Client\n"
            + "\n".join(shifted)
            + "\n# Open Issues\n## Open\nNone\n## Closed\nNone\n# Decision Log\n## Decisions\nNone\n",
        )
        result = run_check(self.repo, "--handoff", str(handoff))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
