"""cashflow.py — 90-day cashflow calendar with Thai tax/payroll timing.

Build a 90-day projection where standard Thai obligations (VAT, SSO, PND.1,
salary, rent) land on the right days.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal as D, ROUND_HALF_UP


@dataclass
class CashEvent:
    day_offset: int  # days from start_date
    label: str
    amount: D  # positive = inflow, negative = outflow


@dataclass
class CashflowSummary:
    opening_balance: D
    closing_balance: D
    low_point_balance: D
    low_point_day_offset: int
    total_inflows: D
    total_outflows: D
    events: list[CashEvent] = field(default_factory=list)


def standard_monthly_events(
    revenue_cash_per_month: D,
    salary_total: D,
    rent: D,
    utilities: D,
    marketing: D,
    cogs_pct_of_revenue: D,
    supplier_credit_days: int,
    vat_payable: D,
    months: int = 3,
) -> list[CashEvent]:
    """สร้าง list ของ CashEvent ตามแบบฉบับ SME ไทย ปกติ.

    แบบจำลองง่ายๆ:
    - Revenue เข้าทุก 7 วัน (เฉลี่ยทั้งเดือน) — 4 ครั้ง/เดือน
    - เงินเดือน + ค่าเช่า + utilities ออกวันที่ 1 ของเดือน
    - PND.1 + SSO + ภพ.30 ออกวันที่ 15 ของเดือนถัดไป
    - Supplier จ่ายตาม credit_days ของยอด COGS เดือนก่อน
    """
    events: list[CashEvent] = []
    revenue_weekly = revenue_cash_per_month / D("4")
    revenue_weekly = revenue_weekly.quantize(D("0.01"), rounding=ROUND_HALF_UP)
    cogs_monthly = (revenue_cash_per_month * cogs_pct_of_revenue).quantize(
        D("0.01"), rounding=ROUND_HALF_UP
    )

    # SSO employer (assume salary base capped — caller passes total salary, not capped)
    # rough: SSO employer = 5% of capped base. Without per-employee detail,
    # approximate at 5% of min(salary_total, n_employees * 15000)
    # caller can pass salary_total ที่ adjust ให้แล้ว — เราคิด SSO เป็น 5% ตรงๆ
    sso_monthly = (salary_total * D("0.05")).quantize(D("0.01"))
    # PND.1 (WHT employees) — depends on bracket. ใช้ rough 2% ของฐาน
    pnd1_monthly = (salary_total * D("0.02")).quantize(D("0.01"))

    for m in range(months):
        base = m * 30
        # weekly revenue inflows (day 7, 14, 21, 28)
        for w in (7, 14, 21, 28):
            events.append(CashEvent(base + w, f"Revenue M{m+1} W{w//7}", revenue_weekly))

        # day 1 of month: salary + rent + utilities + marketing (fixed costs)
        events.append(CashEvent(base + 1, f"Salary M{m+1}", -salary_total))
        events.append(CashEvent(base + 1, f"Rent M{m+1}", -rent))
        events.append(CashEvent(base + 5, f"Utilities M{m+1}", -utilities))
        events.append(CashEvent(base + 10, f"Marketing M{m+1}", -marketing))

        # day 15 next month: PND.1 + SSO + ภพ.30
        next_15 = base + 30 + 15
        events.append(CashEvent(base + 30 + 7, f"PND.1 M{m+1}", -pnd1_monthly))
        events.append(CashEvent(next_15, f"SSO M{m+1}", -sso_monthly))
        events.append(CashEvent(next_15, f"VAT (ภพ.30) M{m+1}", -vat_payable))

        # supplier payment for COGS of this month after credit_days
        supplier_pay_day = base + 30 + supplier_credit_days - 30  # paid next month
        if supplier_credit_days <= 30:
            supplier_pay_day = base + supplier_credit_days
        else:
            supplier_pay_day = base + supplier_credit_days
        events.append(
            CashEvent(supplier_pay_day, f"Supplier (COGS M{m+1})", -cogs_monthly)
        )

    return events


def build_90_day_calendar(
    opening_balance: D,
    events: list[CashEvent],
) -> CashflowSummary:
    """Roll forward 90 days, returning a summary."""
    # sort events by day_offset (and outflows before inflows on same day for safety)
    events_sorted = sorted(events, key=lambda e: (e.day_offset, -e.amount))
    balance = opening_balance
    low_balance = opening_balance
    low_day = 0
    total_in = D("0")
    total_out = D("0")
    for e in events_sorted:
        if e.day_offset >= 90:
            continue
        balance += e.amount
        if e.amount > 0:
            total_in += e.amount
        else:
            total_out += -e.amount
        if balance < low_balance:
            low_balance = balance
            low_day = e.day_offset
    return CashflowSummary(
        opening_balance=opening_balance,
        closing_balance=balance.quantize(D("0.01")),
        low_point_balance=low_balance.quantize(D("0.01")),
        low_point_day_offset=low_day,
        total_inflows=total_in.quantize(D("0.01")),
        total_outflows=total_out.quantize(D("0.01")),
        events=events_sorted,
    )


def _self_test() -> None:
    # ร้านอาหารตามตัวอย่างใน SKILL.md
    events = standard_monthly_events(
        revenue_cash_per_month=D("600000"),
        salary_total=D("180000"),
        rent=D("95000"),
        utilities=D("25000"),
        marketing=D("30000"),
        cogs_pct_of_revenue=D("0.35"),
        supplier_credit_days=30,
        vat_payable=D("28000"),
        months=3,
    )
    s = build_90_day_calendar(D("250000"), events)
    # opening 250k
    # Per month: in 600k, out = salary 180+rent 95+util 25+mkt 30+SSO 9+PND1 3.6+VAT 28+COGS 210 = 580.6k
    # over 3 months: in 1.8M, out 1.74M roughly (some events spill to month 4 outside 90-day window)
    assert s.opening_balance == D("250000")
    assert s.total_inflows > D("0")
    assert s.total_outflows > D("0")
    print(f"  ✓ Opening: {s.opening_balance}")
    print(f"  ✓ Total inflows over 90d: {s.total_inflows}")
    print(f"  ✓ Total outflows over 90d: {s.total_outflows}")
    print(f"  ✓ Closing balance: {s.closing_balance}")
    print(f"  ✓ Low point: {s.low_point_balance} at day {s.low_point_day_offset}")
    # invariants
    assert s.closing_balance == s.opening_balance + s.total_inflows - s.total_outflows
    print("  ✓ accounting identity holds")

    # custom events
    custom = [CashEvent(10, "Bank loan disbursement", D("500000"))]
    s2 = build_90_day_calendar(D("0"), custom)
    assert s2.closing_balance == D("500000")
    print(f"  ✓ Single inflow: closing {s2.closing_balance}")


if __name__ == "__main__":
    _self_test()
    print("cashflow.py — all tests passed")
