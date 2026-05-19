# Contributing

ขอบคุณที่อยากช่วย — รีโปนี้เปิดรับ PR และ issue.

## เปิด issue ก่อน PR เสมอ

ถ้าจะเพิ่ม skill ใหม่ หรือเปลี่ยน behavior ของ skill เดิม — เปิด issue ก่อน. เราอาจจะมีเหตุผลที่ไม่ทำแบบนั้น หรือมีคนกำลังทำอยู่.

## ตั้งค่าเครื่อง

```bash
git clone https://github.com/Boom-Vitt/claude-thai-business-skills.git
cd claude-thai-business-skills

# Python 3.10+ สำหรับ validator + helpers
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt  # ถ้ามี — ตอนนี้ใช้ stdlib เท่านั้น
```

## รัน test

```bash
./scripts/test-all.sh           # รัน self-test ของทุก skill + validator
./scripts/validate-skills.py    # เช็คเฉพาะ frontmatter
```

CI ใน `.github/workflows/test.yml` รันคำสั่งเดียวกันทุก push/PR.

## เพิ่ม skill ใหม่

1. Copy `template/SKILL.md` ไปที่ `skills/<thai-slug>/SKILL.md`
2. แก้ frontmatter — name, description, when_to_use, version, last_verified, tier
3. เขียน body ภาษาไทย (พร้อม EN term มาตรฐาน)
4. ถ้ามี calculation — เขียน helper `<thing>.py` ที่ใช้ `Decimal` + ทดสอบด้วย `if __name__ == "__main__":` block (self-test)
5. Register ใน `scripts/test-all.sh` — เพิ่ม path ของ helper ที่จะถูกรัน
6. เพิ่ม entry ใน `.claude-plugin/marketplace.json` เป็น standalone plugin
7. เพิ่ม entry ใน `SKILLS.md` (พร้อม `/plugin install` คำสั่ง)
8. PR

## House style

- **Voice**: ใช้สรรพนาม "ผม" (เป็น author voice) ใน README + `Why this exists`. ใน SKILL.md ใช้ภาษากลาง (สั่งให้ Claude ทำ ไม่ใช่เล่าเรื่อง)
- **Numbers**: THB เสมอเว้นแต่ระบุ. Format `1,200฿` หรือ `1,200 บาท` — เลือกอย่างใดอย่างหนึ่งใน skill เดียวกัน
- **Dates**: ค.ศ. สำหรับ git/CI/code. พ.ศ. สำหรับ document output ที่ users ใช้กับลูกค้าจริง
- **No hype**: ห้าม "amazing", "powerful", "ล้ำสมัย", "ปฏิวัติวงการ". พูดสิ่งที่ skill ทำ จบ
- **Cite**: ทุกครั้งที่เอ่ยอัตราภาษี/ค่าธรรมเนียมตลาด ระบุปี + แหล่ง (`อ้างอิง revenue.rd.go.th, ปรับล่าสุด 2026-05`)

## PR template

จะมี checklist ใน `.github/PULL_REQUEST_TEMPLATE.md` — กรอกให้ครบ. หลักๆ:

- [ ] `./scripts/test-all.sh` ผ่าน
- [ ] อัปเดต `last_verified:` ใน frontmatter
- [ ] อัปเดต `CHANGELOG.md`
- [ ] ถ้าเป็น skill ใหม่: register ใน `marketplace.json` + `SKILLS.md`
- [ ] ถ้าแก้อัตราภาษี/ค่าธรรมเนียม: ระบุแหล่งใน body PR
