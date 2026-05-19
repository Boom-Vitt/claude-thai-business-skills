# Third-Party Notices

รีโปนี้อ้างอิง (แต่ไม่ได้ bundle) เนื้อหา/data points จากแหล่งทางการและชุมชน. เครดิตและขอบเขตการใช้:

## แหล่งทางการ (public domain / open data)

- **กรมพัฒนาธุรกิจการค้า (DBD)** — `datawarehouse.dbd.go.th` — งบการเงินบริษัทจำกัดที่ยื่นรายปี (public, ฟรี). ใช้ใน `thai-competitor-scan`
- **กรมสรรพากร (Revenue Department)** — `rd.go.th` — อัตราภาษี, ประมวลรัษฎากร, ฟอร์มภงด./ภพ. ใช้ใน `thai-financial-projection`, `thai-business-registration`, `thai-influencer-deal`
- **สำนักงานสถิติแห่งชาติ (NSO)** — `nso.go.th` — household survey, business register. ใช้ใน `thai-market-sizing`
- **ธนาคารแห่งประเทศไทย (BOT)** — `bot.or.th` — economic indicators, payment statistics. ใช้ใน `thai-market-sizing`, `thai-unit-economics`
- **สำนักงาน สศช. (NESDC)** — `nesdc.go.th` — GDP, industry breakdown. ใช้ใน `thai-market-sizing`
- **ETDA** — `etda.or.th` — e-commerce + digital economy statistics. ใช้ใน `thai-market-sizing`, `thai-channel-strategy`
- **กรมศุลกากร (Customs)** — `customs.go.th` — HS code, import duty rate. ใช้ใน `thai-sourcing-landed-cost`
- **อย. (FDA)** — `fda.moph.go.th` — registration timeline สำหรับ cosmetic/food/medical. ใช้ใน `thai-sourcing-landed-cost`
- **TISI / มอก.** — `tisi.go.th` — มาตรฐานบังคับสำหรับ electronics. ใช้ใน `thai-sourcing-landed-cost`
- **สำนักงานประกันสังคม (SSO)** — `sso.go.th` — อัตรา + ฐานเงินสมทบ. ใช้ใน `thai-financial-projection`, `thai-cashflow-survival`
- **BOI** — `boi.go.th` — เกณฑ์ส่งเสริมการลงทุน. ใช้ใน `thai-business-registration`, `thai-vc-fundraising`

## แหล่งการตลาด (proprietary — อ้างอิงเฉพาะ benchmarks ที่เผยแพร่ public)

- **Tellscore** — KOL/KOC rate card published public. ใช้ใน `thai-unit-economics`, `thai-influencer-deal`
- **AnyMind Group** — published industry reports. ใช้ใน `thai-unit-economics`
- **MEDIA Z** — published influencer marketing reports. ใช้ใน `thai-unit-economics`
- **Statista Thailand** — paywalled; เราอ้างอิงเฉพาะ data ที่ free preview เผยแพร่ public
- **Kantar Worldpanel TH, GroupM TH, Nielsen TH** — published quarterly reports

## Inspiration / patterns

- **Lean Canvas** © Ash Maurya (CC BY-SA 3.0) — `thai-sme-canvas` ปรับแนวคิดมา
- **Business Model Canvas** © Strategyzer (CC BY-SA 3.0) — `thai-sme-canvas`
- **Porter's Five Forces** — Michael Porter, Harvard Business School (academic framework) — `thai-competitor-scan`
- **Ansoff Matrix** — Igor Ansoff (academic framework)
- **BCG Growth-Share Matrix** — Boston Consulting Group (academic framework)

## Communities & repos ที่ remix แนวคิด

ดู section "Credits & inspirations" ใน [README.md](README.md). ทุกตัวที่อ้างมีลิงก์ไปยังต้นทาง.

## Disclaimer

อัตราภาษี/ค่าธรรมเนียม/data ทั้งหมดอ้างอิงปี **2026**. หน่วยงานทางการอาจอัปเดต — ตรวจสอบกับ source ตรงๆ ก่อนใช้กับลูกค้าจริง. ดู [SECURITY.md](SECURITY.md) สำหรับ disclaimer เต็ม.
