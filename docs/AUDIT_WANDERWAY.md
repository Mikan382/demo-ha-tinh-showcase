# Rà soát wanderway-framer (3 trang core)

**Ngày:** 2026-06-12  
**Phạm vi:** `index.html`, `about-us.html`, `tours.html`  
**Brand:** Wander Hà Tĩnh — travel agency hiện đại

## Kết luận: ĐẠT

`python tools/audit_colorlib_wanderway.py` → WANDERWAY PASS

---

## Theo trang

| Trang | Hero / tiêu đề | Ảnh (mapping) | Ghi chú |
|---|---|---|---|
| `index.html` | Đi Hà Tĩnh theo một cách mới | IMG01/11/12/54/10 | Nav: Giới thiệu, Tour, Đặt tour |
| `about-us.html` | Giới thiệu công ty | shared-images | Meta VI |
| `tours.html` | Tour phổ biến | shared-images cycle | |

---

## Đã sửa trong pass này

- `FRAMER_VI` mở rộng: meta description, tour regions, section headings
- `fix_wanderway`: ẩn Framer editor bar + badge, gỡ GTM/events script
- `fix_framer`: Tours → Tour, Home → Trang chủ (nếu có), CTA VI
- CDN Framer → `assets/framerusercontent.com` (offline)
- Ảnh hero/content → `shared-images` (5 ảnh/page trong deep_fix)

## Ngoài scope core

- Trang tour quốc gia (`tours_spain.html`, `tours_cuba.html`…) vẫn tên quốc tế trong URL
- Font woff2 remote Framer — fallback system font khi offline
- SSR Framer vẫn có thể còn chuỗi EN trong JSON node sâu

## Kiểm tra lại

```bash
cd demo-ha-tinh-showcase
python tools/deep_fix.py
python tools/audit_colorlib_wanderway.py
python -m http.server 8080
# http://localhost:8080/wanderway-framer/index.html
```
