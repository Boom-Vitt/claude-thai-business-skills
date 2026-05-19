# My setup — ทัวร์ config ที่ผมใช้จริง (sanitized)

หน้านี้เปิดให้ดู config ส่วนตัวผมที่ใช้ทำงานที่ปรึกษาทุกวัน — เผื่อ user อยากเอาไป remix.

## Claude Code

```bash
# ติดตั้ง skill ทั้งชุด
/plugin marketplace add Boom-Vitt/claude-thai-business-skills
/plugin install claude-thai-business-skills

# + ของรีโปอีกตัวสำหรับงานเอกสารไทย
/plugin marketplace add Boom-Vitt/claude-thai-skills
/plugin install claude-thai-skills
```

## เครื่องมือคู่ขนาน

- **Excalidraw** สำหรับวาด Business Model Canvas / Channel Mix matrix ที่ส่งให้ลูกค้าดู
- **Google Sheets** สำหรับ output ของ `pricing.py`, `unit_econ.py`, `cashflow.py` — copy CSV จาก Claude แล้ว paste
- **Notion** สำหรับเก็บ decision log ของลูกค้าแต่ละราย
- **LINE OA** สำหรับคุยลูกค้า (ส่วน Voice ใช้คุยทางโทรศัพท์)

## Workflow ที่ใช้

1. ลูกค้าใหม่ — ใช้ `thai-sme-canvas` วาด BMC ใน 30 นาทีแรก
2. มี product — `thai-pricing-strategy` + `thai-unit-economics` ก่อนตัดสินใจราคา
3. เตรียมจดบริษัท — `thai-business-registration` decision tree
4. ระดมทุน — `thai-vc-fundraising` + `thai-financial-projection`
5. เจอ cashflow ตึง — `thai-cashflow-survival` กางปฏิทิน 90 วัน

## Anti-pattern ที่เคยทำผิด

- เคยใช้ Claude ตั้งราคาโดยไม่หัก Shopee fee — ลูกค้าขายเดือนเดียวเจ๊ง 70k
- เคยทำ projection โดยใช้ tax 20% หมด — ลูกค้าคิดว่าตัวเองขาดทุน ทั้งที่จริง break-even
- เคยแนะนำให้จดบริษัทตั้งแต่ 800k/ปี — เปลือง 60k/ปี ค่าทำบัญชี+ตรวจสอบ
- เคยดีลกับ KOL โดยไม่หัก WHT — สรรพากรเรียกตรวจปีถัดมา

แต่ละเคสเป็นที่มาของ skill ที่อยู่ใน repo นี้.
