"""pricing.py — Waterfall pricing calculator สำหรับ Thai marketplace channels.

ใช้ Decimal ไม่ใช่ float เพื่อไม่ให้ rounding หลุดสตางค์.
อัตราในไฟล์นี้อ้างอิงปี 2026 — ดู benchmarks.md สำหรับ source.
"""
from __future__ import annotations

from decimal import Decimal as D, ROUND_HALF_UP

# 2026 marketplace fees (middle-of-range estimates)
# commission = marketplace cut, gateway = payment/transaction fee
# (เปลี่ยนตัวเลขที่นี่ตรงๆ เมื่อ marketplace ปรับนโยบาย)
CHANNELS: dict[str, dict[str, D]] = {
    "Shopee Mall": {
        "commission": D("0.065"),
        "gateway": D("0.032"),
    },
    "Shopee (non-Mall)": {
        "commission": D("0.045"),
        "gateway": D("0.032"),
    },
    "Lazada Mall": {
        "commission": D("0.06"),
        "gateway": D("0.03"),
    },
    "Lazada (non-Mall)": {
        "commission": D("0.04"),
        "gateway": D("0.03"),
    },
    "TikTok Shop (beauty)": {
        "commission": D("0.05"),
        "gateway": D("0.024"),
    },
    "TikTok Shop (fashion)": {
        "commission": D("0.04"),
        "gateway": D("0.024"),
    },
    "TikTok Shop (electronics)": {
        "commission": D("0.02"),
        "gateway": D("0.024"),
    },
    "LINE Shopping": {
        "commission": D("0.04"),
        "gateway": D("0.024"),
    },
    "หน้าร้าน (offline cash)": {
        "commission": D("0"),
        "gateway": D("0"),
    },
    "หน้าร้าน (offline card)": {
        "commission": D("0"),
        "gateway": D("0.02"),
    },
}


def fee_rate(channel: str) -> D:
    """รวม fee ของ channel (commission + gateway) เป็น % ของราคาขาย."""
    cfg = CHANNELS[channel]
    return cfg["commission"] + cfg["gateway"]


def required_price(
    cogs: D,
    packaging: D,
    shipping_out: D,
    target_margin: D,
    channel: str,
) -> D:
    """ราคาขายขั้นต่ำเพื่อให้กำไรขั้นต้น = target_margin ของราคาขาย.

    Margin model:
        margin = (price * (1 - fee) - cogs - packaging - shipping_out) / price
    Solve for price:
        price * (1 - fee - margin) = cogs + packaging + shipping_out
    """
    fee = fee_rate(channel)
    denom = D("1") - fee - target_margin
    if denom <= 0:
        raise ValueError(
            f"target margin {target_margin} ทำไม่ได้ใน {channel} "
            f"(รวม fee {fee} + margin {target_margin} ≥ 100%)"
        )
    fixed_costs = cogs + packaging + shipping_out
    price = fixed_costs / denom
    return price.quantize(D("0.01"), rounding=ROUND_HALF_UP)


def gross_profit(
    price: D,
    cogs: D,
    packaging: D,
    shipping_out: D,
    channel: str,
) -> tuple[D, D]:
    """คืน (กำไรขั้นต้น ฿, margin %) ที่ราคาขายที่ระบุ."""
    fee = fee_rate(channel)
    revenue_after_fee = price * (D("1") - fee)
    profit = revenue_after_fee - cogs - packaging - shipping_out
    margin = profit / price if price > 0 else D("0")
    return (
        profit.quantize(D("0.01"), rounding=ROUND_HALF_UP),
        margin.quantize(D("0.0001"), rounding=ROUND_HALF_UP),
    )


def _self_test() -> None:
    """รัน self-test — assertions ต้องผ่านทุกข้อ."""
    # case 1: Shopee Mall, COGS 85, pack 8, ship 0, target 35%
    # fee = 0.065 + 0.032 = 0.097
    # denom = 1 - 0.097 - 0.35 = 0.553
    # fixed = 93
    # price = 93 / 0.553 = 168.18
    price = required_price(D("85"), D("8"), D("0"), D("0.35"), "Shopee Mall")
    assert D("167") < price < D("170"), f"shopee mall price unexpected: {price}"
    print(f"  ✓ Shopee Mall COGS 85: price = {price}")

    # case 2: หน้าร้าน cash, no fees, target 35%
    # denom = 1 - 0 - 0.35 = 0.65
    # price = 93 / 0.65 = 143.08
    price2 = required_price(
        D("85"), D("8"), D("0"), D("0.35"), "หน้าร้าน (offline cash)"
    )
    assert D("142") < price2 < D("145"), f"offline price unexpected: {price2}"
    print(f"  ✓ Offline cash COGS 85: price = {price2}")

    # case 3: gross_profit reverse calc
    profit, margin = gross_profit(D("168.18"), D("85"), D("8"), D("0"), "Shopee Mall")
    # at 168.18, revenue after 9.7% fee = 151.87, profit = 151.87 - 93 = 58.87
    # margin = 58.87 / 168.18 = 0.3501
    assert D("58") < profit < D("60"), f"profit unexpected: {profit}"
    assert D("0.34") < margin < D("0.36"), f"margin unexpected: {margin}"
    print(f"  ✓ gross_profit reverse: profit={profit}, margin={margin}")

    # case 4: impossible margin should raise
    try:
        required_price(D("100"), D("0"), D("0"), D("0.95"), "Shopee Mall")
    except ValueError:
        print("  ✓ impossible margin raises ValueError")
    else:
        raise AssertionError("expected ValueError for 95% margin on Shopee Mall")


if __name__ == "__main__":
    _self_test()
    print("pricing.py — all tests passed")
