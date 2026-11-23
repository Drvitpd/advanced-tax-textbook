# ตำราภาษีชั้นสูง: แอปประจำเล่ม

แอปประจำบทของตำราภาษีชั้นสูง (ภาษีเงินได้นิติบุคคล ภาษีมูลค่าเพิ่ม ภาษีธุรกิจเฉพาะ อากรแสตมป์) โดย ดร.วิทยา อรุณศิริเพ็ชร

เว็บแอป: https://drvitpd.github.io/advanced-tax-textbook/ (หน้าบท `chNN.html`)

## โครงสร้าง
- `site/src/chNN.html` แอปรายบท (ต้นฉบับ)
- `site/brand.json` ชื่อแบรนด์ ชื่อเล่ม และแฮชรหัสเข้าแอป
- `site/build_site.py` สร้าง `docs/` (หน้าสารบัญ หน้าบท gate.js และ QR ใน `docs/qr/`)
- `docs/` ไฟล์ที่ GitHub Pages ใช้ (Settings → Pages → main · /docs)

## เปลี่ยนแบรนด์
- โลโก้: แทนไฟล์ `docs/brand/logo.png`
- ชื่อแบรนด์หรือรหัส: แก้ `site/brand.json` แล้วรัน `python3 site/build_site.py`

รหัสเข้าแอปกันการเข้าโดยบังเอิญเท่านั้น ไม่ใช่ระบบความปลอดภัย
