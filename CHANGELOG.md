# Changelog

ตามรูปแบบ [Keep a Changelog](https://keepachangelog.com/), เวอร์ชันแบบ [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-05-19

### Added

- เปิดตัวรีโป — 12 skills สำหรับงานที่ปรึกษา SME ไทย
  - `thai-sme-canvas` — Business Model Canvas ปรับให้เหมาะ SME ไทย
  - `thai-market-sizing` — TAM/SAM/SOM กับ source pointer ทางการ
  - `thai-competitor-scan` — Porter 5 Forces + DBD lookup flow
  - `thai-pricing-strategy` — Pricing waterfall ต่อช่อง + `pricing.py`
  - `thai-unit-economics` — CAC/LTV ด้วย Thai 2026 benchmarks + `unit_econ.py`
  - `thai-financial-projection` — 3-yr P&L + SME tax tier + `tax.py`
  - `thai-business-registration` — Decision tree จดทะเบียน
  - `thai-vc-fundraising` — แผนระดมทุนกับ Thai VC ปี 2026
  - `thai-channel-strategy` — Channel mix matrix
  - `thai-influencer-deal` — KOL deal ถูก WHT + `commission.py`
  - `thai-sourcing-landed-cost` — Landed cost จาก 1688/Alibaba + `landed_cost.py`
  - `thai-cashflow-survival` — 90-day cashflow calendar + `cashflow.py`
- Plugin manifest (`plugin.json`, `marketplace.json`) — ติดตั้งทั้งชุดหรือเลือกตัว
- CI workflow รัน `scripts/test-all.sh` + `scripts/validate-skills.py` ทุก push/PR
- Template สำหรับสร้าง skill ใหม่ที่ `template/SKILL.md`
- Source catalog ที่ `docs/sources.md` — แหล่งข้อมูลทางการที่ skills อ้างอิง
