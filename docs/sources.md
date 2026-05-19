# Data sources — แหล่งข้อมูลทางการที่รีโปนี้อ้างอิง

หน้านี้คือ catalog ของแหล่งข้อมูลทางการที่ทุก skill ใน `skills/` อ้างถึง. ถ้าจะ contribute ตัวเลขใหม่ ต้องชี้แหล่งจากตารางนี้ (หรือเพิ่มแหล่งใหม่ใน PR).

## ภาษี & กฎหมาย

| แหล่ง | URL | ใช้ในข้อมูล | อัปเดต |
|---|---|---|---|
| กรมสรรพากร | `rd.go.th` | corporate tax rate, VAT, WHT, PIT, ฟอร์ม | ตามประกาศ (ตรวจรายไตรมาส) |
| กรมพัฒนาธุรกิจการค้า | `dbd.go.th`, `datawarehouse.dbd.go.th` | งบการเงินบริษัท, การจดทะเบียน | ทุกบริษัทยื่นรายปี |
| BOI | `boi.go.th` | เกณฑ์ส่งเสริม, สิทธิประโยชน์ | ตามประกาศ BOI |
| ประกันสังคม (SSO) | `sso.go.th` | อัตราเงินสมทบ, ฐาน | ตามประกาศ |
| ศุลกากร | `customs.go.th` | HS code, import duty | ตามประกาศ |
| อย. (FDA) | `fda.moph.go.th` | timeline จดทะเบียน cosmetic/food/medical | คงที่ |
| TISI | `tisi.go.th` | มอก. บังคับ | ตามประกาศ |
| PDPC | `pdpc.or.th` | PDPA guideline | ตามประกาศ |

## เศรษฐกิจ & ตลาด

| แหล่ง | URL | ใช้ในข้อมูล |
|---|---|---|
| สำนักงานสถิติแห่งชาติ (NSO) | `nso.go.th` | household survey, business register, demography |
| ธนาคารแห่งประเทศไทย (BOT) | `bot.or.th` | economic indicators, payment statistics, FX |
| NESDC | `nesdc.go.th` | GDP, sector breakdown |
| ETDA | `etda.or.th` | e-commerce statistics, digital economy |
| ก.พาณิชย์ — Trade Statistics | `tradereport.moc.go.th` | import/export data |
| Statista TH | `statista.com` (paywall, ใช้ free preview) | market sizing |

## Marketplace & Ad platforms (ราคา/fee ปี 2026)

| แหล่ง | URL | ใช้ใน |
|---|---|---|
| Shopee Seller Center TH | `seller.shopee.co.th` | Mall commission rate, shipping subsidy |
| Lazada Seller Center TH | `sellercenter.lazada.co.th` | Mall fee, payment fee |
| TikTok Shop Seller TH | `seller-th.tiktok.com` | commission per category |
| LINE Shopping merchant | `linebizapi.line.me/shopping` | platform fee |
| Meta Business Help | `business.facebook.com/help` | ads policy (ไม่ใช่ CPM number) |
| Google Ads TH benchmarks | จาก published industry reports |

## Influencer / KOL benchmarks

| แหล่ง | URL | ใช้ใน |
|---|---|---|
| Tellscore | `tellscore.com` | KOL/KOC published rate cards |
| AnyMind Group | `anymindgroup.com` | published industry reports |
| MEDIA Z | `mediaz.co.th` | influencer marketing reports |
| Wisesight | `wisesight.com` | social listening + reports |

## VC / Funding (Thai)

| Fund | Stage | Check size 2026 | Link |
|---|---|---|---|
| 500 Global (เดิม 500 TukTuks) | Seed | 5-15M฿ | `500.co/southeast-asia` |
| AddVentures (SCG) | A-B | 30-150M฿ | `addventures.co.th` |
| Beacon VC (KBank) | A-B | 30-150M฿ | `beaconvc.fund` |
| Krungsri Finnovate | A-B | 30-150M฿ | `krungsri.com/finnovate` |
| SCB10X | A-C | 50-300M฿ | `scb10x.com` |
| KX (KASIKORN X) | A-B | 30-150M฿ | `kx.global` |
| Bualuang Ventures (BBL) | A-B | 30-150M฿ | `bblam.co.th` |
| InnoSpace TH | Seed | 5-30M฿ | `innospace.co.th` |
| Storyhouse / Story Ventures | Seed-A | 10-50M฿ | (private) |
| True Digital Park ventures | Seed | 5-20M฿ | `truedigitalpark.com` |

> ตัวเลข check size เป็นช่วงโดยประมาณจาก deals ที่เผยแพร่ public — ใช้เป็น guidance ไม่ใช่ commitment.

## ข้อกำหนดในการใช้แหล่งเหล่านี้

- ใช้เฉพาะ data ที่เผยแพร่ public (เว็บไซต์ทางการ, ประกาศ, รายงาน, press release)
- ห้าม scrape paid databases (Statista paid tier, paid market research) — เอาแค่ free preview
- ห้าม cite ตัวเลขที่ไม่มีแหล่ง — ใส่ `[needs source]` แทน
