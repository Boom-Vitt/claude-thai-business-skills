#!/usr/bin/env bash
# install.sh — copy skills เข้าไปที่ ~/.claude/skills/
# usage:
#   ./install.sh                          # ติดตั้งทุก skill
#   ./install.sh thai-pricing-strategy    # ติดตั้งเฉพาะตัว
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$TARGET"

if [[ $# -eq 0 ]]; then
  echo "→ ติดตั้งทุก skill ไปที่ $TARGET"
  for skill_dir in "$REPO_ROOT"/skills/*/; do
    name="$(basename "$skill_dir")"
    rm -rf "$TARGET/$name"
    cp -R "$skill_dir" "$TARGET/$name"
    echo "  ✓ $name"
  done
else
  for name in "$@"; do
    # ทุก user-supplied name ต้องผ่าน guard นี้ก่อนแตะ $TARGET
    if [[ ${#name} -gt 64 || ! "$name" =~ ^thai-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
      echo "  ✗ '$name' — ต้องเป็น thai-<word>(-<word>)* (a-z0-9), ≤ 64 ตัวอักษร (กัน path traversal)" >&2
      exit 1
    fi
    src="$REPO_ROOT/skills/$name"
    if [[ ! -d "$src" ]]; then
      echo "  ✗ $name — ไม่พบ skill (มีอยู่: $(ls "$REPO_ROOT/skills" | tr '\n' ' '))" >&2
      exit 1
    fi
    rm -rf "$TARGET/$name"
    cp -R "$src" "$TARGET/$name"
    echo "  ✓ $name"
  done
fi

echo "เสร็จแล้ว — ปิด/เปิด Claude Code session ใหม่ให้ skill โหลด."
