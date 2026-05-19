<!-- ขอบคุณที่ส่ง PR — กรอก checklist ด้านล่างให้ครบ -->

## สรุปการเปลี่ยนแปลง

<!-- 1-3 ประโยค: PR นี้ทำอะไร -->

## เกี่ยวข้องกับ skill ไหน

- [ ] เพิ่ม skill ใหม่ (ระบุชื่อ: `_____`)
- [ ] แก้ skill เดิม (ระบุชื่อ: `_____`)
- [ ] แก้ infrastructure (scripts, CI, docs)

## Checklist

- [ ] `./scripts/test-all.sh` ผ่าน local
- [ ] อัปเดต `last_verified:` ใน SKILL.md frontmatter (ถ้าแก้ skill เดิม)
- [ ] อัปเดต `CHANGELOG.md` ใต้ `[Unreleased]`
- [ ] ถ้าเป็น skill ใหม่:
  - [ ] register ใน `.claude-plugin/marketplace.json`
  - [ ] เพิ่ม entry ใน `SKILLS.md`
  - [ ] ถ้ามี helper code — register ใน `scripts/test-all.sh`
- [ ] ถ้าแก้อัตราภาษี / ค่าธรรมเนียมตลาด — ระบุแหล่ง + วันที่ตรวจสอบใน PR body

## แหล่งอ้างอิง (ถ้ามี)

<!-- ลิงก์ไปที่ rd.go.th, bot.or.th, dbd.go.th, ฯลฯ ที่ใช้ตรวจสอบตัวเลข -->
