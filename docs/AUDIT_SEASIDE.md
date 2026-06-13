# Rà soát seaside-webflow (5 trang core)

**Ngày:** 2026-06-12  
**Phạm vi:** `index.html`, `about.html`, `resort.html`, `rooms-overview.html`, `contact.html`  
**Brand:** Coastal Stay Ha Tinh — homestay/resort ven biển

## Kết luận: ĐẠT

`python tools/audit_seaside_moonlit.py` → SEASIDE PASS

---

## Theo trang

| Trang | Hero / tiêu đề | Ảnh (mapping) | Ghi chú |
|---|---|---|---|
| `index.html` | Lưu trú gần biển, tận hưởng nhịp sống Hà Tĩnh | IMG08/35 hero CSS; phòng IMG09/29/60 | Nav VI, CTA Xem không gian |
| `about.html` | Giới thiệu Coastal Stay | og:image + shared-images | Liên hệ Thiên Cầm |
| `resort.html` | Tiện ích resort | IMG16/48 pool + gallery | Ảnh CDN → shared-images |
| `rooms-overview.html` | Danh sách phòng | IMG09/29/60 cycle | |
| `contact.html` | Liên hệ | og:image hero | Form demo-safe |

---

## Đã sửa trong pass này

- `fix_seaside_imgs()`: map toàn bộ ảnh nội dung CDN (jpg/png) → `shared-images` (pool 8 ảnh); giữ icon UI local
- Chuẩn hóa path `assets/assets.website-files.com` → `cdn.prod.website-files.com`
- Trang thiếu ảnh body: thêm `og:image` shared-images trong `apply_seaside_html()`
- Audit: bỏ false-positive Webflow (`data-wf-domain`), icon `Icon-*`

## Ngoài scope core

- ~8 trang phụ (events, room detail, 404…) đã qua `fix_seaside_extra()` nhưng chưa audit từng trang
- Icon header vẫn load từ CDN crawl local (không cần shared-images)

## Kiểm tra lại

```bash
cd demo-ha-tinh-showcase
python tools/deep_fix.py
python tools/audit_seaside_moonlit.py
python -m http.server 8080
# http://localhost:8080/seaside-webflow/index.html
```
