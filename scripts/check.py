#!/usr/bin/env python3
"""Lint every governed Markdown document, process, format, and inventory in the repository.

Usage:
  python3 scripts/check.py                  # whole repository
  python3 scripts/check.py <client-slug>    # one client folder
  python3 scripts/check.py --handoff <path> # validate an onboarding handoff file before setup-client
  python3 scripts/check.py --staged         # also require updated/updated_by to change on staged client docs

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
SKILLS_DIR = ROOT / ".agents" / "skills"
SCRIPTS_DIR = ROOT / "scripts"

FORMAT_VERSIONS = {
    "global-context": 1,
    "process": 1,
    "client": 1,
    "open-issues": 1,
    "handoff": 1,
}

VENDORS = {"Claude", "OpenAI", "Gemini"}
SOR_MODES = {"Repository Markdown", "External System"}
ISSUE_AREAS = {"Client", "Entitlements", "Access", "Process"}
AGENT_NAMES = {"claude", "codex", "chatgpt", "gemini", "cursor", "agent", "ai", "bot"}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


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
    """Return list of (heading_text, section_content) at the given heading level."""
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
    return [(h, "\n".join(lines).strip()) for h, lines in sections]


def check_global_context(findings: list[str]) -> int:
    path = ROOT / "AGENTS.md"
    if not path.is_file():
        findings.append("ERROR AGENTS.md: missing root Global Context file")
        return 0
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    expected_title = f"# AGENTS.md — global context (version {FORMAT_VERSIONS['global-context']})"
    if not lines or lines[0].strip() != expected_title:
        findings.append(f"ERROR AGENTS.md: first line must be {expected_title!r}")
    body = "\n".join(lines[1:])
    secs = parse_sections(body, 1)
    expected_h1 = [
        "Application Overview",
        "Scope and Out of Scope",
        "Target AI Environment",
        "Before You Act",
        "Every File",
        "Never",
    ]
    actual_h1 = [h for h, _ in secs]
    if actual_h1 != expected_h1:
        findings.append(f"ERROR AGENTS.md: # sections must be {expected_h1}, got {actual_h1}")
    sec_map = dict(secs)
    if "Scope and Out of Scope" in sec_map:
        sub = [h for h, _ in parse_sections(sec_map["Scope and Out of Scope"], 2)]
        if sub != ["In Scope", "Out of Scope"]:
            findings.append(
                f"ERROR AGENTS.md -> # Scope and Out of Scope: ## sections must be ['In Scope', 'Out of Scope'], got {sub}"
            )
    if "Target AI Environment" in sec_map:
        sub_secs = parse_sections(sec_map["Target AI Environment"], 2)
        sub_names = [h for h, _ in sub_secs]
        expected_sub = ["Vendor", "Skill Invocation", "Native Capabilities"]
        if sub_names != expected_sub:
            findings.append(
                f"ERROR AGENTS.md -> # Target AI Environment: ## sections must be {expected_sub}, got {sub_names}"
            )
        sub_map = dict(sub_secs)
        vendor = sub_map.get("Vendor", "").strip()
        if vendor not in VENDORS:
            findings.append(
                f"ERROR AGENTS.md -> # Target AI Environment -> ## Vendor: {vendor!r} not in {sorted(VENDORS)}"
            )
    return 1


def check_formats_dir(findings: list[str]) -> int:
    count = 0
    if not FORMATS_DIR.is_dir():
        findings.append("ERROR formats/: directory missing")
        return 0
    expected_h2 = ["Purpose", "Location", "Header", "Body", "Rules", "Vocabularies", "Checks"]
    for p in sorted(FORMATS_DIR.glob("*.md")):
        if p.name in {"README.md", "AGENTS.md"}:
            continue
        count += 1
        r = rel(p)
        lines = p.read_text(encoding="utf-8").splitlines()
        slug = p.stem
        m = re.match(r"^# Format: ([a-z0-9-]+) \(version (\d+)\)$", lines[0].strip() if lines else "")
        if not m or m.group(1) != slug:
            findings.append(f"ERROR {r}: first line must be '# Format: {slug} (version N)'")
        elif slug in FORMAT_VERSIONS and int(m.group(2)) != FORMAT_VERSIONS[slug]:
            findings.append(
                f"ERROR {r}: format version {m.group(2)} does not match FORMAT_VERSIONS[{slug!r}]={FORMAT_VERSIONS[slug]}"
            )
        body = "\n".join(lines[1:])
        h2 = [h for h, _ in parse_sections(body, 2)]
        for req in expected_h2:
            if req not in h2:
                findings.append(f"ERROR {r}: missing '## {req}' section")
    return count


def check_processes_dir(findings: list[str]) -> int:
    count = 0
    if not PROCESS_DIR.is_dir():
        findings.append("ERROR process/: directory missing")
        return 0
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
    expected_stage_h3 = [
        "Entry Criteria",
        "Description",
        "Graduation Criteria",
        "Branching and Terminal Paths",
        "Implementing Skills",
    ]
    for p in sorted(PROCESS_DIR.glob("*.md")):
        if p.name in {"README.md", "AGENTS.md"}:
            continue
        count += 1
        r = rel(p)
        lines = p.read_text(encoding="utf-8").splitlines()
        slug = p.stem
        m = re.match(r"^# Process: ([a-z0-9-]+) \(version (\d+)\)$", lines[0].strip() if lines else "")
        if not m or m.group(1) != slug:
            findings.append(f"ERROR {r}: first line must be '# Process: {slug} (version N)'")
        body = "\n".join(lines[1:])
        secs = parse_sections(body, 1)
        actual_h1 = [h for h, _ in secs]
        if actual_h1 != expected_h1:
            findings.append(f"ERROR {r}: # sections must be {expected_h1}, got {actual_h1}")
        sec_map = dict(secs)
        if "System of Record" in sec_map:
            sor_secs = parse_sections(sec_map["System of Record"], 2)
            sor_names = [h for h, _ in sor_secs]
            if sor_names != ["Mode", "Location"]:
                findings.append(
                    f"ERROR {r} -> # System of Record: ## sections must be ['Mode', 'Location'], got {sor_names}"
                )
            sor_map = dict(sor_secs)
            mode = sor_map.get("Mode", "").strip()
            loc = sor_map.get("Location", "").strip()
            if mode not in SOR_MODES:
                findings.append(f"ERROR {r} -> # System of Record -> ## Mode: {mode!r} not in {sorted(SOR_MODES)}")
            if mode == "External System" and "https://" not in loc:
                findings.append(
                    f"ERROR {r} -> # System of Record -> ## Location: External System must include an https:// link"
                )
        if "Stages" in sec_map:
            stages = parse_sections(sec_map["Stages"], 2)
            if not stages:
                findings.append(f"ERROR {r} -> # Stages: must define at least one '## Stage 1: <Name>'")
            for idx, (st_name, st_body) in enumerate(stages, start=1):
                if not st_name.startswith(f"Stage {idx}: "):
                    findings.append(f"ERROR {r} -> # Stages: expected 'Stage {idx}: <Name>', got {st_name!r}")
                h3 = parse_sections(st_body, 3)
                h3_names = [h for h, _ in h3]
                if h3_names != expected_stage_h3:
                    findings.append(
                        f"ERROR {r} -> ## {st_name}: ### sections must be {expected_stage_h3}, got {h3_names}"
                    )
                for h_name, h_val in h3:
                    if not h_val.strip():
                        findings.append(f"ERROR {r} -> ## {st_name} -> ### {h_name}: section is empty")
                    if h_name == "Implementing Skills" and not h_val.strip().startswith(("Manual (Gap)", "External (")):
                        for sk in re.findall(r"`([a-z0-9-]+)`", h_val):
                            if not (SKILLS_DIR / sk / "SKILL.md").is_file():
                                findings.append(
                                    f"ERROR {r} -> ## {st_name} -> ### Implementing Skills: unknown skill {sk!r}"
                                )
    return count


def check_inventories(findings: list[str]) -> int:
    checks = [
        (DOCS_DIR, [p.name for p in DOCS_DIR.glob("*.md") if p.name not in {"README.md", "AGENTS.md"}]),
        (PROCESS_DIR, [p.name for p in PROCESS_DIR.glob("*.md") if p.name not in {"README.md", "AGENTS.md"}]),
        (FORMATS_DIR, [p.name for p in FORMATS_DIR.glob("*.md") if p.name not in {"README.md", "AGENTS.md"}]),
        (SKILLS_DIR, [p.name for p in SKILLS_DIR.iterdir() if p.is_dir()]),
        (SCRIPTS_DIR, [p.name for p in SCRIPTS_DIR.glob("*.py")]),
    ]
    count = 0
    for folder, items in checks:
        readme = folder / "README.md"
        if not readme.is_file():
            findings.append(f"ERROR {rel(folder)}/README.md: missing inventory file")
            continue
        count += 1
        text = readme.read_text(encoding="utf-8")
        for item in sorted(items):
            if item not in text:
                findings.append(f"ERROR {rel(readme)}: inventory is missing entry for {item!r}")
    return count


def parse_header_and_body(
    path: Path, r: str, expected_format: str, expected_client: str | None, findings: list[str]
) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(text)
    if not m:
        findings.append(f"ERROR {r}: missing YAML front matter header")
        return {}, text
    header: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            findings.append(f"ERROR {r}: malformed header line {line!r}")
            continue
        k, _, v = line.partition(":")
        header[k.strip()] = v.strip()

    required_keys = ["title", "format", "format_version", "client", "created", "created_by", "updated", "updated_by"]
    if list(header.keys()) != required_keys:
        findings.append(f"ERROR {r}: header keys must be {required_keys} in order, got {list(header.keys())}")

    if header.get("format") != expected_format:
        findings.append(f"ERROR {r}: header format must be {expected_format!r}, got {header.get('format')!r}")
    expected_ver = str(FORMAT_VERSIONS.get(expected_format, 1))
    if header.get("format_version") != expected_ver:
        findings.append(
            f"ERROR {r}: header format_version must be {expected_ver}, got {header.get('format_version')!r}"
        )
    if expected_client and header.get("client") != expected_client:
        findings.append(f"ERROR {r}: header client must be {expected_client!r}, got {header.get('client')!r}")
    elif not expected_client and not re.match(r"^[a-z0-9-]+$", header.get("client", "")):
        findings.append(f"ERROR {r}: header client must be a lowercase kebab-case slug")

    for d_key in ("created", "updated"):
        if not valid_date(header.get(d_key, "")):
            findings.append(f"ERROR {r}: header {d_key} must be YYYY-MM-DD, got {header.get(d_key)!r}")
    for e_key in ("created_by", "updated_by"):
        val = header.get(e_key, "")
        if not EMAIL_RE.match(val) or val.split("@")[0].lower() in AGENT_NAMES:
            findings.append(f"ERROR {r}: header {e_key} must be a human operator email, got {val!r}")

    return header, m.group(2)


def validate_client_body(body: str, r: str, folder: Path | None, findings: list[str]) -> None:
    expected_h1 = ["General Information", "Business Overview", "Business Problem", "Solution", "Entitlements", "Notes"]
    secs = parse_sections(body, 1)
    actual_h1 = [h for h, _ in secs]
    if actual_h1 != expected_h1:
        findings.append(f"ERROR {r}: # sections must be {expected_h1}, got {actual_h1}")
    sec_map = dict(secs)
    for h_name, h_val in secs:
        if not h_val.strip():
            findings.append(f"ERROR {r} -> # {h_name}: section cannot be empty (use None if unknown)")

    if "General Information" in sec_map:
        gi = parse_sections(sec_map["General Information"], 2)
        expected_gi = ["Name", "Organization", "Website", "Time Zone", "Engagement Started", "Contact"]
        if [h for h, _ in gi] != expected_gi:
            findings.append(
                f"ERROR {r} -> # General Information: ## sections must be {expected_gi}, got {[h for h, _ in gi]}"
            )
        gi_map = dict(gi)
        started = gi_map.get("Engagement Started", "").strip()
        if started != "None" and not valid_date(started):
            findings.append(f"ERROR {r} -> ## Engagement Started: must be YYYY-MM-DD or None, got {started!r}")
        contact = gi_map.get("Contact", "").strip()
        if contact != "None":
            c_lines = [ln.strip() for ln in contact.splitlines() if ln.strip()]
            if (
                len(c_lines) != 2
                or not c_lines[0].startswith("- Name: ")
                or not c_lines[1].startswith("- Email: ")
                or not EMAIL_RE.match(c_lines[1][len("- Email: "):].strip())
            ):
                findings.append(
                    f"ERROR {r} -> ## Contact: must be '- Name: ...' and '- Email: <valid-email>' or None"
                )

    if "Entitlements" in sec_map:
        ent = parse_sections(sec_map["Entitlements"], 2)
        expected_ent = ["Order Form", "Plan Name", "Starts", "Renews", "Deliverables"]
        if [h for h, _ in ent] != expected_ent:
            findings.append(
                f"ERROR {r} -> # Entitlements: ## sections must be {expected_ent}, got {[h for h, _ in ent]}"
            )
        ent_map = dict(ent)
        of_val = ent_map.get("Order Form", "").strip()
        if folder is not None and of_val == "order-form.pdf" and not (folder / "order-form.pdf").is_file():
            findings.append(f"ERROR {r} -> ## Order Form: order-form.pdf is named but missing in {rel(folder)}")
        starts = ent_map.get("Starts", "").strip()
        if starts != "None" and not MONTH_RE.match(starts):
            findings.append(f"ERROR {r} -> ## Starts: must be YYYY-MM or None, got {starts!r}")
        renews = ent_map.get("Renews", "").strip()
        if renews != "None" and not valid_date(renews):
            findings.append(f"ERROR {r} -> ## Renews: must be YYYY-MM-DD or None, got {renews!r}")


def validate_open_issues_body(body: str, r: str, findings: list[str]) -> None:
    secs = parse_sections(body, 1)
    if [h for h, _ in secs] != ["Open", "Closed"]:
        findings.append(f"ERROR {r}: # sections must be ['Open', 'Closed'], got {[h for h, _ in secs]}")
        return
    seen_ids: set[int] = set()
    for sec_name, sec_val in secs:
        val = sec_val.strip()
        if val == "None":
            continue
        lines = [ln.strip() for ln in val.splitlines() if ln.strip()]
        expected_cols = (
            ["#", "Opened", "Area", "Issue", "Next Step"]
            if sec_name == "Open"
            else ["#", "Opened", "Closed", "Area", "Issue", "Resolution"]
        )
        if len(lines) < 2:
            findings.append(f"ERROR {r} -> # {sec_name}: must be 'None' or a valid Markdown table")
            continue
        cols = [c.strip() for c in lines[0].strip("|").split("|")]
        if cols != expected_cols:
            findings.append(f"ERROR {r} -> # {sec_name}: table columns must be {expected_cols}, got {cols}")
            continue
        for row_line in lines[2:]:
            cells = [c.strip() for c in row_line.strip("|").split("|")]
            if len(cells) != len(expected_cols):
                findings.append(f"ERROR {r} -> # {sec_name}: malformed row {row_line!r}")
                continue
            try:
                issue_id = int(cells[0])
                if issue_id <= 0 or issue_id in seen_ids:
                    findings.append(f"ERROR {r} -> # {sec_name}: duplicate or non-positive issue # {cells[0]!r}")
                seen_ids.add(issue_id)
            except ValueError:
                findings.append(f"ERROR {r} -> # {sec_name}: issue # must be an integer, got {cells[0]!r}")
            if not valid_date(cells[1]):
                findings.append(f"ERROR {r} -> # {sec_name}: Opened must be YYYY-MM-DD, got {cells[1]!r}")
            if sec_name == "Open":
                area = cells[2]
            else:
                if not valid_date(cells[2]):
                    findings.append(f"ERROR {r} -> # {sec_name}: Closed must be YYYY-MM-DD, got {cells[2]!r}")
                area = cells[3]
            if area not in ISSUE_AREAS:
                findings.append(f"ERROR {r} -> # {sec_name}: Area {area!r} not in {sorted(ISSUE_AREAS)}")


def shift_headings_up(text: str) -> str:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("##"):
            out.append(line[1:])
        else:
            out.append(line)
    return "\n".join(out)


def lint_handoff(path: Path, findings: list[str]) -> int:
    r = rel(path)
    header, body = parse_header_and_body(path, r, "handoff", None, findings)
    slug = header.get("client", "")
    chapters = parse_sections(body, 1)
    expected_chapters = ["Client", "Open Issues"]
    if [h for h, _ in chapters] != expected_chapters:
        findings.append(f"ERROR {r}: handoff # chapters must be {expected_chapters}, got {[h for h, _ in chapters]}")
        return 1
    ch_map = dict(chapters)
    client_body = shift_headings_up(ch_map["Client"])
    validate_client_body(client_body, f"{r} (# Client)", None, findings)
    # Check order form path if not None
    m_of = re.search(r"^## Order Form\n+([^\n#]+)", client_body, re.M)
    if m_of:
        of_val = m_of.group(1).strip()
        if of_val != "None" and not (path.parent / of_val).is_file():
            findings.append(f"ERROR {r} (# Client -> ## Order Form): referenced file {of_val!r} does not exist")
    issues_body = shift_headings_up(ch_map["Open Issues"])
    validate_open_issues_body(issues_body, f"{r} (# Open Issues)", findings)
    if "None" in client_body and ch_map["Open Issues"].strip().endswith("None"):
        findings.append(f"WARN  {r}: # Client contains None sections; setup-client will add them to the Setup Ledger")
    return 1


def lint_client_folder(folder: Path, slug: str, findings: list[str], docs_headers: dict[str, dict[str, str]]) -> int:
    count = 0
    required_files = [("client.md", "client", validate_client_body), ("open-issues.md", "open-issues", None)]
    for filename, fmt, _ in required_files:
        p = folder / filename
        r = rel(p)
        if not p.is_file():
            findings.append(f"ERROR {r}: required client document missing")
            continue
        count += 1
        header, body = parse_header_and_body(p, r, fmt, slug, findings)
        docs_headers[r] = header
        if fmt == "client":
            validate_client_body(body, r, folder, findings)
        elif fmt == "open-issues":
            validate_open_issues_body(body, r, findings)
    for stray in sorted(folder.glob("*.md")):
        if stray.name not in {"client.md", "open-issues.md"}:
            findings.append(f"ERROR {rel(stray)}: file name does not mirror a registered client format")
    return count


def check_staged(docs_headers: dict[str, dict[str, str]], findings: list[str]) -> None:
    try:
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=M"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
    except Exception as e:
        findings.append(f"WARN  --staged: could not read git index ({e})")
        return
    for r in staged:
        if r not in docs_headers:
            continue
        try:
            old_text = subprocess.run(
                ["git", "show", f"HEAD:{r}"], cwd=ROOT, capture_output=True, text=True, check=True
            ).stdout
        except subprocess.CalledProcessError:
            continue
        old_m = FRONT_MATTER_RE.match(old_text)
        if not old_m:
            continue
        old_h: dict[str, str] = {}
        for line in old_m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                old_h[k.strip()] = v.strip()
        new_h = docs_headers[r]
        if old_h.get("updated") == new_h.get("updated") and old_h.get("updated_by") == new_h.get("updated_by"):
            findings.append(f"ERROR {r}: modified in git index but updated/updated_by did not change")


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    findings: list[str] = []
    docs_headers: dict[str, dict[str, str]] = {}
    checked = 0

    if "--handoff" in flags:
        if not args or not Path(args[0]).is_file():
            print("ERROR --handoff requires a path to an existing handoff Markdown file")
            return 1
        checked += lint_handoff(Path(args[0]).resolve(), findings)
    elif args:
        slug = args[0]
        folder = CLIENTS_DIR / slug
        if not folder.is_dir():
            print(f"ERROR clients/{slug}: no such client folder")
            return 1
        checked += lint_client_folder(folder, slug, findings, docs_headers)
    else:
        checked += check_global_context(findings)
        checked += check_formats_dir(findings)
        checked += check_processes_dir(findings)
        checked += check_inventories(findings)
        if CLIENTS_DIR.is_dir():
            for folder in sorted(p for p in CLIENTS_DIR.iterdir() if p.is_dir()):
                checked += lint_client_folder(folder, folder.name, findings, docs_headers)

    if "--staged" in flags:
        check_staged(docs_headers, findings)

    for f in sorted(findings, key=lambda s: (not s.startswith("ERROR"), s)):
        print(f)
    errors = sum(1 for f in findings if f.startswith("ERROR"))
    warns = len(findings) - errors
    print(f"{checked} document(s) checked: {errors} error(s), {warns} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
