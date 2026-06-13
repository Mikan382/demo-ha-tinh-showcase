# Audit: luxestay-framer

**Brand:** LuxeStay Ha Tinh — villa / boutique stay  
**Tier:** C (Framer)  
**Script:** `python tools/audit_mountain_luxestay.py`

## Core pages

| Page | Hero / nội dung | Ảnh shared | EN |
|---|---|---|---|
| `index.html` | Không gian nghỉ dưỡng riêng tư tại Hà Tĩnh | 14 | ✓ |
| `rooms.html` | Danh sách phòng | 13 | ✓ |
| `restaurant.html` | Ẩm thực | 8 | ✓ |
| `contact-us.html` | Liên hệ | 3 | ✓ |

## Nav (index)

Giới thiệu, Phòng, Ẩm thực, Liên hệ.

## Pipeline

- `deep_fix.py` → brand, hero, ảnh (kể cả `url(&quot;…&quot;)`), form demo
- `fix_showcase.py` → `LUXESTAY_VI`, `fix_luxestay()`, symlink `.mjs`, ẩn editor Framer

## Kết quả

**PASS** — audit blocking 0.

## Sót nhỏ (không fail)

- Trang `wellness.html`, `wedding.html`, chi tiết phòng dài — chưa trong core audit
- Một số trang con thiếu đủ mục nav (giới hạn SSR Framer)
