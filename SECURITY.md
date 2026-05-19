# Security & Disclaimer

## ขอบเขตการติดตั้ง / Install scope

ทั้งสองวิธีติดตั้ง — `/plugin install` และ `./install.sh` — **เขียนไฟล์เฉพาะใน `~/.claude/skills/<thai-*>`** เท่านั้น. ไม่แตะ:

- skills อื่นของ user (ทุกตัวมี prefix `thai-` ไม่ชน namespace กับใคร)
- `~/.claude/settings.json` / hooks / commands / agents
- ระบบไฟล์อื่นนอก `~/.claude/skills/`

**ไม่มี** postinstall script, ไม่มี `curl`/`sudo`, ไม่ดาวน์โหลดอะไรเพิ่มเวลาติดตั้ง. ถอนการติดตั้ง: ลบ folder `~/.claude/skills/thai-*` ที่ไม่ต้องการได้โดยตรง.

`./install.sh <name>` ตรวจชื่อด้วย regex `^[a-z0-9][a-z0-9-]*$` ก่อนเขียน — กัน path traversal เช่น `./install.sh ../docs`.

## รายงานช่องโหว่

ถ้าเจอช่องโหว่ที่กระทบความปลอดภัยของ user (เช่น helper code ที่ leak input, prompt injection ที่ทำให้ Claude แนะนำสิ่งที่ผิดกฎหมาย) — **อย่าเปิด public issue**.

ส่งไปที่: vittawat.soo+security [at] boombignose.org

จะตอบกลับใน 7 วัน.

## Disclaimer (เนื้อหากฎหมาย/ภาษี)

เนื้อหาในรีโปนี้ **ไม่ใช่คำปรึกษากฎหมายหรือคำปรึกษาภาษี**. เป็น "first-cut consulting framework" ที่ที่ปรึกษา/founder เอาไปใช้:

1. คุยกับลูกค้าตัวเอง (ในฐานะที่ปรึกษา)
2. เตรียมประเด็นก่อนคุยกับทนาย/ผู้สอบบัญชี
3. เข้าใจ landscape ของกฎหมาย/ภาษีไทยก่อนตัดสินใจ

**ห้ามใช้เป็น sole source** สำหรับ:

- การยื่นภาษี (ภงด.50, ภงด.51, ภพ.30, ฯลฯ)
- การจดทะเบียนบริษัท / ใบอนุญาต BOI / FDA / TISI
- การร่างสัญญา / NDA / employment contract
- การวางโครงสร้างหุ้น / convertible note / SAFE term sheet

ตัวเลขในรีโปนี้อ้างอิง **ปี 2026** — กฎหมายเปลี่ยน, อัตราเปลี่ยน, marketplace fee เปลี่ยน. ตรวจสอบกับแหล่งทางการก่อนใช้กับลูกค้าจริง.

## ตัวอย่างเคส = synthetic fixtures

ตัวอย่างชื่อบริษัท, เลขผู้เสียภาษี, ลูกค้า, ตัวเลขใน skill demos = **ของสมมุติทั้งหมด**. ไม่ใช่ลูกค้าจริง, ไม่ใช่บริษัทจริง.

## ไม่มีคำแนะนำ tax avoidance

Skill ในรีโปนี้แนะนำ **tax planning ถูกกฎหมาย** เท่านั้น (เช่น ตัดสินใจระหว่าง sole prop vs บริษัทตามขนาดรายได้). **ไม่มี** คำแนะนำ:

- ออกใบกำกับภาษีเท็จ
- ใช้ structure ปลอม shell company เพื่อเลี่ยงภาษี
- ละเมิด transfer pricing rules
- หลีก WHT โดย misclassify ลูกจ้างเป็น contractor

ถ้าเจอ skill ที่ทำผิดข้อนี้ — เปิด issue เร่งด่วน.
