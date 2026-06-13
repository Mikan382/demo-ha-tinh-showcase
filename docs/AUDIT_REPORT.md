# Báo cáo rà soát — Ha Tinh Template Showcase

**Ngày:** 2026-06-12  
**Phạm vi:** 9 template demo + catalog (`index.html`)  
**Công cụ:** `tools/deep_fix.py`, `tools/audit_core.py`, kiểm tra HTTP + browser snapshot

---

## Tóm tắt

Lần triển khai đầu dùng thay thế hàng loạt (đổi `img src` tuần tự, `Bali → Hà Tĩnh` toàn cục) nên **chưa đạt chuẩn showcase**. Đã chạy **pass rà soát sâu** với các hành động chính:

| Vấn đề ban đầu | Cách xử lý |
|---|---|
| `seaside-webflow` — icon sao/avatar bị thay bằng ảnh phòng | Khôi phục 5 trang core từ `template-scrapes/`, chỉ đổi hero CSS + text có chủ đích |
| `asatha` — popup "Buy this template $99" | Xóa DOM popup + `display:none` trên mọi `.html` |
| `colorlib` — hero `bg_1.jpg`, title lỗi | Map `shared-images`, sửa nav/title |
| `hotale` — menu/blog tiếng Anh, địa chỉ Madrid | Menu desktop 6 mục VI; blog titles VI; map label Hà Tĩnh |
| `travol` — ", Europe", Perugia | Sửa chuỗi địa danh, nav VI 6 trang core |
| Framer — badge BUY THIS TEMPLATE, Europe | Ẩn badge, thay text hiển thị |

**Kết quả `audit_core.py` (trang core theo plan):** 0 lỗi blocking.

---

## Checklist Definition of Done

| Tiêu chí | Catalog | travol | hotale | seaside | asatha | colorlib | moonlit | framer×3 | bali |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| HTTP 200 homepage | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| Brand / title VI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ README |
| Nav core VI | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | — |
| Hero ảnh Hà Tĩnh | — | ✅ | ✅ | ✅ CSS | ✅ | ✅ | ✅ | ✅ | — |
| Không popup vendor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Form demo (preventDefault) | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Nội dung body VI (core) | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | — |

**Chú thích:** ✅ đạt trên trang ưu tiên · ⚠️ còn tiếng Anh ở section phụ / trang con / footer template · — không áp dụng

---

## Chi tiết từng template

### travol-duruthemes — Ha Tinh Travel
- **Pass:** 6 trang core, nav VI, hero `shared-images`, testimonial tên Việt, footer contact demo.
- **Còn lại:** Các biến thể `index2–4`, `tours2` (ngoài phạm vi plan) vẫn tiếng Anh.

### hotale-resort — Thien Cam Resort
- **Pass:** Homepage VI, ảnh resort `shared-images`, menu desktop gọn 6 mục, blog section đã Việt hóa tiêu đề.
- **Còn lại:** Menu mobile (`mm-menu`) vẫn nhiều mục template gốc; `price-table.html` / `contact.html` không có hero ảnh (trang phụ); Google Maps embed vẫn tọa độ UK (chỉ đổi label text).

### seaside-webflow — Coastal Stay Ha Tinh
- **Pass:** Hero 3 slide qua CSS → `shared-images`; địa chỉ Thiên Cầm; điểm đến Hà Tĩnh; form VI; không còn lỗi ảnh sao/avatar.
- **Còn lại:** Trang `events/*`, `rooms/*` chi tiết chưa localize; footer link "Webflow".

### asatha-luxury-webflow — Ke Go Retreat
- **Pass:** Popup mua template đã xóa/ẩn; hero + section ảnh Kẻ Gỗ; brand VI; CTA chính VI.
- **Còn lại:** Một số đoạn marketing gốc (guest stories, địa chỉ Bali còn sót trong paragraph); footer "Made by design"; trang blog/package con chưa rà.

