#!/usr/bin/env python3
"""Lint every governed Markdown document, process, format, and inventory in the repository.

Usage:
  python3 scripts/check.py                  # whole repository
  python3 scripts/check.py <client-slug>    # one client folder
  python3 scripts/check.py --handoff <path> # validate an onboarding handoff file
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
ISSUE_AREAS = {"Client", "Entitlements", "Access", "Process"}
USER_STATUSES = {"Active", "Retired"}
ROLE_STATUSES = {"Active", "Retired"}
ASSIGNMENT_STATUSES = {"Active", "Ended"}
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
    "client-assignments.md": "system/client-assignments",
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
USER_FIELDS = ["Name", "Primary Role", "Status", "Notes"]
ROLE_FIELDS = ["Display Name", "Purpose", "Core Tasks", "Processes", "Skills", "Status"]
ASSIGNMENT_FIELDS = ["User", "Role", "Client", "Status", "Started", "Ended", "Notes"]
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

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
STALE_SKILL_RE = re.compile(r"(?<![\w-])create-application(?![\w-])")
STALE_FORMAT_RE = re.compile(
    r"(?<![\w/])formats/(global-context|process|client|open-issues|handoff|decision-log|question-journal)\.md"
)
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


def check_processes(findings: list[str]) -> int:
    count = 0
    expected_h1 = [
        "Purpose",
        "Scope",
        "Roles",
        "Cadence",
        "System of Record",
        "Inputs",
        "Stages",
        "Outputs",
        "Rules",
        "Related",
    ]
    expected_stage = [
        "Entry Criteria",
        "Description",
        "Graduation Criteria",
        "Branching and Terminal Paths",
        "Implementing Skills",
    ]
    if not PROCESS_DIR.is_dir():
        findings.append("ERROR process/: directory missing")
        return 0
    for path in sorted(PROCESS_DIR.glob("*.md")):
        if path.name in {"README.md", "AGENTS.md"}:
            continue
        count += 1
        lines = path.read_text(encoding="utf-8").splitlines()
        match = re.match(r"^# Process: ([a-z0-9-]+) \(version (\d+)\)$", lines[0].strip() if lines else "")
        if not match or match.group(1) != path.stem:
            findings.append(f"ERROR {rel(path)}: first line must be '# Process: {path.stem} (version N)'")
        secs = parse_sections("\n".join(lines[1:]), 1)
        actual = [heading for heading, _ in secs]
        if actual != expected_h1:
            findings.append(f"ERROR {rel(path)}: # sections must be {expected_h1}, got {actual}")
        sec_map = dict(secs)
        sor = parse_sections(sec_map.get("System of Record", ""), 2)
        if [heading for heading, _ in sor] != ["Mode", "Location"]:
            findings.append(f"ERROR {rel(path)} -> # System of Record: ## sections must be ['Mode', 'Location']")
        sor_map = dict(sor)
        mode = sor_map.get("Mode", "").strip()
        if mode not in SOR_MODES:
            findings.append(f"ERROR {rel(path)} -> ## Mode: {mode!r} is not a system-of-record mode")
        if mode == "External System" and "https://" not in sor_map.get("Location", ""):
            findings.append(f"ERROR {rel(path)} -> ## Location: External System must include an https:// link")
        stages = parse_sections(sec_map.get("Stages", ""), 2)
        if not stages:
            findings.append(f"ERROR {rel(path)} -> # Stages: at least one stage is required")
        for index, (name, stage_body) in enumerate(stages, start=1):
            if not name.startswith(f"Stage {index}: "):
                findings.append(f"ERROR {rel(path)} -> # Stages: expected 'Stage {index}: <Name>', got {name!r}")
            h3 = parse_sections(stage_body, 3)
            if [heading for heading, _ in h3] != expected_stage:
                findings.append(f"ERROR {rel(path)} -> ## {name}: ### sections must be {expected_stage}")
            for heading, value in h3:
                if not value.strip():
                    findings.append(f"ERROR {rel(path)} -> ## {name} -> ### {heading}: section is empty")
                if heading == "Implementing Skills" and not value.strip().startswith(("Manual (Gap)", "External (")):
                    for skill in re.findall(r"`([a-z0-9-]+)`", value):
                        if not (SKILLS_DIR / skill / "SKILL.md").is_file():
                            findings.append(
                                f"ERROR {rel(path)} -> ## {name} -> ### Implementing Skills: unknown skill {skill!r}"
                            )
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
    processes = {
        path.stem for path in PROCESS_DIR.glob("*.md") if path.name not in {"README.md", "AGENTS.md"}
    } if PROCESS_DIR.is_dir() else set()
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
    return statuses


def lint_assignments(
    body: str, user_status: dict[str, str], role_status: dict[str, str], findings: list[str], where: str
) -> None:
    parsed = records(body, findings, where)
    if not parsed:
        return
    seen: set[tuple[str, str]] = set()
    for heading, subs in parsed.items():
        if not re.fullmatch(r"A-\d{4}", heading):
            findings.append(f"ERROR {where} -> # {heading}: assignment heading must look like A-0001")
        got = fields_of(subs, ASSIGNMENT_FIELDS, findings, f"{where} -> # {heading}")
        if got is None:
            continue
        user = got["User"]
        role = got["Role"]
        client = got["Client"]
        status = got["Status"]
        if user not in user_status:
            findings.append(f"ERROR {where} -> # {heading} -> ## User: unknown user {user!r}")
        if role not in role_status:
            findings.append(f"ERROR {where} -> # {heading} -> ## Role: unknown role {role!r}")
        if not SLUG_RE.match(client):
            findings.append(f"ERROR {where} -> # {heading} -> ## Client: {client!r} is not a client slug")
        if status not in ASSIGNMENT_STATUSES:
            findings.append(f"ERROR {where} -> # {heading} -> ## Status: {status!r} is not an assignment status")
        if not valid_date(got["Started"]):
            findings.append(f"ERROR {where} -> # {heading} -> ## Started: must be YYYY-MM-DD")
        client_dir = CLIENTS_DIR / client
        archive_dir = ARCHIVE_DIR / client
        if status == "Active":
            if got["Ended"] != "None":
                findings.append(f"ERROR {where} -> # {heading}: an Active assignment has Ended of None")
            if user_status.get(user) == "Retired" or role_status.get(role) == "Retired":
                findings.append(f"ERROR {where} -> # {heading}: an Active assignment cannot use a Retired user or role")
            if not client_dir.is_dir():
                findings.append(f"ERROR {where} -> # {heading} -> ## Client: clients/{client}/ does not exist")
            pair = (user, client)
            if pair in seen:
                findings.append(f"ERROR {where} -> # {heading}: duplicate Active assignment for this user and client")
            seen.add(pair)
        elif status == "Ended":
            if not valid_date(got["Ended"]):
                findings.append(f"ERROR {where} -> # {heading} -> ## Ended: an Ended assignment needs YYYY-MM-DD")
            if not client_dir.is_dir() and not archive_dir.is_dir():
                findings.append(f"ERROR {where} -> # {heading} -> ## Client: {client!r} is not in clients/ or archive/")


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
        if got["Title"] == "None" or got["Request"] == "None":
            findings.append(f"ERROR {where} -> # {heading}: Title and Request are required")
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
    role_status = lint_roles(bodies.get("user-roles.md", "None"), findings, "system/user-roles.md")
    user_status = lint_users(bodies.get("users.md", "None"), role_status, findings, "system/users.md")
    lint_assignments(
        bodies.get("client-assignments.md", "None"), user_status, role_status, findings, "system/client-assignments.md"
    )
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


def validate_client_body(body: str, where: str, folder: Path | None, findings: list[str]) -> None:
    expected = ["General Information", "Business Overview", "Business Problem", "Solution", "Entitlements", "Notes"]
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
    entitlements = parse_sections(sec_map.get("Entitlements", ""), 2)
    expected_entitlements = ["Order Form", "Plan Name", "Starts", "Renews", "Deliverables"]
    if [heading for heading, _ in entitlements] != expected_entitlements:
        findings.append(f"ERROR {where} -> # Entitlements: ## sections must be {expected_entitlements}")
    ent_map = dict(entitlements)
    order_form = ent_map.get("Order Form", "").strip()
    if folder is not None and order_form == "order-form.pdf" and not (folder / "order-form.pdf").is_file():
        findings.append(f"ERROR {where} -> ## Order Form: order-form.pdf is missing")
    starts = ent_map.get("Starts", "").strip()
    if starts and starts != "None" and not MONTH_RE.match(starts):
        findings.append(f"ERROR {where} -> ## Starts: must be YYYY-MM or None")
    renews = ent_map.get("Renews", "").strip()
    if renews and renews != "None" and not valid_date(renews):
        findings.append(f"ERROR {where} -> ## Renews: must be YYYY-MM-DD or None")


def validate_open_issues(body: str, findings: list[str], where: str) -> tuple[set[int], set[int]]:
    secs = parse_sections(body, 1)
    if [heading for heading, _ in secs] != ["Open", "Closed"]:
        findings.append(f"ERROR {where}: # sections must be ['Open', 'Closed']")
        return set(), set()
    all_ids: set[int] = set()
    closed_ids: set[int] = set()
    for name, value in secs:
        columns = (
            ["#", "Opened", "Area", "Issue", "Next Step"]
            if name == "Open"
            else ["#", "Opened", "Closed", "Area", "Issue", "Resolution"]
        )
        rows = parse_table(value, columns, findings, f"{where} -> # {name}")
        if not rows:
            continue
        for row in rows:
            try:
                number = int(row[0])
                if number <= 0 or number in all_ids:
                    raise ValueError
            except ValueError:
                findings.append(f"ERROR {where} -> # {name}: issue # {row[0]!r} is duplicate or not a positive integer")
                continue
            all_ids.add(number)
            if not valid_date(row[1]):
                findings.append(f"ERROR {where} -> # {name}: Opened must be YYYY-MM-DD")
            if name == "Open":
                area = row[2]
            else:
                closed_ids.add(number)
                if not valid_date(row[2]):
                    findings.append(f"ERROR {where} -> # Closed: Closed must be YYYY-MM-DD")
                area = row[3]
            if area not in ISSUE_AREAS:
                findings.append(f"ERROR {where} -> # {name}: Area {area!r} is not a known area")
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
        match = re.fullmatch(r"open-issues #(\d+)", source)
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
        "open-issues.md": "clients/open-issues",
        "decision-log.md": "clients/decision-log",
    }
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
        validate_client_body(bodies["client.md"], rel(folder / "client.md"), folder, findings)
    all_ids, closed_ids = set(), set()
    if "open-issues.md" in bodies:
        all_ids, closed_ids = validate_open_issues(bodies["open-issues.md"], findings, rel(folder / "open-issues.md"))
    sources: list[tuple[str, str]] = []
    if "decision-log.md" in bodies:
        sources = validate_decision_log(bodies["decision-log.md"], findings, rel(folder / "decision-log.md"))
    if "open-issues.md" in bodies and "decision-log.md" in bodies:
        cross_check_decisions(closed_ids, all_ids, sources, findings, rel(folder / "decision-log.md"))
    for stray in sorted(folder.glob("*.md")):
        if stray.name not in required:
            findings.append(f"ERROR {rel(stray)}: file name does not mirror a registered client format")
    readme = CLIENTS_DIR / "README.md"
    if readme.is_file() and slug not in readme.read_text(encoding="utf-8"):
        findings.append(f"ERROR clients/README.md: inventory is missing client {slug!r}")
    return count


def shift_headings_up(text: str) -> str:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        out.append(line[1:] if not in_fence and line.startswith("##") else line)
    return "\n".join(out)


def lint_handoff(path: Path, versions: dict[str, int], findings: list[str]) -> int:
    where = rel(path)
    header, body = header_and_body(path, "clients/handoff", versions, findings, None)
    if header.get("client") and not SLUG_RE.match(header.get("client", "")):
        findings.append(f"ERROR {where}: header client must be a lowercase kebab-case slug")
    chapters = parse_sections(body, 1)
    expected = ["Client", "Open Issues", "Decision Log"]
    if [heading for heading, _ in chapters] != expected:
        findings.append(f"ERROR {where}: handoff # chapters must be {expected}, got {[heading for heading, _ in chapters]}")
        return 1
    chapter_map = dict(chapters)
    client_body = shift_headings_up(chapter_map["Client"])
    validate_client_body(client_body, f"{where} (# Client)", None, findings)
    order_form = re.search(r"^## Order Form\n+([^\n#]+)", client_body, re.M)
    if order_form and order_form.group(1).strip() != "None" and not (path.parent / order_form.group(1).strip()).is_file():
        findings.append(f"ERROR {where}: order form {order_form.group(1).strip()!r} does not exist beside the handoff")
    all_ids, closed_ids = validate_open_issues(
        shift_headings_up(chapter_map["Open Issues"]), findings, f"{where} (# Open Issues)"
    )
    sources = validate_decision_log(
        shift_headings_up(chapter_map["Decision Log"]), findings, f"{where} (# Decision Log)"
    )
    cross_check_decisions(closed_ids, all_ids, sources, findings, f"{where} (# Decision Log)")
    if "\nNone" in client_body and chapter_map["Open Issues"].strip().endswith("None"):
        findings.append(f"WARN  {where}: # Client contains None sections; setup-client will add them to the Setup Ledger")
    return 1


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

    if "--handoff" in flags:
        if not args or not Path(args[0]).is_file():
            print("ERROR --handoff requires a path to an existing handoff Markdown file")
            return 1
        checked += lint_handoff(Path(args[0]).resolve(), versions, findings)
    elif args:
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
