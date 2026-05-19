#!/usr/bin/env bash
# scripts/test-all.sh — รัน self-test ของทุก skill + frontmatter validator
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Validating SKILL.md frontmatter ==="
python3 scripts/validate-skills.py

echo
echo "=== Running Python helper self-tests ==="
HELPERS=(
  "skills/thai-pricing-strategy/pricing.py"
  "skills/thai-unit-economics/unit_econ.py"
  "skills/thai-financial-projection/tax.py"
  "skills/thai-influencer-deal/commission.py"
  "skills/thai-sourcing-landed-cost/landed_cost.py"
  "skills/thai-cashflow-survival/cashflow.py"
)

failed=0
for helper in "${HELPERS[@]}"; do
  if [[ -f "$helper" ]]; then
    echo "→ $helper"
    if python3 "$helper"; then
      echo "  ✓ pass"
    else
      echo "  ✗ FAIL"
      failed=$((failed + 1))
    fi
  fi
done

if [[ $failed -gt 0 ]]; then
  echo
  echo "✗ $failed test(s) failed"
  exit 1
fi

echo
echo "✓ all tests passed"
