# AGENTS.md — คู่มือ AI agents

ไฟล์นี้สำหรับ AI agent (Claude Code, Cursor, Codex, Gemini CLI, …) ที่จะมาทำงานในรีโปนี้.

## บริบท / Context

รีโปนี้เป็นชุด Claude Code **skills** สำหรับงานที่ปรึกษา SME ไทย. แต่ละ skill อยู่ใน `skills/<name>/` พร้อม `SKILL.md` (frontmatter + คำแนะนำ) และ optional helper code.

ผู้ใช้ปลายทาง: founder/CEO ของ SME ไทย, ที่ปรึกษาที่ดูแล SME, นักวิเคราะห์ที่ทำงานในบริบทไทย. **ไม่ใช่ดีเวลอปเปอร์ฝรั่ง**. ทุก output ต้อง:

- ภาษาไทยเป็นหลัก (พร้อมศัพท์ภาษาอังกฤษเมื่อมาตรฐานต้องการ เช่น VAT, WHT, P&L, CAC, LTV)
- ตัวเลขเป็น THB เว้นแต่จะระบุ
- กฎหมาย/ภาษีอ้างอิงไทย (ประมวลรัษฎากร, PDPA, BOI, DBD) ไม่ใช่ US/EU
- ตลาดอ้างอิงไทย (Shopee TH, Lazada TH, TikTok Shop TH, LINE Shopping, FB Shop TH)

## วิธีทำงานในรีโปนี้ / How to work here

1. **อ่าน `template/SKILL.md`** ก่อนสร้าง skill ใหม่
2. **รัน `./scripts/validate-skills.py`** หลังแก้ frontmatter เพื่อเช็คโครงสร้าง
3. **รัน `./scripts/test-all.sh`** ก่อน commit
4. ทุก skill ต้องมี **self-test** ถ้ามี helper code (.py / .ts)
5. ใช้ `Decimal` ไม่ใช่ `float` ในทุกการคำนวนเงิน — เคยมีบั๊กตอน VAT 7% บน 33.33฿
6. อย่าเดา marketplace fee — copy benchmark จาก `skills/<name>/benchmarks.md` แล้วระบุ "อ้างอิงปี 2026"

## โครงสร้าง SKILL.md

ทุก SKILL.md เริ่มด้วย frontmatter YAML:

```yaml
---
name: thai-something
description: หนึ่งบรรทัด ตอบคำถาม "skill นี้ใช้ทำอะไร" — Claude เอาไปจับ intent
when_to_use:
  - เคสที่ skill นี้ตอบโจทย์ (1)
  - เคสที่ skill นี้ตอบโจทย์ (2)
when_not_to_use:
  - เคสที่ skill นี้ไม่เหมาะ
version: 0.1.0
last_verified: 2026-05-19
tier: validator | reference | prose
---
```

จากนั้นเป็น Markdown body — แนะนำ Claude ทีละขั้น. ดูตัวอย่างใน `skills/thai-pricing-strategy/SKILL.md`.

## หน่วยภาษี/กฎหมายที่ต้องอัปเดต / Tax & legal data to keep fresh

ทุกครั้งที่กฎหมายเปลี่ยน อัปเดต `last_verified:` ใน frontmatter และเพิ่ม entry ใน `CHANGELOG.md`.

- **Corporate income tax (SME)** — 2026: <300k = 0%, 300k-3M = 15%, >3M = 20% (ทุนชำระ ≤5M, รายได้ ≤30M)
- **VAT threshold** — 2026: 1.8M฿/ปี (ตามมาตรา 81/1)
- **WHT talent fee** — 2026: 3% (ไทย), 5% (ต่างชาติ resident), 15% (non-resident)
- **SSO contribution** — 2026: 5% นายจ้าง + 5% ลูกจ้าง, cap ที่ฐาน 15,000฿/เดือน
- **Marketplace fees** — Shopee Mall 5-8%, Lazada Mall 5-7%, TikTok Shop 1-8%, LINE Shopping 3-5% (ปี 2026)

## Disclaimer

รีโปนี้ **ไม่ใช่คำปรึกษากฎหมาย/ภาษีของจริง**. AI agents ที่เขียน skill ใหม่ต้อง:

1. ระบุ "อ้างอิงปี 2026" ทุกที่ที่เอ่ยอัตรา
2. แนะนำให้ user "ตรวจสอบกับผู้สอบบัญชี/ทนายของตัวเอง" ในเคสที่มี risk จริง
3. ห้ามให้คำแนะนำเชิง tax avoidance — เฉพาะ tax planning ที่ถูกกฎหมาย
