#!/usr/bin/env python3
"""Validate frontmatter ของ SKILL.md ทุกตัวใน skills/*/SKILL.md

ตรวจ:
  - มีไฟล์ SKILL.md
  - มี YAML frontmatter ระหว่าง --- ... ---
  - มี keys ที่จำเป็น: name, description, when_to_use, version, last_verified, tier
  - tier เป็นหนึ่งใน: validator, reference, prose
  - name ตรงกับชื่อ directory
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_KEYS = {
    "name",
    "description",
    "when_to_use",
    "version",
    "last_verified",
    "tier",
}
VALID_TIERS = {"validator", "reference", "prose"}

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


def parse_frontmatter(text: str) -> dict | None:
    """รับ raw markdown text — return dict ของ frontmatter หรือ None ถ้าไม่มี."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    block = m.group(1)
    data: dict[str, object] = {}
    current_list_key: str | None = None
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            current_list_key = None
            continue
        # list item
        if line.lstrip().startswith("- ") and current_list_key:
            data.setdefault(current_list_key, [])
            value = line.lstrip()[2:].strip()
            data[current_list_key].append(value)  # type: ignore[union-attr]
            continue
        # key: value
        m2 = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if not m2:
            continue
        key, value = m2.group(1), m2.group(2).strip()
        if value == "":
            current_list_key = key
            continue
        # strip quotes
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        data[key] = value
        current_list_key = None
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    name = skill_dir.name
    if not skill_file.exists():
        return [f"[{name}] missing SKILL.md"]
    text = skill_file.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"[{name}] no YAML frontmatter — must start with '---'"]
    missing = REQUIRED_KEYS - set(fm.keys())
    if missing:
        errors.append(f"[{name}] missing frontmatter keys: {sorted(missing)}")
    if fm.get("name") != name:
        errors.append(
            f"[{name}] frontmatter name='{fm.get('name')}' does not match directory"
        )
    tier = fm.get("tier")
    if tier not in VALID_TIERS:
        errors.append(
            f"[{name}] tier='{tier}' must be one of {sorted(VALID_TIERS)}"
        )
    when = fm.get("when_to_use")
    if not isinstance(when, list) or len(when) == 0:
        errors.append(f"[{name}] when_to_use must be a non-empty list")
    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"  ✗ no skills/ directory at {SKILLS_DIR}", file=sys.stderr)
        return 1
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    total_errors: list[str] = []
    for d in skill_dirs:
        errs = validate_skill(d)
        if errs:
            for e in errs:
                print(f"  ✗ {e}")
            total_errors.extend(errs)
        else:
            print(f"  ✓ {d.name}")
    print()
    if total_errors:
        print(f"  ✗ {len(total_errors)} error(s)", file=sys.stderr)
        return 1
    print(f"  ✓ all {len(skill_dirs)} skill(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
