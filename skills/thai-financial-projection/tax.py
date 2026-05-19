"""tax.py — Thai SME corporate income tax + SSO calculator.

อัตราอ้างอิงปี 2026 ตามประมวลรัษฎากร + พรฎ. SME.
"""
from __future__ import annotations

from decimal import Decimal as D, ROUND_HALF_UP

# SME eligibility (ทุน ≤5M และรายได้ ≤30M)
SME_PAID_UP_CAP = D("5000000")
SME_REVENUE_CAP = D("30000000")

# SME tier brackets (2026)
SME_BRACKETS: list[tuple[D, D, D]] = [
    # (lower_bound, upper_bound, rate)
    (D("0"), D("300000"), D("0.00")),
    (D("300000"), D("3000000"), D("0.15")),
    (D("3000000"), D("999999999"), D("0.20")),
]

CORPORATE_TAX_FLAT = D("0.20")

# VAT
VAT_THRESHOLD = D("1800000")
VAT_RATE = D("0.07")

# SSO 2026
SSO_BASE_CAP_MONTHLY = D("15000")
SSO_EMPLOYER_RATE = D("0.05")
SSO_EMPLOYEE_RATE = D("0.05")


def is_sme(paid_up_capital: D, gross_revenue: D) -> bool:
    """SME ต้องเข้าทั้ง 2 เกณฑ์ — ทุนชำระ ≤5M และรายได้ ≤30M."""
    return paid_up_capital <= SME_PAID_UP_CAP and gross_revenue <= SME_REVENUE_CAP


def sme_corporate_tax(net_profit: D, paid_up_capital: D, gross_revenue: D) -> D:
    """คำนวน corporate income tax. ถ้าไม่ใช่ SME ใช้ flat 20%."""
    if net_profit <= 0:
        return D("0")
    if not is_sme(paid_up_capital, gross_revenue):
        return (net_profit * CORPORATE_TAX_FLAT).quantize(
            D("0.01"), rounding=ROUND_HALF_UP
        )
    # SME — apply progressive brackets
    tax = D("0")
    for lower, upper, rate in SME_BRACKETS:
        if net_profit <= lower:
            break
        taxable_in_bracket = min(net_profit, upper) - lower
        tax += taxable_in_bracket * rate
    return tax.quantize(D("0.01"), rounding=ROUND_HALF_UP)


def sso_monthly_contribution(salary: D, side: str = "both") -> D:
    """SSO contribution ต่อเดือน. base capped ที่ 15,000.

    side: "employer" | "employee" | "both"
    """
    base = min(salary, SSO_BASE_CAP_MONTHLY)
    if side == "employer":
        return (base * SSO_EMPLOYER_RATE).quantize(D("0.01"))
    if side == "employee":
        return (base * SSO_EMPLOYEE_RATE).quantize(D("0.01"))
    if side == "both":
        return (
            base * (SSO_EMPLOYER_RATE + SSO_EMPLOYEE_RATE)
        ).quantize(D("0.01"))
    raise ValueError(f"side must be employer | employee | both, got {side!r}")


def sso_annual_employer(employees: list[D]) -> D:
    """รวม SSO ฝั่งนายจ้างต่อปีจาก list ของเงินเดือนต่อคน."""
    total = D("0")
    for s in employees:
        total += sso_monthly_contribution(s, "employer") * D("12")
    return total.quantize(D("0.01"))


def vat_status(annual_revenue: D) -> str:
    """ตรวจว่ารายได้เกิน VAT threshold หรือยัง.

    ตามมาตรา 81/1 ประมวลรัษฎากร: ต้องจดเมื่อรายรับ "เกิน" 1.8M (strict >),
    ที่ 1.8M พอดียังไม่ trigger.
    """
    if annual_revenue > VAT_THRESHOLD:
        return f"ต้องจด VAT — รายได้ {annual_revenue:,} เกิน {VAT_THRESHOLD:,}"
    return f"ยังไม่ต้องจด VAT — รายได้ {annual_revenue:,} ยังไม่เกิน {VAT_THRESHOLD:,}"


def _self_test() -> None:
    # case 1: SME ปกติ, net profit 500k
    # tier: 0% on 300k + 15% on 200k = 30,000
    tax = sme_corporate_tax(D("500000"), D("1000000"), D("3000000"))
    assert tax == D("30000.00"), f"500k profit unexpected: {tax}"
    print(f"  ✓ SME net 500k → tax {tax}")

    # case 2: SME, net profit 3.5M
    # 0% on 300k + 15% on 2.7M + 20% on 500k = 0 + 405,000 + 100,000 = 505,000
    tax2 = sme_corporate_tax(D("3500000"), D("2000000"), D("10000000"))
    assert tax2 == D("505000.00"), f"3.5M profit unexpected: {tax2}"
    print(f"  ✓ SME net 3.5M → tax {tax2}")

    # case 3: not SME (revenue > 30M)
    # flat 20% on 5M = 1,000,000
    tax3 = sme_corporate_tax(D("5000000"), D("1000000"), D("35000000"))
    assert tax3 == D("1000000.00"), f"non-SME 5M unexpected: {tax3}"
    print(f"  ✓ non-SME (rev>30M) net 5M → tax {tax3} (flat 20%)")

    # case 4: SSO ลูกจ้างเงินเดือน 22k (เกิน cap 15k) — employer 750
    e = sso_monthly_contribution(D("22000"), "employer")
    assert e == D("750.00"), f"sso employer 22k unexpected: {e}"
    print(f"  ✓ SSO employer @22k salary → {e}/month")

    # case 5: SSO 6 คน เงินเดือน 22k each, ทั้งปี employer = 750 × 12 × 6 = 54,000
    annual = sso_annual_employer([D("22000")] * 6)
    assert annual == D("54000.00"), f"annual SSO unexpected: {annual}"
    print(f"  ✓ SSO annual 6 employees @22k → {annual}")

    # case 6: VAT
    s = vat_status(D("2400000"))
    assert "ต้องจด" in s, f"vat status unexpected: {s}"
    print(f"  ✓ VAT @2.4M revenue → {s}")

    # case 6b: VAT boundary — exactly 1.8M is NOT a trigger (มาตรา 81/1: "เกิน" = strict >)
    s_boundary = vat_status(VAT_THRESHOLD)
    assert "ยังไม่ต้อง" in s_boundary, f"1.8M boundary should not trigger: {s_boundary}"
    print(f"  ✓ VAT @1.8M exactly → {s_boundary}")

    # case 7: loss → no tax
    assert sme_corporate_tax(D("-50000"), D("1000000"), D("5000000")) == D("0")
    print("  ✓ loss → no tax")


if __name__ == "__main__":
    _self_test()
    print("tax.py — all tests passed")
