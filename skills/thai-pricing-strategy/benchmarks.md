# Marketplace fees — Thailand 2026 reference

อัตรา commission + gateway ใน `pricing.py` ใช้ตัวเลขกลางของช่วงต่อไปนี้. แก้ใน `CHANNELS` ตรงๆ เมื่อ marketplace ปรับนโยบาย.

## Shopee TH

| Seller tier | Commission | Transaction fee (incl. VAT) | Total |
|---|---:|---:|---:|
| Shopee Mall (officially curated) | 5-8% (ตามหมวด) | 3.21% | ~9.5% |
| Shopee Preferred | 3-5% | 3.21% | ~7% |
| Shopee non-Mall regular | 0-5% | 3.21% | ~5.5% |

> Mall commission แตกต่างตามหมวด: Beauty/Personal Care 6-8%, Fashion 5-7%, Electronics 3-5%, Grocery 2-4%

อ้างอิง: Shopee Seller Center TH — `seller.shopee.co.th`

## Lazada TH

| Seller tier | Commission | Payment fee (incl. VAT) | Total |
|---|---:|---:|---:|
| LazMall | 5-7% | 3% (รวม VAT) | ~9% |
| Lazada non-Mall regular | 3-5% | 3% | ~7% |

อ้างอิง: Lazada Seller Center TH — `sellercenter.lazada.co.th`

## TikTok Shop TH

| Category | Commission (2026) |
|---|---:|
| Beauty & Personal Care | 5% |
| Fashion & Apparel | 4% |
| Home & Living | 3.5% |
| Electronics | 2% |
| Sports & Outdoors | 3% |
| Books & Stationery | 1% |

+ Transaction fee 2.4% (เฉลี่ย)

> ปี 2026 TikTok Shop ลด commission เพื่อแข่ง Shopee — เช็คอัปเดตทุกไตรมาส

อ้างอิง: TikTok Shop Seller TH — `seller-th.tiktok.com`

## LINE Shopping

- Commission: 3-5% (เฉลี่ย 4%)
- Transaction fee: 2.4%
- + LINE OA monthly fee แยก (ถ้ามี OA premium)

## หน้าร้าน (offline)

- Cash: 0%
- Card via terminal: 1.5-2.5% (depending on bank + card brand)
- PromptPay QR: 0%
- QR True/SCB Easy/K+: 0%

## Notes ที่สำคัญ

1. **Shipping subsidy** — Shopee Mall มักบังคับ "free shipping max 50฿" ทำให้ seller ต้อง absorb 20-50฿ ต่อชิ้นถ้า basket < threshold. ใส่เป็น `shipping_out` ใน `required_price()`.
2. **Voucher contribution** — Shopee/Lazada campaigns (9.9, 11.11, 12.12) มัก require seller absorb 5-15% voucher. ไม่อยู่ใน `pricing.py` — คำนวนแยกถ้าจะร่วม campaign.
3. **Marketplace ads** — TikTok Shop ads, Shopee Search ads ไม่ใช่ fee บังคับ. ดู unit_econ skill ถ้าจะรวม.
4. **VAT** — ราคา list บน marketplace ทุกที่เป็น **VAT-inclusive** (ถ้า seller จด VAT). ใน `pricing.py` ถือว่าเป็น cost-side ไม่ใช่ price-side. ถ้า seller จด VAT ต้องบวก 7% บนราคาขาย → ใช้ `thai-financial-projection`.
