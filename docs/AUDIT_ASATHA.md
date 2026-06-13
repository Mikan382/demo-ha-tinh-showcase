# Rà soát asatha-luxury-webflow (6 trang core)

**Ngày:** 2026-06-13  
**Phạm vi:** `index.html`, `about-us.html`, `villas-and-suites.html`, `wellness.html`, `dining.html`, `contact-us.html`  
**Brand:** Ke Go Retreat — luxury retreat / wellness / villa

## Kết luận: ĐẠT

`python tools/audit_hotale_asatha.py` → ASATHA PASS

---

## Theo trang

| Trang | Hero / concept | Ảnh (mapping) | Menu |
|---|---|---|---|
| `index.html` | Nghỉ dưỡng giữa thiên nhiên Hà Tĩnh | IMG18, 19 hero | Giới thiệu, Villa, Wellness, Ẩm thực, Liên hệ |
| `about-us.html` | Câu chuyện Ke Go Retreat | shared-images | ✓ |
| `villas-and-suites.html` | Villa & suite (tên VI) | IMG20, 58 | ✓ |
| `wellness.html` | Spa & wellness | IMG28, 57 | ✓ |
| `dining.html` | Ẩm thực Ke Go | IMG26, 59 | ✓ |
| `contact-us.html` | Form liên hệ demo | shared-images | ✓ |

---

## Đã sửa trong pass này

- Toàn bộ ảnh raster `cdn.prod.website-files.com` → `shared-images` (pool 10 ảnh)
- Xóa `srcset` CDN broken; giữ logo SVG
- Modal đặt phòng, CTA, footer → VI
- Ẩn vendor: `showcase-dropdown`, Flowcub footer, template popup
- Villa names (Sunset Estate → Villa Hoàng Hôn, …)
- Đoạn "Discover …" / meta EN còn sót → VI

## Ngoài scope core

- Trang villa chi tiết (`villas-and-suites_*.html`), packages, blog posts — chưa Việt hóa đầy đủ
- Logo SVG gốc template (giữ nguyên — hiển thị OK)
- Menu mobile label "Menu" (chấp nhận được)

## Kiểm tra lại

```bash
cd demo-ha-tinh-showcase
python tools/deep_fix.py
python tools/audit_hotale_asatha.py
python -m http.server 8080
```

Mở: `http://localhost:8080/asatha-luxury-webflow/index.html`
