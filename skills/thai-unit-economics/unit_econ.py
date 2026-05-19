"""unit_econ.py — CAC/LTV/payback calculator ด้วย Thai 2026 benchmarks.

อัตราใน BENCHMARKS อ้างอิงปี 2026 จาก Tellscore, AnyMind, MEDIA Z published reports.
"""
from __future__ import annotations

from decimal import Decimal as D, ROUND_HALF_UP

# CPM = cost per 1,000 impressions (THB)
# Flat fees ใน KOL — แสดงเป็น tuple (low, high)
BENCHMARKS_2026: dict[str, dict[str, tuple[D, D]]] = {
    "meta_cpm": {
        "beauty": (D("180"), D("320")),
        "fashion": (D("120"), D("220")),
        "food_delivery": (D("80"), D("180")),
        "electronics": (D("150"), D("280")),
        "general": (D("100"), D("250")),
    },
    "tiktok_cpm": {
        "beauty": (D("150"), D("280")),
        "fashion": (D("100"), D("200")),
        "food_delivery": (D("60"), D("150")),
        "general": (D("90"), D("220")),
    },
    "line_oa_push_per_msg": {
        "broadcast": (D("0.20"), D("0.30")),
    },
    "kol_flat_per_post": {
        "koc_nano": (D("800"), D("3000")),
        "micro": (D("8000"), D("35000")),
        "mid": (D("50000"), D("250000")),
        "macro": (D("300000"), D("1500000")),
    },
}


def cac(total_spend: D, new_customers: int) -> D:
    """CAC = total spend ÷ จำนวนลูกค้าใหม่."""
    if new_customers <= 0:
        raise ValueError("จำนวนลูกค้าใหม่ต้อง > 0")
    return (total_spend / D(new_customers)).quantize(
        D("0.01"), rounding=ROUND_HALF_UP
    )


def ltv(
    aov: D,
    purchases_per_year: D,
    gross_margin_rate: D,
    customer_lifetime_years: D = D("1"),
) -> D:
    """LTV = AOV × purchases/yr × margin × lifetime.

    customer_lifetime_years default 1 = "ปีเดียว" — สำหรับ SME ไทยที่ retention สั้น
    ใช้ค่า conservative.
    """
    if not (D("0") < gross_margin_rate < D("1")):
        raise ValueError("gross_margin_rate ต้องอยู่ระหว่าง 0 ถึง 1")
    return (
        aov * purchases_per_year * gross_margin_rate * customer_lifetime_years
    ).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def payback_transactions(cac_value: D, aov: D, gross_margin_rate: D) -> D:
    """payback period as จำนวน transactions เพื่อกินคืน CAC."""
    contribution_per_tx = aov * gross_margin_rate
    if contribution_per_tx <= 0:
        raise ValueError("contribution per transaction ต้อง > 0")
    return (cac_value / contribution_per_tx).quantize(
        D("0.01"), rounding=ROUND_HALF_UP
    )


def ratio_ltv_cac(ltv_value: D, cac_value: D) -> D:
    if cac_value <= 0:
        raise ValueError("CAC ต้อง > 0")
    return (ltv_value / cac_value).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def assess(ltv_cac_ratio: D, payback_tx: D) -> list[str]:
    """ผลิตข้อสังเกตเชิงประเมิน — caller ตัดสินใจว่าจะแสดงไหม."""
    notes: list[str] = []
    if ltv_cac_ratio < D("1"):
        notes.append("LTV:CAC < 1 — ขาดทุนจากการ acquisition ทุกราย, ต้องหยุดสเกล")
    elif ltv_cac_ratio < D("3"):
        notes.append(
            f"LTV:CAC = {ltv_cac_ratio} (ควร > 3) — ลด CAC หรือเพิ่ม retention/AOV"
        )
    else:
        notes.append(f"LTV:CAC = {ltv_cac_ratio} — healthy")
    if payback_tx > D("4"):
        notes.append(
            f"Payback {payback_tx} transactions เกิน 4 — cashflow trap, ต้องดู runway"
        )
    return notes


def _self_test() -> None:
    # case: ครีม COGS 85, ขาย 250, ad spend 30k, ได้ลูกค้าใหม่ 38
    c = cac(D("30000"), 38)
    assert D("789") <= c <= D("790"), f"CAC unexpected: {c}"
    print(f"  ✓ CAC = {c}")

    # gross margin (ไม่รวม fee = 1.0) ที่ 60%
    l = ltv(D("250"), D("1.4"), D("0.60"))
    # 250 * 1.4 * 0.6 * 1 = 210
    assert l == D("210.00"), f"LTV unexpected: {l}"
    print(f"  ✓ LTV = {l}")

    p = payback_transactions(c, D("250"), D("0.60"))
    # 789.47 / 150 = 5.26
    assert D("5") < p < D("6"), f"payback unexpected: {p}"
    print(f"  ✓ Payback = {p} transactions")

    r = ratio_ltv_cac(l, c)
    # 210 / 789.47 = 0.27
    assert D("0.26") < r < D("0.28"), f"ratio unexpected: {r}"
    print(f"  ✓ LTV:CAC = {r}")

    notes = assess(r, p)
    assert any("unhealthy" not in n for n in notes)  # notes returned
    assert len(notes) >= 1
    print(f"  ✓ assess produced {len(notes)} note(s)")

    # error case
    try:
        cac(D("100"), 0)
    except ValueError:
        print("  ✓ cac(0 customers) raises")
    else:
        raise AssertionError("expected ValueError")


if __name__ == "__main__":
    _self_test()
    print("unit_econ.py — all tests passed")