### colorlib-deluxe — Deluxe Hotel Ha Tinh
- **Pass:** `index.html` hero/bg + phòng map `shared-images`; nav 5 trang core VI.
- **Còn lại:** Một số section mô tả ngắn còn tiếng Anh trên subpages.

### moonlit-react — Moonlit Hotel Ha Tinh
- **Pass:** 5 trang core, ảnh chính đã map, label nav cơ bản VI.
- **Còn lại:** React bundle vẫn chứa string gốc trong JS (ngoài phạm vi HTML edit).

### mountain-lodge / wanderway / luxestay (Framer)
- **Pass:** Brand VI, ảnh hero `shared-images`, badge Framer ẩn, CTA cơ bản VI.
- **Còn lại:** Nội dung SSR Framer vẫn lẫn tiếng Anh trong JSON/text node; chỉ homepage + 2–3 trang nav đã chạm.

### webflow-bali-travel
- **Pass:** Card limitation + `README.md` + link preview (đúng spec, không rebuild HTML).

---

## Cách chạy lại audit

```bash
cd c:\scratch\demo-ha-tinh-showcase
python -m http.server 8080
python tools/deep_fix.py      # áp dụng sửa (idempotent)
python tools/audit_core.py      # quét trang core
```

---

## Pass 2 polish (2026-06-12)

| Hạng mục | Trạng thái |
|---|---|
| hotale menu mobile | ✅ 6 mục VI (Trang chủ → Liên hệ) |
| hotale map embed | ✅ Tọa độ Thiên Cầm / Hà Tĩnh |
| hotale lorem / blog sót | ✅ Thay đoạn "wonderful serenity", blog title EN |
| asatha toàn bộ `*.html` | ✅ Text VI + xóa popup trên mọi trang |
| seaside trang phụ | ✅ `events.html`, `rooms_*`, `events_*` (9 trang) |
| audit_core | ✅ 0 lỗi blocking |

## Pass 4 — Infrastructure (trang trắng, asset, bản quyền)

Script mới: `tools/fix_showcase.py` (chạy tự động sau `deep_fix.py`)

| Vấn đề | Cách xử lý |
|---|---|
| **moonlit** trang tối/trống (0 ảnh raster) | Sửa `index.htmlassets/` → `assets/`; map ảnh → `shared-images`; fallback icon emoji |
| **seaside** ảnh card 404 | Sửa path `561acb.../NN_*.png` → `../assets/shared-images/` |
| **colorlib** ảnh `images/` thiếu | Map toàn bộ `images/*.jpg` → `shared-images`; bỏ script timepicker hỏng |
| **wanderway** phụ thuộc CDN Framer | Rewrite URL → `assets/framerusercontent.com/...` (offline) |
| **luxestay** `.mjs` 404 | Copy symlink `.mjs.js` → `.mjs` |
| **hotale** `upload/` thiếu | Map background → `shared-images` |
| **travol** `img/destination/` trống | Map tab ảnh → `shared-images` |
| Popup/badge vendor | CSS ẩn global + xóa link Webflow/Flowcub/Framer templates |
| Framer footer “Fourtwelve” | Ẩn + thay text |

**Lưu ý:** Icon font (flaticon hotale/moonlit, ionicons colorlib) vẫn có thể thiếu file `.woff` từ crawl — moonlit dùng emoji fallback; hotale/colorlib giữ SVG/CSS gốc nếu còn.

## Pass 3 polish (2026-06-12)

| Hạng mục | Trạng thái |
|---|---|
| hotale tên phòng + giá | ✅ VI (Phòng Deluxe, giá VND, / đêm) |
| hotale tiện ích + testimonial | ✅ Bãi đỗ xe, Hồ bơi, tên khách Việt |
| Catalog thumbnails | ✅ Ảnh hero `shared-images` + overlay gradient |

## Khuyến nghị nếu cần polish thêm

1. **asatha** — paragraph marketing dài trong trang blog/package con.
2. **hotale** — label phụ trong widget đặt phòng (EN trong JS bundle).
3. **moonlit / colorlib** — string trong React/JS chưa Việt hóa.
