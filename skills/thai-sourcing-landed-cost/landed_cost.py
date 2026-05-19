"""landed_cost.py — Import landed cost + compliance flag calculator.

อ้างอิงปี 2026: customs.go.th, fda.moph.go.th, tisi.go.th, nbtc.go.th.
"""
from __future__ import annotations

from decimal import Decimal as D, ROUND_HALF_UP

VAT_RATE = D("0.07")

# Common HS categories (เลข 4 หลัก) — ใช้ MFN rate (ไม่ใช้ FTA discount)
# (description, mfn_duty_rate, compliance_flags)
HS_CATEGORIES: dict[str, dict] = {
    "3304": {
        "name": "Cosmetics (skincare, makeup)",
        "duty": D("0.20"),
        "compliance": ["FDA cosmetic notification (1-3 เดือน)"],
    },
    "2106": {
        "name": "Food supplement",
        "duty": D("0.20"),
        "compliance": [
            "FDA food registration (3-6 เดือน)",
            "อย. label ภาษาไทยบังคับ",
        ],
    },
    "8517": {
        "name": "Mobile/communication devices",
        "duty": D("0.0"),
        "compliance": [
            "NBTC type approval (30-60 วัน) สำหรับอุปกรณ์แพร่คลื่น",
            "บางรุ่น TISI/มอก. (charger)",
        ],
    },
    "8518": {
        "name": "Audio (headphones, speakers, microphones)",
        "duty": D("0.20"),
        "compliance": [
            "TISI/มอก. 2274-2549 (อิเล็กทรอนิกส์เสียง บางรุ่น)",
            "ถ้า bluetooth/wireless → NBTC type approval",
        ],
    },
    "6109": {
        "name": "T-shirts / knitwear",
        "duty": D("0.30"),
        "compliance": [],
    },
    "6204": {
        "name": "Women's outerwear",
        "duty": D("0.30"),
        "compliance": [],
    },
    "9503": {
        "name": "Toys",
        "duty": D("0.20"),
        "compliance": ["TISI 685-2540 (ของเล่นทุกประเภท) บังคับ"],
    },
    "4901": {
        "name": "Books",
        "duty": D("0.0"),
        "compliance": [],
    },
    "3926": {
        "name": "Plastic articles (phone cases, accessories)",
        "duty": D("0.20"),
        "compliance": [],
    },
    "9506": {
        "name": "Sports equipment",
        "duty": D("0.20"),
        "compliance": ["บางหมวด TISI (helmet, lifejacket)"],
    },
}


def compute_landed_cost(
    fob_per_unit_thb: D,
    shipping_per_unit_thb: D,
    hs_code: str,
    duty_rate_override: D | None = None,
) -> dict[str, D]:
    """คำนวน landed cost per unit.

    fob_per_unit_thb: ราคาต้นทาง converted แล้วเป็น THB
    shipping_per_unit_thb: shipping per unit (รวมประกัน) THB
    hs_code: HS 4 หลักที่ Match HS_CATEGORIES
    duty_rate_override: ถ้า user มี FTA cert หรือ duty rate พิเศษ ใส่เข้ามา
    """
    if hs_code not in HS_CATEGORIES:
        raise ValueError(
            f"unknown HS {hs_code} — ใช้ duty_rate_override หรือเพิ่มใน HS_CATEGORIES"
        )
    info = HS_CATEGORIES[hs_code]
    duty_rate = duty_rate_override if duty_rate_override is not None else info["duty"]

    cif = fob_per_unit_thb + shipping_per_unit_thb
    duty = (cif * duty_rate).quantize(D("0.01"), rounding=ROUND_HALF_UP)
    vat = ((cif + duty) * VAT_RATE).quantize(D("0.01"), rounding=ROUND_HALF_UP)
    total = (cif + duty + vat).quantize(D("0.01"), rounding=ROUND_HALF_UP)

    return {
        "fob": fob_per_unit_thb.quantize(D("0.01")),
        "shipping": shipping_per_unit_thb.quantize(D("0.01")),
        "cif": cif.quantize(D("0.01")),
        "duty_rate": duty_rate,
        "duty": duty,
        "vat_on_cif_duty": vat,
        "total_landed": total,
    }


def compliance_flags(hs_code: str) -> list[str]:
    """คืน list ของ compliance flag สำหรับ HS category นี้."""
    if hs_code not in HS_CATEGORIES:
        return [f"HS {hs_code} ไม่อยู่ใน lookup — ตรวจที่ tariff.customs.go.th"]
    return list(HS_CATEGORIES[hs_code]["compliance"])


def _self_test() -> None:
    # case 1: bluetooth headphones, FOB 900฿, shipping 55฿, HS 8518
    r = compute_landed_cost(D("900"), D("55"), "8518")
    # CIF = 955
    # duty 20% = 191
    # VAT 7% on (955+191=1146) = 80.22
    # total = 955 + 191 + 80.22 = 1226.22
    assert r["cif"] == D("955.00"), r
    assert r["duty"] == D("191.00"), r
    assert r["vat_on_cif_duty"] == D("80.22"), r
    assert r["total_landed"] == D("1226.22"), r
    print(f"  ✓ Bluetooth audio HS 8518 → landed {r['total_landed']}")

    # compliance
    flags = compliance_flags("8518")
    assert len(flags) == 2, flags
    print(f"  ✓ HS 8518 has {len(flags)} compliance flag(s)")

    # case 2: skincare HS 3304
    r2 = compute_landed_cost(D("400"), D("30"), "3304")
    # CIF 430, duty 20% = 86, VAT (430+86)*7% = 36.12, total = 552.12
    assert r2["duty"] == D("86.00"), r2
    assert r2["total_landed"] == D("552.12"), r2
    print(f"  ✓ Skincare HS 3304 → landed {r2['total_landed']}, flags: {compliance_flags('3304')}")

    # case 3: ASEAN FTA override (0% duty)
    r3 = compute_landed_cost(D("400"), D("30"), "6109", duty_rate_override=D("0"))
    # CIF 430, no duty, VAT 7% = 30.10, total = 460.10
    assert r3["duty"] == D("0"), r3
    assert r3["total_landed"] == D("460.10"), r3
    print(f"  ✓ T-shirt HS 6109 ASEAN FTA 0% → landed {r3['total_landed']}")

    # error
    try:
        compute_landed_cost(D("100"), D("10"), "9999")
    except ValueError:
        print("  ✓ unknown HS raises")
    else:
        raise AssertionError("expected ValueError for unknown HS")


if __name__ == "__main__":
    _self_test()
    print("landed_cost.py — all tests passed")
