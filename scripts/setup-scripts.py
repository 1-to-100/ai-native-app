#!/usr/bin/env python3
"""Configure and verify skill exposure for the repository's target AI environment.

Usage:
  python3 scripts/setup-scripts.py                        # wire for the vendor in AGENTS.md
  python3 scripts/setup-scripts.py --env claude|openai|gemini
  python3 scripts/setup-scripts.py --check                # report only; exit 1 on any problem

The source of truth for skills is `.agents/skills/<name>/SKILL.md`.
This script never edits a skill or a governed document; it only manages
vendor discovery symlinks (`.claude/skills/`, `.gemini/skills/`, `GEMINI.md`).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_SRC = ROOT / ".agents" / "skills"
CLAUDE_SKILLS = ROOT / ".claude" / "skills"
GEMINI_SKILLS = ROOT / ".gemini" / "skills"
GEMINI_MD = ROOT / "GEMINI.md"
AGENTS_MD = ROOT / "AGENTS.md"

FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
VENDOR_MAP = {"claude": "Claude", "openai": "OpenAI", "gemini": "Gemini"}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def detect_vendor_from_agents_md() -> tuple[str | None, list[str]]:
    if not AGENTS_MD.is_file():
        return None, ["AGENTS.md is missing at the repository root"]
    text = AGENTS_MD.read_text(encoding="utf-8")
    m = re.search(r"^## Vendor\n+([^\n#]+)", text, re.M)
    if not m:
        return None, ["AGENTS.md: missing '## Vendor' under '# Target AI Environment'"]
    val = m.group(1).strip().lower()
    if val not in VENDOR_MAP:
        return None, [f"AGENTS.md: unknown Vendor {m.group(1).strip()!r} (expected Claude, OpenAI, or Gemini)"]
    return val, []


def discover_skills() -> tuple[list[str], list[str]]:
    names: list[str] = []
    problems: list[str] = []
    if not SKILLS_SRC.is_dir():
        return names, [f"missing skills directory: {rel(SKILLS_SRC)}"]
    for folder in sorted(p for p in SKILLS_SRC.iterdir() if p.is_dir()):
        skill_md = folder / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"{rel(folder)}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(text)
        if not match:
            problems.append(f"{rel(skill_md)}: missing YAML front matter")
            continue
        fields: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fields[k.strip()] = v.strip()
        if fields.get("name") != folder.name:
            problems.append(
                f"{rel(skill_md)}: front matter name {fields.get('name')!r} does not match folder {folder.name!r}"
            )
        if not fields.get("description"):
            problems.append(f"{rel(skill_md)}: front matter missing description")
        names.append(folder.name)
    return names, problems


def sync_symlink_dir(target_dir: Path, names: list[str], prefix: str, check: bool) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    problems: list[str] = []
    if not check:
        target_dir.mkdir(parents=True, exist_ok=True)
    elif not target_dir.is_dir():
        problems.append(f"missing directory: {rel(target_dir)}")
        return lines, problems

    for name in names:
        link = target_dir / name
        expected_target = os.path.relpath(SKILLS_SRC / name, target_dir)
        if link.is_symlink():
            state = "ok" if os.readlink(link) == expected_target else "wrong-target"
        else:
            state = "not-a-symlink" if link.exists() else "missing"

        if state == "ok":
            lines.append(f"  ok       {prefix}{name}  ->  {expected_target}")
        elif state == "not-a-symlink":
            problems.append(f"{rel(link)} exists and is not a symlink")
        elif check:
            problems.append(f"{rel(link)}: {state}")
        else:
            if state == "wrong-target":
                link.unlink()
            link.symlink_to(expected_target, target_is_directory=True)
            lines.append(f"  linked   {prefix}{name}  ->  {expected_target}")

    if target_dir.is_dir():
        for link in sorted(target_dir.iterdir()):
            if not link.is_symlink() or link.name in names:
                continue
            resolved = (target_dir / os.readlink(link)).resolve()
            if SKILLS_SRC.resolve() in resolved.parents:
                if check:
                    problems.append(f"{rel(link)}: stale symlink")
                else:
                    link.unlink()
                    lines.append(f"  removed  {rel(link)} (stale)")
    return lines, problems


def main(argv: list[str]) -> int:
    check = False
    env_override: str | None = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--check":
            check = True
            i += 1
        elif arg == "--env" and i + 1 < len(argv):
            env_override = argv[i + 1].lower()
            i += 2
        else:
            print(__doc__)
            return 2

    if env_override and env_override not in VENDOR_MAP:
        print(f"ERROR unknown --env {env_override!r}; expected claude, openai, or gemini")
        return 2

    names, problems = discover_skills()
    detected_vendor, vendor_problems = detect_vendor_from_agents_md()
    problems += vendor_problems
    vendor = env_override or detected_vendor or "claude"

    print(f"Target AI environment: {VENDOR_MAP.get(vendor, vendor)}")
    print(f"Skills in {rel(SKILLS_SRC)}: {', '.join(names) if names else 'none'}")

    if vendor == "claude":
        print("\nClaude Code (.claude/skills):")
        lines, more = sync_symlink_dir(CLAUDE_SKILLS, names, "/", check)
        print("\n".join(lines))
        problems += more
    elif vendor == "openai":
        print("\nOpenAI Codex (.agents/skills):")
        for name in names:
            print(f"  ok       ${name}  ({rel(SKILLS_SRC / name / 'SKILL.md')})")
        print("  .agents/skills and AGENTS.md are OpenAI Codex's native locations")
    elif vendor == "gemini":
        print("\nGemini (.gemini/skills & GEMINI.md):")
        lines, more = sync_symlink_dir(GEMINI_SKILLS, names, "@", check)
        if GEMINI_MD.is_symlink() and os.readlink(GEMINI_MD) == "AGENTS.md":
            lines.append("  ok       GEMINI.md  ->  AGENTS.md")
        elif check:
            more.append("GEMINI.md symlink to AGENTS.md is missing")
        else:
            if GEMINI_MD.exists() or GEMINI_MD.is_symlink():
                GEMINI_MD.unlink()
            GEMINI_MD.symlink_to("AGENTS.md")
            lines.append("  linked   GEMINI.md  ->  AGENTS.md")
        print("\n".join(lines))
        problems += more

    if problems:
        print("\nProblems:")
        for p in problems:
            print(f"  ERROR {p}")
        return 1

    print(f"\nAll skills are configured for {VENDOR_MAP[vendor]}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
