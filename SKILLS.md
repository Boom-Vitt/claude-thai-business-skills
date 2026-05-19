# Skills — รายการเต็ม

ติดตั้งแบบเลือกตัว — copy คำสั่งทีละ skill ได้เลย.

```bash
/plugin marketplace add Boom-Vitt/claude-thai-business-skills
```

## 🧭 กลยุทธ์ & การวิเคราะห์ตลาด

### thai-sme-canvas
**[skills/thai-sme-canvas](skills/thai-sme-canvas)** — Business Model Canvas แบบ SME ไทย

ใช้เมื่อ: founder/ที่ปรึกษาอยากวาดโมเดลธุรกิจ SME ไทย โดยมีช่อง family-stakeholder, ทุนจดทะเบียน vs ทุนชำระแล้ว, MOU vs registered partner ที่ template ฝรั่งไม่มี.

```bash
/plugin install thai-sme-canvas
```

### thai-market-sizing
**[skills/thai-market-sizing](skills/thai-market-sizing)** — TAM/SAM/SOM ที่ดึงตัวเลขจริงจาก NSO/BOT/DBD/ETDA/NESDC

ใช้เมื่อ: ต้องประเมินขนาดตลาดไทย — Claude จะถาม category แล้วชี้แหล่งข้อมูลทางการ ฟรี, ระบุ confidence interval.

```bash
/plugin install thai-market-sizing
```

### thai-competitor-scan
**[skills/thai-competitor-scan](skills/thai-competitor-scan)** — Porter 5 Forces + วิธีดึงงบคู่แข่งจาก DBD

ใช้เมื่อ: อยากวิเคราะห์คู่แข่งโดยใช้ data จริง — ทุกบริษัทจำกัดในไทยต้องยื่นงบกับ DBD ทุกปี เปิด public ที่ datawarehouse.dbd.go.th.

```bash
/plugin install thai-competitor-scan
```

## 💰 ตั้งราคา & หน่วยเศรษฐกิจ

### thai-pricing-strategy ⭐
**[skills/thai-pricing-strategy](skills/thai-pricing-strategy)** — Pricing waterfall ต่อช่อง

ใช้เมื่อ: ตั้งราคาแล้วลืมหัก marketplace fee, payment gateway, packaging, freight — แล้วเหลือ margin จริงไม่ถึง 10%. `pricing.py` คำนวน margin จริงต่อช่อง (Shopee Mall, Lazada Mall, TikTok Shop, LINE Shopping, หน้าร้าน).

```bash
/plugin install thai-pricing-strategy
```

### thai-unit-economics ⭐
**[skills/thai-unit-economics](skills/thai-unit-economics)** — CAC/LTV/payback ด้วย benchmark Thai 2026

ใช้เมื่อ: คำนวน unit economics โดยไม่ใช้ benchmark US (จะหลอกตัวเอง). มี Meta/TikTok CPM, LINE OA push cost, KOC/nano/mid-tier KOL fees จาก Tellscore/AnyMind/MEDIA Z ปี 2026.

```bash
/plugin install thai-unit-economics
```

### thai-financial-projection
**[skills/thai-financial-projection](skills/thai-financial-projection)** — 3-yr P&L + cashflow ที่ถูก

ใช้เมื่อ: ทำ projection 3 ปี — `tax.py` คำนวน SME tax tier (<300k = 0%, 300k-3M = 15%, >3M = 20%), VAT cycle, SSO 5%+5%, ภงด.50/51 timing.

```bash
/plugin install thai-financial-projection
```

## 📜 จดทะเบียน & ระดมทุน

### thai-business-registration
**[skills/thai-business-registration](skills/thai-business-registration)** — Decision tree จดทะเบียน

ใช้เมื่อ: ต้องตัดสินใจ ทะเบียนพาณิชย์ vs หจก. vs บริษัทจำกัด vs BOI — flag VAT trigger 1.8M฿/ปี, SSO trigger เมื่อมีพนักงาน 1 คน.

```bash
/plugin install thai-business-registration
```

### thai-vc-fundraising
**[skills/thai-vc-fundraising](skills/thai-vc-fundraising)** — แผนระดมทุนจาก Thai VC จริง

ใช้เมื่อ: เตรียมระดมทุนกับ VC ไทย — มี catalog ของ 500 Global, AddVentures, Beacon VC, Krungsri Finnovate, SCB10X, KX, Bualuang Ventures, InnoSpace, Storyhouse พร้อม stage / check size / thesis ปี 2026.

```bash
/plugin install thai-vc-fundraising
```

## 🚀 Go-to-Market & ดำเนินงาน

### thai-channel-strategy
**[skills/thai-channel-strategy](skills/thai-channel-strategy)** — Channel mix matrix

ใช้เมื่อ: ต้องเลือกช่อง — LINE OA / FB Shop / Shopee Mall / Lazada / TikTok Shop / offline — โดย map AOV, repeat rate, margin headroom ลงในตาราง decision.

```bash
/plugin install thai-channel-strategy
```

### thai-influencer-deal
**[skills/thai-influencer-deal](skills/thai-influencer-deal)** — โครงสร้างดีล KOL ถูกกฎหมาย

ใช้เมื่อ: ดีลกับ KOL/KOC — `commission.py` คำนวน net payout หลัง WHT (3/5/15% ตามสัญชาติ/ประเภท), แยก talent fee จาก affiliate revenue share, สร้าง contract template.

```bash
/plugin install thai-influencer-deal
```

### thai-sourcing-landed-cost
**[skills/thai-sourcing-landed-cost](skills/thai-sourcing-landed-cost)** — Landed cost จาก 1688/Alibaba

ใช้เมื่อ: นำเข้าสินค้า — `landed_cost.py` คำนวน import duty ตาม HS code, VAT 7% on CIF, flag FDA (cosmetic/food/medical 1-6 เดือน) / TISI (electronics) / มอก. requirement.

```bash
/plugin install thai-sourcing-landed-cost
```

## 💧 Cash Survival

### thai-cashflow-survival ⭐
**[skills/thai-cashflow-survival](skills/thai-cashflow-survival)** — 90-day cashflow calendar

ใช้เมื่อ: SME ใกล้ตึง — `cashflow.py` กางปฏิทิน 90 วันที่ lock timing ไทย: credit term 30/60/90, VAT refund delay 3-6 เดือน, PND.1 (วันที่ 7), SSO (15), ภงด.50/51 schedule.

```bash
/plugin install thai-cashflow-survival
```
