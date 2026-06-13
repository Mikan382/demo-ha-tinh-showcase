# Audit: mountain-lodge-framer

**Brand:** Ke Go Eco Lodge — eco lodge ven hồ Kẻ Gỗ  
**Tier:** C (Framer)  
**Script:** `python tools/audit_mountain_luxestay.py`

## Core pages

| Page | Hero / nội dung | Ảnh shared | EN |
|---|---|---|---|
| `index.html` | Chạm vào nhịp sống xanh bên hồ Kẻ Gỗ | 27 | ✓ |
| `about.html` | Giới thiệu lodge | 6 | ✓ |
| `rooms.html` | Phòng nghỉ | 25 | ✓ |
| `restaurants.html` | Ẩm thực | 29 | ✓ |
| `contact.html` | Liên hệ + form demo | 17 | ✓ |

## Nav (index)

Phòng, Liên hệ, Gallery — menu VI trên SSR.

## Pipeline

- `deep_fix.py` → brand, hero, ảnh `src` + `url()`, form demo
- `fix_showcase.py` → `MOUNTAIN_VI`, `fix_mountain()`, ẩn Framer editor/badge

## Kết quả

**PASS** — audit blocking 0.

## Sót nhỏ (không fail)

- Một số nhãn tiếng Anh trong footer (FACEBOOK, INSTAGRAM, ngày blog mẫu)
- Trang phụ `area.html`, `events.html`, `gallery.html` chưa trong core audit
