#!/usr/bin/env python3
"""Lint every governed Markdown document, process, format, and inventory in the repository.

Usage:
  python3 scripts/check.py                  # whole repository
  python3 scripts/check.py <client-slug>    # one client folder
  python3 scripts/check.py --staged         # require updated/updated_by changes on staged data docs
  python3 scripts/check.py --root <path>    # lint another checkout (used by tests)

Reports findings as ERROR or WARN; never edits a file. Exit code 1 on any ERROR.
"""
from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
PROCESS_DIR = ROOT / "process"
FORMATS_DIR = ROOT / "formats"
CLIENTS_DIR = ROOT / "clients"
ARCHIVE_DIR = ROOT / "archive"
SYSTEM_DIR = ROOT / "system"
SKILLS_DIR = ROOT / ".agents" / "skills"
SCRIPTS_DIR = ROOT / "scripts"

VENDORS = {"Claude", "OpenAI", "Gemini"}
SOR_MODES = {"Repository Markdown", "External System"}
ISSUE_AREAS = {"Client", "Order Form", "Access", "Process"}
USER_STATUSES = {"Active", "Retired"}
ROLE_STATUSES = {"Active", "Retired"}
SYSTEM_CATEGORIES = {
    "Work Management",
    "CRM",
    "Email",
    "Calendar",
    "Files",
    "Analytics",
    "Identity",
    "Other",
}
EXTERNAL_STATUSES = {"Planned", "Active", "Retired"}
PRICING_MODELS = {"Fixed Fee", "Per Unit", "Tiered", "Usage-Based", "Time and Materials"}
FREQUENCIES = {"Daily", "Weekly", "Monthly", "Quarterly", "Annual", "One Time"}
ITEM_STATUSES = {"Active", "Retired"}
ORDER_STATUSES = {"Draft", "Sent", "Signed", "Cancelled"}
RENEWAL_TERMS = {"Auto-Renew", "Manual Renewal", "Does Not Renew"}
BACKLOG_STATUSES = {"Proposed", "Ready", "In Progress", "Done", "Cancelled"}
AGENT_NAMES = {"claude", "codex", "chatgpt", "gemini", "cursor", "agent", "ai", "bot"}
SKILL_SECTIONS = [
    "When to use",
    "Inputs",
    "Reads",
    "Procedure",
    "Writes",
    "Stops when",
    "Never",
]
FORMAT_H2 = ["Purpose", "Location", "Header", "Body", "Rules", "Vocabularies", "Checks"]
SYSTEM_HEADER = ["title", "format", "format_version", "created", "created_by", "updated", "updated_by"]
CLIENT_HEADER = [
    "title",
    "format",
    "format_version",
    "client",
    "created",
    "created_by",
    "updated",
    "updated_by",
]
SYSTEM_FILES = {
    "users.md": "system/users",
    "user-roles.md": "system/user-roles",
    "external-systems.md": "system/external-systems",
    "application-backlog.md": "system/application-backlog",
    "question-journal.md": "system/question-journal",
}
RESERVED = [
    "AGENTS.md",
    "process/README.md",
    "process/AGENTS.md",
    "formats/README.md",
    "formats/AGENTS.md",
    ".agents/skills/README.md",
    ".agents/skills/AGENTS.md",
    "scripts/README.md",
    "scripts/AGENTS.md",
    "clients/README.md",
    "clients/AGENTS.md",
    "system/README.md",
    "system/AGENTS.md",
]
USER_FIELDS = ["Name", "Primary Role", "Assigned Clients", "Status", "Notes"]
ROLE_FIELDS = ["Display Name", "Purpose", "Core Tasks", "Processes", "Skills", "Status"]
EXTERNAL_FIELDS = [
    "Display Name",
    "Category",
    "Status",
    "Purpose",
    "Coordination Guidance",
    "System Administration",
    "User Connection",
    "Owner",
]
PRODUCT_FIELDS = [
    "Overview",
    "Specification",
    "Pricing Model",
    "Pricing Unit",
    "List Price",
    "Frequency",
    "Status",
]
ORDER_SECTIONS = ["Order Details", "Parties", "Line Items", "Commercial Terms", "Execution", "Notes"]
ORDER_DETAIL_FIELDS = [
    "Order Number",
    "Status",
    "Plan Name",
    "Order Date",
    "Effective Date",
    "Term End",
    "Renewal",
]
ORDER_PARTY_FIELDS = ["Customer Legal Name", "Customer Signatory", "Sales Representative"]
ORDER_TERMS_FIELDS = ["Currency", "Billing Contact", "Payment Terms", "Discounts and Adjustments"]
ORDER_EXECUTION_FIELDS = ["Signed Date", "Signed Copy"]
ORDER_LINE_COLUMNS = ["Product or Service", "Specification", "Quantity", "Unit", "Unit Price", "Frequency"]
BACKLOG_FIELDS = [
    "Title",
    "Status",
    "Opened",
    "Request",
    "Refined Requirement",
    "Acceptance Criteria",
    "Plan",
    "Dependencies",
    "Resolution",
]
BACKLOG_REQUEST_FIELDS = [
    "Statement",
    "Problem and Trigger",
    "Desired Outcome",
    "In Scope",
    "Out of Scope",
    "Mechanisms and Records Affected",
    "Constraints",
    "Why Held",
    "Open Points",
]
BACKLOG_REQUIRED_REQUEST_FIELDS = [
    "Statement",
    "Problem and Trigger",
    "Desired Outcome",
    "In Scope",
    "Mechanisms and Records Affected",
]

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PRICE_RE = re.compile(r"^\d+(?:\.\d+)? [A-Z]{3}$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
NUMBER_RE = re.compile(r"^\d+(?:\.\d+)?$")
CARD_RE = re.compile(r"\b(?:\d[ -]?){13,19}\b")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
STALE_SKILL_RE = re.compile(r"(?<![\w-])create-application(?![\w-])")
STALE_FORMAT_RE = re.compile(
    r"(?<![\w/])formats/(global-context|process|client|open-issues|open-items|decision-log|question-journal)\.md"
)
STALE_ISSUES_RE = re.compile(r"(?<![\w-])open-issues(?:\.md|(?= #\d))")
LIFECYCLE_TITLE_RE = re.compile(r"^# Lifecycle Stage: ([a-z0-9-]+) \(version (\d+)\)$")
STAGE_HEADING_RE = re.compile(r"^Stage (\d+): \S.*$")
AUTOMATION_RE = re.compile(r"^Automation: (?:On-Demand|Recurring \((?P<schedule>.+)\))$")
PROCESS_SECTIONS = [
    "Purpose",
    "Scope",
    "Supervisor Role",
    "Cadence",
    "System of Record",
    "Inputs",
    "Stages",
    "Outputs",
    "Rules",
    "Related",
]
STAGE_SECTIONS = [
    "Entry Criteria",
    "Owner",
    "Description",
    "Graduation Criteria",
    "Branching and Terminal Paths",
    "Implementing Skills",
]
IN_FLIGHT_COLUMNS = ["#", "Opened", "Process", "Stage", "Responsible", "Updated", "Status Notes"]
COMPLETED_COLUMNS = ["#", "Opened", "Completed", "Process", "Outcome", "Status Notes"]
OPEN_COLUMNS = ["#", "Opened", "Area", "Issue", "Next Step"]
CLOSED_COLUMNS = ["#", "Opened", "Closed", "Area", "Issue", "Resolution"]
SECRET_RE = re.compile(
    r"(?i)\b(password|api[_-]?key|secret|access[_-]?token|token)\b\s*[:=]\s*\S+"
)
PEM_RE = re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")
EM_DASH = "\u2014"


def configure(root: Path) -> None:
    global ROOT, DOCS_DIR, PROCESS_DIR, FORMATS_DIR, CLIENTS_DIR, ARCHIVE_DIR, SYSTEM_DIR, SKILLS_DIR, SCRIPTS_DIR
    ROOT = root
    DOCS_DIR = ROOT / "docs"
    PROCESS_DIR = ROOT / "process"
    FORMATS_DIR = ROOT / "formats"
    CLIENTS_DIR = ROOT / "clients"
    ARCHIVE_DIR = ROOT / "archive"
    SYSTEM_DIR = ROOT / "system"
    SKILLS_DIR = ROOT / ".agents" / "skills"
    SCRIPTS_DIR = ROOT / "scripts"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def valid_date(val: str) -> bool:
    if not DATE_RE.match(val):
        return False
    try:
        dt.date.fromisoformat(val)
        return True
    except ValueError:
        return False


def parse_sections(body: str, level: int = 1) -> list[tuple[str, str]]:
    prefix = "#" * level + " "
    sections: list[tuple[str, list[str]]] = []
    in_fence = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith(prefix) and not line.startswith("#" * (level + 1)):
            sections.append((line[len(prefix):].strip(), []))
        elif sections:
            sections[-1][1].append(line)
    return [(heading, "\n".join(lines).strip()) for heading, lines in sections]


def table_targets(text: str) -> set[str]:
    found: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        found.update(re.findall(r"\[[^\]]*\]\(([^)]+)\)", line))
    return found


def bullets(text: str, findings: list[str], where: str) -> list[str] | None:
    if text.strip() == "None":
        return []
    values: list[str] = []
    for line in [ln.strip() for ln in text.splitlines() if ln.strip()]:
        if not line.startswith("- "):
            findings.append(f"ERROR {where}: expected a bullet list or None")
            return None
        values.append(line[2:].strip())
    return values


def has_secret(text: str) -> bool:
    return bool(SECRET_RE.search(text) or PEM_RE.search(text))


def parse_table(val: str, expected_cols: list[str], findings: list[str], where: str) -> list[list[str]] | None:
    if val.strip() == "None":
        return []
    lines = [ln.strip() for ln in val.splitlines() if ln.strip()]
    if len(lines) < 2:
        findings.append(f"ERROR {where}: must be None or a Markdown table")
        return None
    cols = [cell.strip() for cell in lines[0].strip("|").split("|")]
    if cols != expected_cols:
        findings.append(f"ERROR {where}: table columns must be {expected_cols}, got {cols}")
        return None
    rows: list[list[str]] = []
    for row_line in lines[2:]:
        cells = [cell.strip() for cell in row_line.strip("|").split("|")]
        if len(cells) != len(expected_cols):
            findings.append(f"ERROR {where}: malformed row {row_line!r}")
            continue
        rows.append(cells)
    if not rows:
        findings.append(f"ERROR {where}: table has no rows; use None when empty")
    return rows


def records(body: str, findings: list[str], where: str) -> dict[str, list[tuple[str, str]]] | None:
    if body.strip() == "None":
        return {}
    parsed = parse_sections(body, 1)
    if not parsed:
        findings.append(f"ERROR {where}: body must be None or one # record per entry")
        return None
    out: dict[str, list[tuple[str, str]]] = {}
    for heading, content in parsed:
        if heading in out:
            findings.append(f"ERROR {where}: duplicate record {heading!r}")
        out[heading] = parse_sections(content, 2)
    return out


def fields_of(
    subs: list[tuple[str, str]], expected: list[str], findings: list[str], where: str
) -> dict[str, str] | None:
    names = [heading for heading, _ in subs]
    if names != expected:
        findings.append(f"ERROR {where}: ## sections must be {expected}, got {names}")
        return None
    out: dict[str, str] = {}
    for heading, value in subs:
        if not value.strip():
            findings.append(f"ERROR {where} -> ## {heading}: section cannot be empty")
            out[heading] = ""
        else:
            out[heading] = value.strip()
    return out


def load_formats(findings: list[str]) -> dict[str, int]:
    versions: dict[str, int] = {}
    if not FORMATS_DIR.is_dir():
        findings.append("ERROR formats/: directory missing")
        return versions
    for path in sorted(FORMATS_DIR.rglob("*.md")):
        if path.name in {"README.md", "AGENTS.md"}:
            continue
        identifier = path.relative_to(FORMATS_DIR).with_suffix("").as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        title = lines[0].strip() if lines else ""
        match = re.match(r"^# Format: ([a-z0-9/-]+) \(version (\d+)\)$", title)
        if not match or match.group(1) != identifier:
            findings.append(f"ERROR {rel(path)}: first line must be '# Format: {identifier} (version N)'")
            continue
        versions[identifier] = int(match.group(2))
        h2 = [heading for heading, _ in parse_sections("\n".join(lines[1:]), 2)]
        for required in FORMAT_H2:
            if required not in h2:
                findings.append(f"ERROR {rel(path)}: missing '## {required}' section")
    return versions


def check_global_context(versions: dict[str, int], findings: list[str]) -> int:
    path = ROOT / "AGENTS.md"
    if not path.is_file():
        findings.append("ERROR AGENTS.md: missing root Global Context file")
        return 0
    version = versions.get("system/global-context")
    lines = path.read_text(encoding="utf-8").splitlines()
    if version is None:
        findings.append("ERROR AGENTS.md: formats/system/global-context.md is missing")
    else:
        expected = f"# AGENTS.md — global context (version {version})"
        if not lines or lines[0].strip() != expected:
            findings.append(f"ERROR AGENTS.md: first line must be {expected!r}")
    secs = parse_sections("\n".join(lines[1:]), 1)
    expected_h1 = [
        "Application Overview",
        "Scope and Out of Scope",
        "Target AI Environment",
        "Before You Act",
        "Every File",
        "Never",
    ]
    actual = [heading for heading, _ in secs]
    if actual != expected_h1:
        findings.append(f"ERROR AGENTS.md: # sections must be {expected_h1}, got {actual}")
    sec_map = dict(secs)
    scope = sec_map.get("Scope and Out of Scope", "")
    if [heading for heading, _ in parse_sections(scope, 2)] != ["In Scope", "Out of Scope"]:
        findings.append("ERROR AGENTS.md -> # Scope and Out of Scope: ## sections must be ['In Scope', 'Out of Scope']")
    target = sec_map.get("Target AI Environment", "")
    sub = parse_sections(target, 2)
    if [heading for heading, _ in sub] != ["Vendor", "Skill Invocation", "Native Capabilities"]:
        findings.append(
            "ERROR AGENTS.md -> # Target AI Environment: ## sections must be "
            "['Vendor', 'Skill Invocation', 'Native Capabilities']"
        )
    vendor = dict(sub).get("Vendor", "").strip()
    if vendor not in VENDORS:
        findings.append(f"ERROR AGENTS.md -> ## Vendor: {vendor!r} is not a known vendor")
    return 1


def parse_owner(value: str) -> tuple[str, list[str]]:
    """Classify a stage's #### Owner as ('Automation', []), ('Roles', [slugs]), or ('Invalid', [])."""
    text = value.strip()
    if AUTOMATION_RE.match(text):
        return "Automation", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines and all(line.startswith("- ") for line in lines):
        return "Roles", [line[2:].strip() for line in lines]
    return "Invalid", []


def lifecycle_files() -> list[Path]:
    if not PROCESS_DIR.is_dir():
        return []
    return sorted(path for path in PROCESS_DIR.glob("*.md") if path.name not in {"README.md", "AGENTS.md"})


def process_map() -> dict[str, dict[str, tuple[str, list[str]]]]:
    """Every process name under process/ mapped to its stage headings and parsed owners. Reports nothing."""
    processes: dict[str, dict[str, tuple[str, list[str]]]] = {}
    for path in lifecycle_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        for name, body in parse_sections("\n".join(lines[1:]), 1):
            stages: dict[str, tuple[str, list[str]]] = {}
            for stage_name, stage_body in parse_sections(dict(parse_sections(body, 2)).get("Stages", ""), 3):
                stages[stage_name] = parse_owner(dict(parse_sections(stage_body, 4)).get("Owner", ""))
            processes.setdefault(name, stages)
    return processes


def role_statuses() -> dict[str, str]:
    body = read_system_body("user-roles.md")
    return lint_roles(body, [], "") if body is not None else {}


def check_processes(findings: list[str]) -> int:
    count = 0
    if not PROCESS_DIR.is_dir():
        findings.append("ERROR process/: directory missing")
        return 0
    roles = role_statuses()
    seen_names: dict[str, str] = {}

    def active_role(slug: str, where: str) -> None:
        if slug not in roles:
            findings.append(f"ERROR {where}: unknown role {slug!r}")
        elif roles[slug] != "Active":
            findings.append(f"ERROR {where}: role {slug!r} is not Active")

    for path in lifecycle_files():
        count += 1
        lines = path.read_text(encoding="utf-8").splitlines()
        match = LIFECYCLE_TITLE_RE.match(lines[0].strip() if lines else "")
        if not match or match.group(1) != path.stem:
            findings.append(f"ERROR {rel(path)}: first line must be '# Lifecycle Stage: {path.stem} (version N)'")
        processes = parse_sections("\n".join(lines[1:]), 1)
        if not processes:
            findings.append(f"ERROR {rel(path)}: at least one '# <Process Name>' section is required")
        for name, body in processes:
            where = f"{rel(path)} -> # {name}"
            if name in seen_names:
                findings.append(f"ERROR {where}: duplicate process name (also in {seen_names[name]})")
            seen_names.setdefault(name, rel(path))
            secs = parse_sections(body, 2)
            actual = [heading for heading, _ in secs]
            if actual != PROCESS_SECTIONS:
                findings.append(f"ERROR {where}: ## sections must be {PROCESS_SECTIONS}, got {actual}")
            sec_map = dict(secs)
            for heading, value in secs:
                if not value.strip():
                    findings.append(f"ERROR {where} -> ## {heading}: section is empty")
            supervisor = sec_map.get("Supervisor Role", "").strip()
            if supervisor:
                if not SLUG_RE.match(supervisor):
                    findings.append(f"ERROR {where} -> ## Supervisor Role: must be a single role slug")
                else:
                    active_role(supervisor, f"{where} -> ## Supervisor Role")
            sor = parse_sections(sec_map.get("System of Record", ""), 3)
            if [heading for heading, _ in sor] != ["Mode", "Location"]:
                findings.append(f"ERROR {where} -> ## System of Record: ### sections must be ['Mode', 'Location']")
            sor_map = dict(sor)
            mode = sor_map.get("Mode", "").strip()
            if mode not in SOR_MODES:
                findings.append(f"ERROR {where} -> ### Mode: {mode!r} is not a system-of-record mode")
            if mode == "External System" and "https://" not in sor_map.get("Location", ""):
                findings.append(f"ERROR {where} -> ### Location: External System must include an https:// link")
            stages = parse_sections(sec_map.get("Stages", ""), 3)
            if not stages:
                findings.append(f"ERROR {where} -> ## Stages: at least one stage is required")
            for index, (stage_name, stage_body) in enumerate(stages, start=1):
                stage_where = f"{where} -> ### {stage_name}"
                if not stage_name.startswith(f"Stage {index}: ") or not STAGE_HEADING_RE.match(stage_name):
                    findings.append(f"ERROR {where} -> ## Stages: expected 'Stage {index}: <Name>', got {stage_name!r}")
                h4 = parse_sections(stage_body, 4)
                if [heading for heading, _ in h4] != STAGE_SECTIONS:
                    findings.append(f"ERROR {stage_where}: #### sections must be {STAGE_SECTIONS}")
                h4_map = dict(h4)
                for heading, value in h4:
                    if not value.strip():
                        findings.append(f"ERROR {stage_where} -> #### {heading}: section is empty")
                kind, owner_roles = parse_owner(h4_map.get("Owner", ""))
                if "Owner" in h4_map and kind == "Invalid":
                    findings.append(
                        f"ERROR {stage_where} -> #### Owner: must be a bullet list of role slugs, "
                        "'Automation: On-Demand', or 'Automation: Recurring (<schedule>)'"
                    )
                if len(set(owner_roles)) != len(owner_roles):
                    findings.append(f"ERROR {stage_where} -> #### Owner: duplicate role slug")
                for slug in owner_roles:
                    if not SLUG_RE.match(slug):
                        findings.append(f"ERROR {stage_where} -> #### Owner: {slug!r} is not a role slug")
                    else:
                        active_role(slug, f"{stage_where} -> #### Owner")
                skills_value = h4_map.get("Implementing Skills", "").strip()
                if kind == "Automation" and skills_value.startswith("Manual (Gap)"):
                    findings.append(
                        f"ERROR {stage_where} -> #### Implementing Skills: an Automation stage must name a skill, not Manual (Gap)"
                    )
                if kind == "Automation" and not re.findall(r"`([a-z0-9-]+)`", skills_value):
                    findings.append(f"ERROR {stage_where} -> #### Implementing Skills: an Automation stage must name a skill")
                if not skills_value.startswith(("Manual (Gap)", "External (")):
                    for skill in re.findall(r"`([a-z0-9-]+)`", skills_value):
                        if not (SKILLS_DIR / skill / "SKILL.md").is_file():
                            findings.append(f"ERROR {stage_where} -> #### Implementing Skills: unknown skill {skill!r}")
    return count


def inventory_files(folder: Path, pattern: str, skip: set[str]) -> set[str]:
    return {path.name for path in folder.glob(pattern) if path.name not in skip}


def gitignored(path: Path) -> bool:
    """True when path is ignored. Works in a checkout and in a copy that has .gitignore but no .git."""
    try:
        completed = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", "--", path.as_posix()],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
    except OSError:
        return False
    return completed.returncode == 0


def repository_docs() -> set[str]:
    """Docs an operator has explicitly kept in the repository. Ignored local docs are omitted."""
    expected: set[str] = set()
    if not DOCS_DIR.is_dir():
        return expected
    for path in DOCS_DIR.rglob("*.md"):
        if path.name in {"README.md", "AGENTS.md"} and path.parent == DOCS_DIR:
            continue
        if gitignored(path):
            continue
        expected.add(path.relative_to(DOCS_DIR).as_posix())
    return expected


def check_one_inventory(readme: Path, expected: set[str], findings: list[str]) -> int:
    if not readme.is_file():
        findings.append(f"ERROR {rel(readme)}: missing inventory file")
        return 0
    found = table_targets(readme.read_text(encoding="utf-8"))
    for item in sorted(expected - found):
        findings.append(f"ERROR {rel(readme)}: inventory is missing entry for {item!r}")
    for item in sorted(found - expected):
        findings.append(f"ERROR {rel(readme)}: inventory lists {item!r}, which is not on disk")
    return 1


def check_inventories(findings: list[str]) -> int:
    docs_expected = repository_docs()
    format_expected = {
        path.relative_to(FORMATS_DIR).as_posix()
        for path in FORMATS_DIR.rglob("*.md")
        if path.name not in {"README.md", "AGENTS.md"}
    }
    skill_expected = {
        f"{path.name}/SKILL.md" for path in SKILLS_DIR.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    }
    count = 0
    count += check_one_inventory(DOCS_DIR / "README.md", docs_expected, findings)
    count += check_one_inventory(
        PROCESS_DIR / "README.md", inventory_files(PROCESS_DIR, "*.md", {"README.md", "AGENTS.md"}), findings
    )
    count += check_one_inventory(FORMATS_DIR / "README.md", format_expected, findings)
    count += check_one_inventory(SKILLS_DIR / "README.md", skill_expected, findings)
    count += check_one_inventory(SCRIPTS_DIR / "README.md", inventory_files(SCRIPTS_DIR, "*.py", set()), findings)
    count += check_one_inventory(
        SYSTEM_DIR / "README.md", inventory_files(SYSTEM_DIR, "*.md", {"README.md", "AGENTS.md"}), findings
    )
    return count


def check_reserved(findings: list[str]) -> None:
    for item in RESERVED:
        if not (ROOT / item).is_file():
            findings.append(f"ERROR {item}: reserved framework file is missing")


def check_skills(findings: list[str]) -> int:
    count = 0
    if not SKILLS_DIR.is_dir():
        findings.append("ERROR .agents/skills/: directory missing")
        return 0
    for folder in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        path = folder / "SKILL.md"
        count += 1
        if not path.is_file():
            findings.append(f"ERROR {rel(folder)}: missing SKILL.md")
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(text)
        if not match:
            findings.append(f"ERROR {rel(path)}: missing YAML front matter")
            continue
        fields: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                fields[key.strip()] = value.strip()
        if fields.get("name") != folder.name:
            findings.append(f"ERROR {rel(path)}: front matter name must be {folder.name!r}")
        if not fields.get("description"):
            findings.append(f"ERROR {rel(path)}: front matter description is empty")
        headings = [heading for heading, _ in parse_sections(match.group(2), 2)]
        for required in SKILL_SECTIONS:
            if required not in headings:
                findings.append(f"ERROR {rel(path)}: missing '## {required}' section")
    return count


def check_stale_references(findings: list[str]) -> None:
    roots = [ROOT / "AGENTS.md", ROOT / "README.md", ROOT / "scripts" / "README.md", ROOT / "scripts" / "AGENTS.md"]
    for folder in (PROCESS_DIR, FORMATS_DIR, SYSTEM_DIR, CLIENTS_DIR, DOCS_DIR, SKILLS_DIR, ARCHIVE_DIR):
        if folder.is_dir():
            roots.extend(folder.rglob("*.md"))
    seen: set[Path] = set()
    for path in roots:
        if not path.is_file() or path in seen or gitignored(path):
            continue
        seen.add(path)
        text = path.read_text(encoding="utf-8")
        if STALE_SKILL_RE.search(text):
            findings.append(f"ERROR {rel(path)}: stale skill reference 'create-application'")
        if STALE_FORMAT_RE.search(text):
            findings.append(f"ERROR {rel(path)}: stale flat format path; use formats/system/ or formats/clients/")
        if ARCHIVE_DIR not in path.parents and STALE_ISSUES_RE.search(text):
            findings.append(f"ERROR {rel(path)}: stale open-issues reference; use open-items")


def header_and_body(
    path: Path,
    expected_format: str,
    versions: dict[str, int],
    findings: list[str],
    client: str | None,
) -> tuple[dict[str, str], str]:
    where = rel(path)
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        findings.append(f"ERROR {where}: missing YAML front matter header")
        return {}, text
    header: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            findings.append(f"ERROR {where}: malformed header line {line!r}")
            continue
        key, _, value = line.partition(":")
        header[key.strip()] = value.strip()
    expected_keys = CLIENT_HEADER if expected_format.startswith("clients/") else SYSTEM_HEADER
    if list(header.keys()) != expected_keys:
        findings.append(f"ERROR {where}: header keys must be {expected_keys} in order, got {list(header.keys())}")
    if header.get("format") != expected_format:
        findings.append(f"ERROR {where}: header format must be {expected_format!r}, got {header.get('format')!r}")
    expected_version = str(versions.get(expected_format, ""))
    if not expected_version:
        findings.append(f"ERROR {where}: format {expected_format!r} is not a registered contract")
    elif header.get("format_version") != expected_version:
        findings.append(
            f"ERROR {where}: header format_version must be {expected_version}, got {header.get('format_version')!r}"
        )
    if client is not None and header.get("client") != client:
        findings.append(f"ERROR {where}: header client must be {client!r}, got {header.get('client')!r}")
    for key in ("created", "updated"):
        if not valid_date(header.get(key, "")):
            findings.append(f"ERROR {where}: header {key} must be YYYY-MM-DD")
    for key in ("created_by", "updated_by"):
        value = header.get(key, "")
        if not EMAIL_RE.match(value) or value.split("@")[0].lower() in AGENT_NAMES:
            findings.append(f"ERROR {where}: header {key} must be a human operator email, got {value!r}")
    return header, match.group(2)


def reference_sets() -> tuple[set[str], set[str]]:
    processes = set(process_map())
    skills = {
        path.name for path in SKILLS_DIR.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    } if SKILLS_DIR.is_dir() else set()
    return processes, skills


def lint_roles(body: str, findings: list[str], where: str) -> dict[str, str]:
    parsed = records(body, findings, where)
    statuses: dict[str, str] = {}
    if parsed is None:
        return statuses
    processes, skills = reference_sets()
    for heading, subs in parsed.items():
        if not SLUG_RE.match(heading):
            findings.append(f"ERROR {where} -> # {heading}: role heading must be a lowercase kebab-case slug")
        got = fields_of(subs, ROLE_FIELDS, findings, f"{where} -> # {heading}")
        if got is None:
            continue
        if got["Display Name"] == "None" or got["Purpose"] == "None":
            findings.append(f"ERROR {where} -> # {heading}: Display Name and Purpose are required")
        if got["Status"] not in ROLE_STATUSES:
            findings.append(f"ERROR {where} -> # {heading} -> ## Status: {got['Status']!r} is not a role status")
        statuses[heading] = got["Status"]
        for label, known in (("Processes", processes), ("Skills", skills)):
            values = bullets(got[label], findings, f"{where} -> # {heading} -> ## {label}")
            if values is None:
                continue
            for value in values:
                if value not in known:
                    findings.append(f"ERROR {where} -> # {heading} -> ## {label}: unknown reference {value!r}")
    return statuses


def lint_users(body: str, role_status: dict[str, str], findings: list[str], where: str) -> dict[str, str]:
    parsed = records(body, findings, where)
    statuses: dict[str, str] = {}
    if parsed is None:
        return statuses
    for heading, subs in parsed.items():
        if not EMAIL_RE.match(heading):
            findings.append(f"ERROR {where} -> # {heading}: user heading must be an email address")
        got = fields_of(subs, USER_FIELDS, findings, f"{where} -> # {heading}")
        if got is None:
            continue
        if has_secret(got["Notes"]):
            findings.append(f"ERROR {where} -> # {heading}: Notes must not contain a credential")
        if got["Name"] == "None":
            findings.append(f"ERROR {where} -> # {heading} -> ## Name: a name is required")
        if got["Status"] not in USER_STATUSES:
            findings.append(f"ERROR {where} -> # {heading} -> ## Status: {got['Status']!r} is not a user status")
        statuses[heading] = got["Status"]
        role = got["Primary Role"]
        if role not in role_status:
            findings.append(f"ERROR {where} -> # {heading} -> ## Primary Role: unknown role {role!r}")
        elif got["Status"] == "Active" and role_status[role] != "Active":
            findings.append(f"ERROR {where} -> # {heading}: an Active user requires an Active primary role")
        clients = bullets(got["Assigned Clients"], findings, f"{where} -> # {heading} -> ## Assigned Clients") or []
        if len(set(clients)) != len(clients):
            findings.append(f"ERROR {where} -> # {heading} -> ## Assigned Clients: duplicate client slug")
        if clients and got["Status"] == "Retired":
            findings.append(f"ERROR {where} -> # {heading}: a Retired user must have Assigned Clients of None")
        for slug in clients:
            if not SLUG_RE.match(slug):
                findings.append(f"ERROR {where} -> # {heading} -> ## Assigned Clients: {slug!r} is not a client slug")
            elif not (CLIENTS_DIR / slug).is_dir():
                findings.append(f"ERROR {where} -> # {heading} -> ## Assigned Clients: clients/{slug}/ does not exist")
    return statuses


def lint_external(body: str, users: set[str], findings: list[str], where: str) -> None:
    parsed = records(body, findings, where)
    if not parsed:
        return
    for heading, subs in parsed.items():
        if not SLUG_RE.match(heading):
            findings.append(f"ERROR {where} -> # {heading}: system heading must be a lowercase kebab-case slug")
        got = fields_of(subs, EXTERNAL_FIELDS, findings, f"{where} -> # {heading}")
        if got is None:
            continue
        if has_secret("\n".join(got.values())):
            findings.append(f"ERROR {where} -> # {heading}: a credential must not be stored in external-system guidance")
        if got["Display Name"] == "None" or got["Purpose"] == "None":
            findings.append(f"ERROR {where} -> # {heading}: Display Name and Purpose are required")
        if got["Category"] not in SYSTEM_CATEGORIES:
            findings.append(f"ERROR {where} -> # {heading} -> ## Category: {got['Category']!r} is not a category")
        if got["Status"] not in EXTERNAL_STATUSES:
            findings.append(f"ERROR {where} -> # {heading} -> ## Status: {got['Status']!r} is not a system status")
        owner = got["Owner"]
        if owner != "None" and owner not in users:
            findings.append(f"ERROR {where} -> # {heading} -> ## Owner: unknown user {owner!r}")


def lint_products(body: str, findings: list[str], where: str) -> dict[str, str]:
    parsed = records(body, findings, where)
    specs: dict[str, str] = {}
    if not parsed:
        return specs
    for heading, subs in parsed.items():
        got = fields_of(subs, PRODUCT_FIELDS, findings, f"{where} -> # {heading}")
        if got is None:
            continue
        if got["Overview"] == "None" or got["Specification"] == "None":
            findings.append(f"ERROR {where} -> # {heading}: Overview and Specification are required")
        if "|" in got["Specification"] or "\n" in got["Specification"]:
            findings.append(
                f"ERROR {where} -> # {heading} -> ## Specification: must be one line without a pipe character"
            )
        for name, vocab in (("Pricing Model", PRICING_MODELS), ("Frequency", FREQUENCIES), ("Status", ITEM_STATUSES)):
            if got[name] not in vocab:
                findings.append(f"ERROR {where} -> # {heading} -> ## {name}: {got[name]!r} is not in its vocabulary")
        if got["List Price"] != "None" and not PRICE_RE.match(got["List Price"]):
            findings.append(f"ERROR {where} -> # {heading} -> ## List Price: must be '<number> <CODE>' or None")
        specs[heading] = got["Specification"]
    return specs


def read_system_body(filename: str) -> str | None:
    path = SYSTEM_DIR / filename
    if not path.is_file():
        return None
    match = FRONT_MATTER_RE.match(path.read_text(encoding="utf-8"))
    return match.group(2) if match else None


def contact_ok(text: str) -> bool:
    if text == "None":
        return True
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return (
        len(lines) == 2
        and lines[0].startswith("- Name: ")
        and lines[1].startswith("- Email: ")
        and bool(EMAIL_RE.match(lines[1][len("- Email: "):].strip()))
    )


def validate_order_form_body(
    body: str,
    where: str,
    folder: Path | None,
    catalog: dict[str, str] | None,
    user_emails: set[str] | None,
    findings: list[str],
) -> None:
    secs = parse_sections(body, 1)
    if [heading for heading, _ in secs] != ORDER_SECTIONS:
        findings.append(f"ERROR {where}: # sections must be {ORDER_SECTIONS}, got {[h for h, _ in secs]}")
        return
    sec_map = dict(secs)
    for heading, value in secs:
        if not value.strip():
            findings.append(f"ERROR {where} -> # {heading}: section cannot be empty (use None if unknown)")
    if CARD_RE.search(body):
        findings.append(f"ERROR {where}: must not contain a card or bank number")

    def fields(section: str, expected: list[str]) -> dict[str, str]:
        got = fields_of(parse_sections(sec_map[section], 2), expected, findings, f"{where} -> # {section}")
        return got or {}

    def date_ok(field: str, value: str, allow_none: bool) -> None:
        if value and not (allow_none and value == "None") and not valid_date(value):
            findings.append(f"ERROR {where} -> ## {field}: must be YYYY-MM-DD{' or None' if allow_none else ''}")

    details = fields("Order Details", ORDER_DETAIL_FIELDS)
    if details:
        if details["Status"] not in ORDER_STATUSES:
            findings.append(f"ERROR {where} -> ## Status: {details['Status']!r} is not an order status")
        if details["Renewal"] not in RENEWAL_TERMS:
            findings.append(f"ERROR {where} -> ## Renewal: {details['Renewal']!r} is not a renewal term")
        date_ok("Order Date", details["Order Date"], False)
        date_ok("Effective Date", details["Effective Date"], True)
        date_ok("Term End", details["Term End"], True)
    parties = fields("Parties", ORDER_PARTY_FIELDS)
    if parties:
        if not contact_ok(parties["Customer Signatory"]):
            findings.append(f"ERROR {where} -> ## Customer Signatory: must be '- Name: ...' and '- Email: ...' or None")
        rep_email = parties["Sales Representative"]
        if rep_email != "None" and user_emails is not None and rep_email not in user_emails:
            findings.append(f"ERROR {where} -> ## Sales Representative: {rep_email!r} is not a record in system/users.md")
    terms = fields("Commercial Terms", ORDER_TERMS_FIELDS)
    if terms:
        if terms["Currency"] != "None" and not CURRENCY_RE.match(terms["Currency"]):
            findings.append(f"ERROR {where} -> ## Currency: must be an ISO 4217 code or None")
        if not contact_ok(terms["Billing Contact"]):
            findings.append(f"ERROR {where} -> ## Billing Contact: must be '- Name: ...' and '- Email: ...' or None")
    execution = fields("Execution", ORDER_EXECUTION_FIELDS)
    if execution:
        date_ok("Signed Date", execution["Signed Date"], True)
        if details and details["Status"] == "Signed" and execution["Signed Date"] == "None":
            findings.append(f"ERROR {where} -> ## Signed Date: required once status is Signed")
        copy = execution["Signed Copy"]
        if copy not in {"None", "order-form.pdf"}:
            findings.append(f"ERROR {where} -> ## Signed Copy: must be order-form.pdf or None")
        elif copy == "order-form.pdf" and folder is not None and not (folder / "order-form.pdf").is_file():
            findings.append(f"ERROR {where} -> ## Signed Copy: order-form.pdf is missing")
    rows = parse_table(sec_map["Line Items"], ORDER_LINE_COLUMNS, findings, f"{where} -> # Line Items") or []
    for row in rows:
        name, spec, quantity, _unit, price, frequency = row
        if frequency not in FREQUENCIES:
            findings.append(f"ERROR {where} -> # Line Items: {name!r} frequency {frequency!r} is not a frequency")
        for label, value in (("Quantity", quantity), ("Unit Price", price)):
            if value != "None" and not NUMBER_RE.match(value):
                findings.append(f"ERROR {where} -> # Line Items: {name!r} {label} must be a number or None")
        if catalog is not None:
            if name not in catalog:
                findings.append(f"ERROR {where} -> # Line Items: {name!r} is not in system/products-and-services.md")
            elif spec != catalog[name]:
                findings.append(f"ERROR {where} -> # Line Items: {name!r} Specification differs from the catalog")


def lint_backlog(body: str, findings: list[str], where: str) -> None:
    parsed = records(body, findings, where)
    if not parsed:
        return
    graph: dict[str, list[str]] = {}
    for heading, subs in parsed.items():
        if not re.fullmatch(r"APP-\d{4}", heading):
            findings.append(f"ERROR {where} -> # {heading}: backlog heading must look like APP-0001")
        got = fields_of(subs, BACKLOG_FIELDS, findings, f"{where} -> # {heading}")
        if got is None:
            continue
        if got["Title"] == "None":
            findings.append(f"ERROR {where} -> # {heading}: Title is required")
        request_where = f"{where} -> # {heading} -> ## Request"
        open_points = "None"
        if not got["Request"].startswith("### Statement"):
            findings.append(f"ERROR {request_where}: must open directly with '### Statement'")
        request = fields_of(parse_sections(got["Request"], 3), BACKLOG_REQUEST_FIELDS, findings, request_where)
        if request is not None:
            for name in BACKLOG_REQUIRED_REQUEST_FIELDS:
                if request[name] == "None":
                    findings.append(f"ERROR {request_where} -> ### {name}: required and cannot be None")
            bullets(request["Open Points"], findings, f"{request_where} -> ### Open Points")
            open_points = request["Open Points"]
        if got["Status"] in {"Ready", "In Progress"} and open_points != "None":
            findings.append(f"ERROR {request_where} -> ### Open Points: must be None once status is {got['Status']}")
        if got["Status"] not in BACKLOG_STATUSES:
            findings.append(f"ERROR {where} -> # {heading} -> ## Status: {got['Status']!r} is not a backlog status")
        if not valid_date(got["Opened"]):
            findings.append(f"ERROR {where} -> # {heading} -> ## Opened: must be YYYY-MM-DD")
        if got["Status"] in {"Ready", "In Progress"}:
            for name in ("Refined Requirement", "Acceptance Criteria", "Plan"):
                if got[name] == "None":
                    findings.append(f"ERROR {where} -> # {heading} -> ## {name}: required once status is {got['Status']}")
        if got["Status"] in {"Done", "Cancelled"} and got["Resolution"] == "None":
            findings.append(f"ERROR {where} -> # {heading} -> ## Resolution: required once status is {got['Status']}")
        deps = bullets(got["Dependencies"], findings, f"{where} -> # {heading} -> ## Dependencies") or []
        graph[heading] = deps
        for dep in deps:
            if dep == heading:
                findings.append(f"ERROR {where} -> # {heading}: a backlog item cannot depend on itself")
            elif not re.fullmatch(r"APP-\d{4}", dep):
                findings.append(f"ERROR {where} -> # {heading} -> ## Dependencies: {dep!r} is not a backlog heading")
        for plan_path in re.findall(r"`([^`]+)`", got["Plan"]):
            if "/" in plan_path or plan_path.endswith(".md"):
                if not (ROOT / plan_path).exists():
                    findings.append(f"ERROR {where} -> # {heading} -> ## Plan: missing path {plan_path!r}")
    for heading, deps in graph.items():
        for dep in deps:
            if dep not in graph and re.fullmatch(r"APP-\d{4}", dep):
                findings.append(f"ERROR {where} -> # {heading} -> ## Dependencies: unknown item {dep!r}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def cyclic(item: str) -> bool:
        if item in visiting:
            return True
        if item in visited or item not in graph:
            return False
        visiting.add(item)
        if any(cyclic(dep) for dep in graph[item]):
            return True
        visiting.remove(item)
        visited.add(item)
        return False

    if any(cyclic(item) for item in list(graph)):
        findings.append(f"ERROR {where}: backlog dependencies contain a cycle")


def lint_journal(body: str, findings: list[str], where: str) -> None:
    secs = parse_sections(body, 1)
    if [heading for heading, _ in secs] != ["Open", "Closed"]:
        findings.append(f"ERROR {where}: # sections must be ['Open', 'Closed']")
        return
    processes, skills = reference_sets()
    seen: set[int] = set()
    for name, value in secs:
        columns = (
            ["#", "Asked", "Question", "Skill", "Process", "Stage", "LLM"]
            if name == "Open"
            else ["#", "Asked", "Closed", "Question", "Skill", "Process", "Stage", "LLM", "Change"]
        )
        rows = parse_table(value, columns, findings, f"{where} -> # {name}")
        if not rows:
            continue
        for row in rows:
            try:
                number = int(row[0])
                if number <= 0 or number in seen:
                    raise ValueError
                seen.add(number)
            except ValueError:
                findings.append(f"ERROR {where} -> # {name}: issue # {row[0]!r} is duplicate or not a positive integer")
            if not valid_date(row[1]):
                findings.append(f"ERROR {where} -> # {name}: Asked must be YYYY-MM-DD")
            if name == "Closed" and not valid_date(row[2]):
                findings.append(f"ERROR {where} -> # Closed: Closed must be YYYY-MM-DD")
            skill = row[3] if name == "Open" else row[4]
            process = row[4] if name == "Open" else row[5]
            if skill != EM_DASH and skill not in skills:
                findings.append(f"ERROR {where} -> # {name}: unknown skill {skill!r}")
            if process != EM_DASH and process not in processes:
                findings.append(f"ERROR {where} -> # {name}: unknown process {process!r}")
            if name == "Closed" and (not row[8] or row[8] == EM_DASH):
                findings.append(f"ERROR {where} -> # Closed: Change must name the absorbing change")


def lint_system(versions: dict[str, int], findings: list[str], headers: dict[str, dict[str, str]]) -> int:
    count = 0
    bodies: dict[str, str] = {}
    if not SYSTEM_DIR.is_dir():
        findings.append("ERROR system/: directory missing")
        return 0
    for filename, format_id in SYSTEM_FILES.items():
        path = SYSTEM_DIR / filename
        if not path.is_file():
            findings.append(f"ERROR {rel(path)}: required system record is missing")
            continue
        count += 1
        header, body = header_and_body(path, format_id, versions, findings, None)
        headers[rel(path)] = header
        bodies[filename] = body
    products_path = SYSTEM_DIR / "products-and-services.md"
    if products_path.is_file():
        count += 1
        header, body = header_and_body(products_path, "system/products-and-services", versions, findings, None)
        headers[rel(products_path)] = header
        lint_products(body, findings, "system/products-and-services.md")
    role_status = lint_roles(bodies.get("user-roles.md", "None"), findings, "system/user-roles.md")
    user_status = lint_users(bodies.get("users.md", "None"), role_status, findings, "system/users.md")
    lint_external(bodies.get("external-systems.md", "None"), set(user_status), findings, "system/external-systems.md")
    lint_backlog(bodies.get("application-backlog.md", "None"), findings, "system/application-backlog.md")
    if "question-journal.md" in bodies:
        lint_journal(bodies["question-journal.md"], findings, "system/question-journal.md")
    if user_status:
        known = set(user_status)
        for path_text, header in headers.items():
            for key in ("created_by", "updated_by"):
                email = header.get(key, "")
                if email and email not in known:
                    findings.append(f"WARN  {path_text}: {key} {email!r} is not a record in system/users.md")
    return count


def validate_client_body(body: str, where: str, findings: list[str]) -> None:
    expected = ["General Information", "Business Overview", "Business Problem", "Solution", "Notes"]
    secs = parse_sections(body, 1)
    if [heading for heading, _ in secs] != expected:
        findings.append(f"ERROR {where}: # sections must be {expected}, got {[heading for heading, _ in secs]}")
    sec_map = dict(secs)
    for heading, value in secs:
        if not value.strip():
            findings.append(f"ERROR {where} -> # {heading}: section cannot be empty (use None if unknown)")
    general = parse_sections(sec_map.get("General Information", ""), 2)
    expected_general = ["Name", "Organization", "Website", "Time Zone", "Engagement Started", "Contact"]
    if [heading for heading, _ in general] != expected_general:
        findings.append(f"ERROR {where} -> # General Information: ## sections must be {expected_general}")
    general_map = dict(general)
    started = general_map.get("Engagement Started", "").strip()
    if started and started != "None" and not valid_date(started):
        findings.append(f"ERROR {where} -> ## Engagement Started: must be YYYY-MM-DD or None")
    contact = general_map.get("Contact", "").strip()
    if contact and contact != "None":
        lines = [line.strip() for line in contact.splitlines() if line.strip()]
        if (
            len(lines) != 2
            or not lines[0].startswith("- Name: ")
            or not lines[1].startswith("- Email: ")
            or not EMAIL_RE.match(lines[1][len("- Email: "):].strip())
        ):
            findings.append(f"ERROR {where} -> ## Contact: must be '- Name: ...' and '- Email: <valid-email>' or None")


def validate_open_items(
    body: str, findings: list[str], where: str, user_emails: set[str] | None
) -> tuple[set[int], set[int]]:
    """Validate the four open-items tables. Returns (all ids, closed issue ids)."""
    expected = ["In Flight", "Completed", "Open", "Closed"]
    secs = parse_sections(body, 1)
    if [heading for heading, _ in secs] != expected:
        findings.append(f"ERROR {where}: # sections must be {expected}")
        return set(), set()
    processes = process_map()
    all_ids: set[int] = set()
    closed_ids: set[int] = set()
    columns = {
        "In Flight": IN_FLIGHT_COLUMNS,
        "Completed": COMPLETED_COLUMNS,
        "Open": OPEN_COLUMNS,
        "Closed": CLOSED_COLUMNS,
    }
    for name, value in secs:
        table_where = f"{where} -> # {name}"
        rows = parse_table(value, columns[name], findings, table_where)
        if not rows:
            continue
        for row in rows:
            try:
                number = int(row[0])
                if number <= 0 or number in all_ids:
                    raise ValueError
            except ValueError:
                findings.append(f"ERROR {table_where}: # {row[0]!r} is duplicate across the file or not a positive integer")
                continue
            all_ids.add(number)
            if not valid_date(row[1]):
                findings.append(f"ERROR {table_where}: Opened must be YYYY-MM-DD")
            if name == "In Flight":
                _, _, process, stage, responsible, updated, _ = row
                if not valid_date(updated):
                    findings.append(f"ERROR {table_where}: Updated must be YYYY-MM-DD")
                if process not in processes:
                    findings.append(f"ERROR {table_where}: row {number} names unknown process {process!r}")
                    continue
                if stage not in processes[process]:
                    findings.append(f"ERROR {table_where}: row {number} names unknown stage {stage!r} of {process!r}")
                    continue
                kind, owner_roles = processes[process][stage]
                if responsible == "Automation":
                    if kind != "Automation":
                        findings.append(f"ERROR {table_where}: row {number} is Automation but {stage!r} is role-owned")
                elif EMAIL_RE.match(responsible):
                    if user_emails is not None and responsible not in user_emails:
                        findings.append(f"ERROR {table_where}: row {number} Responsible {responsible!r} is not in system/users.md")
                elif kind == "Automation":
                    findings.append(f"ERROR {table_where}: row {number} Responsible must be Automation for {stage!r}")
                elif not owner_roles or responsible != owner_roles[0]:
                    findings.append(
                        f"ERROR {table_where}: row {number} Responsible {responsible!r} is not the owning role of {stage!r}"
                    )
            elif name == "Completed":
                if not valid_date(row[2]):
                    findings.append(f"ERROR {table_where}: Completed must be YYYY-MM-DD")
                if row[3] not in processes:
                    findings.append(f"ERROR {table_where}: row {number} names unknown process {row[3]!r}")
            else:
                if name == "Open":
                    area = row[2]
                else:
                    closed_ids.add(number)
                    if not valid_date(row[2]):
                        findings.append(f"ERROR {table_where}: Closed must be YYYY-MM-DD")
                    area = row[3]
                if area not in ISSUE_AREAS:
                    findings.append(f"ERROR {table_where}: Area {area!r} is not a known area")
    return all_ids, closed_ids


def validate_decision_log(body: str, findings: list[str], where: str) -> list[tuple[str, str]]:
    secs = parse_sections(body, 1)
    if [heading for heading, _ in secs] != ["Decisions"]:
        findings.append(f"ERROR {where}: # sections must be ['Decisions']")
        return []
    rows = parse_table(
        secs[0][1], ["#", "Date", "Area", "Decision", "Source"], findings, f"{where} -> # Decisions"
    )
    sources: list[tuple[str, str]] = []
    seen: set[int] = set()
    for row in rows or []:
        try:
            number = int(row[0])
            if number <= 0 or number in seen:
                raise ValueError
            seen.add(number)
        except ValueError:
            findings.append(f"ERROR {where}: decision # {row[0]!r} is duplicate or not a positive integer")
        if not valid_date(row[1]):
            findings.append(f"ERROR {where}: Date must be YYYY-MM-DD")
        if row[2] not in ISSUE_AREAS:
            findings.append(f"ERROR {where}: Area {row[2]!r} is not a known area")
        if not row[3]:
            findings.append(f"ERROR {where}: Decision cannot be empty")
        sources.append((row[0], row[4]))
    return sources


def cross_check_decisions(
    closed_ids: set[int], all_ids: set[int], sources: list[tuple[str, str]], findings: list[str], where: str
) -> None:
    cited: dict[int, int] = {}
    for decision_number, source in sources:
        if source == "operator":
            continue
        match = re.fullmatch(r"open-items #(\d+)", source)
        if not match:
            findings.append(f"ERROR {where}: decision #{decision_number} source {source!r} is not valid")
            continue
        issue_id = int(match.group(1))
        if issue_id not in closed_ids:
            findings.append(f"ERROR {where}: decision #{decision_number} cites issue {issue_id}, which is not closed")
        cited[issue_id] = cited.get(issue_id, 0) + 1
        if issue_id not in all_ids:
            findings.append(f"ERROR {where}: decision #{decision_number} cites missing issue {issue_id}")
    for issue_id in sorted(closed_ids):
        if cited.get(issue_id, 0) != 1:
            findings.append(f"ERROR {where}: closed issue {issue_id} must be cited by exactly one decision")


def lint_client_folder(
    folder: Path, slug: str, versions: dict[str, int], findings: list[str], headers: dict[str, dict[str, str]]
) -> int:
    count = 0
    required = {
        "client.md": "clients/client",
        "open-items.md": "clients/open-items",
        "decision-log.md": "clients/decision-log",
    }
    users_body = read_system_body("users.md")
    user_emails = set(records(users_body, [], "") or {}) if users_body is not None else None
    bodies: dict[str, str] = {}
    for filename, format_id in required.items():
        path = folder / filename
        if not path.is_file():
            findings.append(f"ERROR {rel(path)}: required client document is missing")
            continue
        count += 1
        header, body = header_and_body(path, format_id, versions, findings, slug)
        headers[rel(path)] = header
        bodies[filename] = body
    if "client.md" in bodies:
        validate_client_body(bodies["client.md"], rel(folder / "client.md"), findings)
    all_ids, closed_ids = set(), set()
    if "open-items.md" in bodies:
        all_ids, closed_ids = validate_open_items(
            bodies["open-items.md"], findings, rel(folder / "open-items.md"), user_emails
        )
    sources: list[tuple[str, str]] = []
    if "decision-log.md" in bodies:
        sources = validate_decision_log(bodies["decision-log.md"], findings, rel(folder / "decision-log.md"))
    if "open-items.md" in bodies and "decision-log.md" in bodies:
        cross_check_decisions(closed_ids, all_ids, sources, findings, rel(folder / "decision-log.md"))
    order_path = folder / "order-form.md"
    if order_path.is_file():
        count += 1
        header, body = header_and_body(order_path, "clients/order-form", versions, findings, slug)
        headers[rel(order_path)] = header
        catalog_body = read_system_body("products-and-services.md")
        catalog = lint_products(catalog_body, [], "") if catalog_body is not None else None
        validate_order_form_body(body, rel(order_path), folder, catalog, user_emails, findings)
    for stray in sorted(folder.glob("*.md")):
        if stray.name not in required and stray.name != "order-form.md":
            findings.append(f"ERROR {rel(stray)}: file name does not mirror a registered client format")
    readme = CLIENTS_DIR / "README.md"
    if readme.is_file() and slug not in readme.read_text(encoding="utf-8"):
        findings.append(f"ERROR clients/README.md: inventory is missing client {slug!r}")
    return count


def check_staged(headers: dict[str, dict[str, str]], findings: list[str]) -> None:
    try:
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=M"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
    except Exception as exc:
        findings.append(f"WARN  --staged: could not read git index ({exc})")
        return
    for path_text in staged:
        if path_text not in headers:
            continue
        try:
            old_text = subprocess.run(
                ["git", "show", f"HEAD:{path_text}"], cwd=ROOT, capture_output=True, text=True, check=True
            ).stdout
        except subprocess.CalledProcessError:
            continue
        old_match = FRONT_MATTER_RE.match(old_text)
        if not old_match:
            continue
        old_header: dict[str, str] = {}
        for line in old_match.group(1).splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                old_header[key.strip()] = value.strip()
        new_header = headers[path_text]
        if old_header.get("updated") == new_header.get("updated") and old_header.get("updated_by") == new_header.get(
            "updated_by"
        ):
            findings.append(f"ERROR {path_text}: modified in git index but updated/updated_by did not change")


def parse_args(argv: list[str]) -> tuple[Path, list[str], set[str]]:
    root = Path(__file__).resolve().parent.parent
    args: list[str] = []
    flags: set[str] = set()
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--root" and index + 1 < len(argv):
            root = Path(argv[index + 1]).resolve()
            index += 2
            continue
        if arg.startswith("--"):
            flags.add(arg)
        else:
            args.append(arg)
        index += 1
    return root, args, flags


def main(argv: list[str]) -> int:
    root, args, flags = parse_args(argv)
    configure(root)
    findings: list[str] = []
    headers: dict[str, dict[str, str]] = {}
    versions = load_formats(findings)
    checked = len(versions)

    if args:
        folder = CLIENTS_DIR / args[0]
        if not folder.is_dir():
            print(f"ERROR clients/{args[0]}: no such client folder")
            return 1
        checked += lint_client_folder(folder, args[0], versions, findings, headers)
    else:
        checked += check_global_context(versions, findings)
        checked += check_processes(findings)
        checked += check_inventories(findings)
        checked += check_skills(findings)
        check_reserved(findings)
        check_stale_references(findings)
        checked += lint_system(versions, findings, headers)
        if CLIENTS_DIR.is_dir():
            for folder in sorted(path for path in CLIENTS_DIR.iterdir() if path.is_dir()):
                checked += lint_client_folder(folder, folder.name, versions, findings, headers)

    if "--staged" in flags:
        check_staged(headers, findings)

    for finding in sorted(findings, key=lambda item: (not item.startswith("ERROR"), item)):
        print(finding)
    errors = sum(1 for finding in findings if finding.startswith("ERROR"))
    warnings = len(findings) - errors
    print(f"{checked} document(s) checked: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
