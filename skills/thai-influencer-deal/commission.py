"""commission.py — KOL/KOC payout calculator with Thai WHT.

อ้างอิงประมวลรัษฎากร 2026 มาตรา 50, 70.
"""
from __future__ import annotations

from decimal import Decimal as D, ROUND_HALF_UP

VAT_RATE = D("0.07")

# WHT rates by residence (for service fees / talent fees)
WHT_RATES: dict[str, D] = {
    "thai": D("0.03"),                    # บุคคล/นิติบุคคลในประเทศ
    "non_resident_dta_low": D("0.05"),    # มี DTA, ค่าบริการทั่วไป
    "non_resident_no_dta": D("0.15"),     # ไม่มี DTA, มาตรา 70
}

WHT_THRESHOLD_PER_PAYMENT = D("1000")  # ต่ำกว่านี้ไม่หัก (per occurrence)


def wht_rate(residence: str) -> D:
    if residence not in WHT_RATES:
        raise ValueError(
            f"residence must be one of {list(WHT_RATES)}, got {residence!r}"
        )
    return WHT_RATES[residence]


def compute_payout(
    talent_fee: D,
    affiliate_revenue: D,
    residence: str,
    kol_vat_registered: bool,
) -> dict[str, D]:
    """คำนวน cost ฝั่ง brand + net payout ฝั่ง KOL.

    talent_fee: ค่าตัว flat (ก่อน VAT, ก่อน WHT)
    affiliate_revenue: รายได้จาก revenue share (ถ้ามี — เป็นจำนวนเงินที่คำนวนแล้วจาก GMV × rate)
    residence: "thai" | "non_resident_dta_low" | "non_resident_no_dta"
    """
    gross = talent_fee + affiliate_revenue
    rate = wht_rate(residence)

    # WHT base = gross fee ก่อน VAT
    wht_amount = D("0")
    if gross >= WHT_THRESHOLD_PER_PAYMENT:
        wht_amount = (gross * rate).quantize(D("0.01"), rounding=ROUND_HALF_UP)

    vat = D("0")
    if kol_vat_registered:
        vat = (gross * VAT_RATE).quantize(D("0.01"), rounding=ROUND_HALF_UP)

    # Brand pays: gross + VAT, then withholds WHT
    # KOL receives: gross + VAT - WHT
    # Brand net cash out = gross + VAT - WHT (cash out), then remits WHT to RD = + WHT
    # = gross + VAT
    # Brand's expense (deductible) = gross
    # Brand's VAT credit = VAT (claim back on ภพ.30)
    # Brand's effective cost = gross
    cash_to_kol = gross + vat - wht_amount
    brand_cash_out = gross + vat  # to KOL + to RD (WHT)
    brand_effective_cost = gross  # after VAT credit

    return {
        "gross_fee": gross,
        "vat_added": vat,
        "wht_withheld": wht_amount,
        "cash_to_kol": cash_to_kol.quantize(D("0.01")),
        "brand_total_cash_out": brand_cash_out.quantize(D("0.01")),
        "brand_effective_cost": brand_effective_cost.quantize(D("0.01")),
        "wht_rate_applied": rate,
    }


def _self_test() -> None:
    # case 1: Thai KOL, jdvat, talent fee 350k, no affiliate
    r = compute_payout(D("350000"), D("0"), "thai", True)
    # WHT 3% = 10,500
    # VAT 7% = 24,500
    # cash to KOL = 350,000 + 24,500 - 10,500 = 364,000
    # brand cash out total = 374,500
    # brand effective cost = 350,000 (VAT credit back)
    assert r["wht_withheld"] == D("10500.00"), r
    assert r["vat_added"] == D("24500.00"), r
    assert r["cash_to_kol"] == D("364000.00"), r
    assert r["brand_total_cash_out"] == D("374500.00"), r
    assert r["brand_effective_cost"] == D("350000.00"), r
    print(f"  ✓ Thai VAT-reg KOL 350k → cash {r['cash_to_kol']}, brand cost {r['brand_effective_cost']}")

    # case 2: Thai KOC, no VAT registration, talent 800 → below threshold
    r2 = compute_payout(D("800"), D("0"), "thai", False)
    assert r2["wht_withheld"] == D("0"), f"sub-1000 should not withhold: {r2}"
    assert r2["vat_added"] == D("0"), r2
    assert r2["cash_to_kol"] == D("800.00"), r2
    print(f"  ✓ KOC 800 (below threshold) → cash {r2['cash_to_kol']}")

    # case 3: Thai KOL no VAT, talent 5000
    r3 = compute_payout(D("5000"), D("0"), "thai", False)
    # WHT 3% = 150, no VAT
    # cash to KOL = 5000 - 150 = 4850
    # brand cash out = 5000
    assert r3["wht_withheld"] == D("150.00"), r3
    assert r3["cash_to_kol"] == D("4850.00"), r3
    assert r3["brand_total_cash_out"] == D("5000.00"), r3
    print(f"  ✓ Thai non-VAT KOL 5000 → cash {r3['cash_to_kol']}")

    # case 4: non-resident no DTA, 100k
    r4 = compute_payout(D("100000"), D("0"), "non_resident_no_dta", False)
    # WHT 15% = 15,000
    assert r4["wht_withheld"] == D("15000.00"), r4
    assert r4["cash_to_kol"] == D("85000.00"), r4
    print(f"  ✓ Non-resident no DTA 100k → WHT {r4['wht_withheld']}, cash {r4['cash_to_kol']}")

    # case 5: combined talent + affiliate
    r5 = compute_payout(D("50000"), D("23000"), "thai", True)
    gross = D("73000")
    assert r5["gross_fee"] == gross, r5
    # WHT 3% = 2190
    # VAT 7% = 5110
    # cash to KOL = 73000 + 5110 - 2190 = 75920
    assert r5["wht_withheld"] == D("2190.00"), r5
    assert r5["cash_to_kol"] == D("75920.00"), r5
    print(f"  ✓ Talent+affiliate 73000 → cash {r5['cash_to_kol']}")

    # error: bad residence
    try:
        compute_payout(D("1000"), D("0"), "bogus", False)
    except ValueError:
        print("  ✓ bogus residence raises")
    else:
        raise AssertionError("expected ValueError")


if __name__ == "__main__":
    _self_test()
    print("commission.py — all tests passed")
