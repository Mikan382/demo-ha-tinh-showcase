# Rà soát travol-duruthemes (6 trang core)

**Ngày:** 2026-06-13  
**Phạm vi:** `index.html`, `about.html`, `tours.html`, `destination.html`, `gallery.html`, `contact.html`  
**Spec:** `CONTENT_BY_TEMPLATE.md`, `IMAGE_MAPPING_BY_TEMPLATE.md`

## Kết luận

| Tiêu chí | Trước rà soát | Sau chỉnh (pass 1) |
|---|---|---|
| Nav / logo VI | Đạt | Đạt |
| Hero text VI | Một slide còn EN | Đạt |
| Body text VI | Nhiều EN + lorem | Đạt (core) |
| Ảnh hiển thị | blog/team/slider 404 | Đạt (`shared-images`) |
| Footer / form | Một phần EN | Đạt |
| Vendor popup | Ẩn | Đạt |

**Trạng thái hiện tại: ĐẠT cho 6 trang core** (`python tools/audit_travol.py` → PASS)

---

## Chi tiết theo trang

### index.html — Trang chủ
- Hero: "Khám phá Hà Tĩnh theo cách riêng của bạn" + ảnh IMG01/11/34
- Form tìm tour: label VI, option thời gian VI
- Tour gợi ý: Thiên Cầm, Hương Tích, Kẻ Gỗ, Đồng Lộc
- Tab điểm đến: tên thành phố EU → địa danh Hà Tĩnh
- Blog carousel: tiêu đề VI + ảnh `shared-images`
- Testimonial: tên VI, nội dung VI
- Clients logo: **ẩn** (ảnh gốc không crawl được)

### about.html — Giới thiệu
- Banner + nội dung VI
- Team 3 người: tên VI, ảnh `shared-images`
- Lorem ipsum footer → mô tả Ha Tinh Travel

### tours.html — Tour
- Danh sách tour VI, ảnh destination `shared-images`
- Footer đồng bộ

### destination.html — Điểm đến
- Banner "Điểm đến phổ biến"
- 6+ card: Thiên Cầm, Đồng Lộc, Hương Tích, Kẻ Gỗ… + ảnh đúng mapping

### gallery.html — Gallery
- Banner VI
- 6 ảnh gallery: IMG02, 31, 33, 37, 41, 53 (+ hero có sẵn)
- Video section: giữ embed YouTube/Vimeo (demo)

### contact.html — Liên hệ
- Banner "Liên hệ"
- Thông tin: Ha Tinh Travel, 0239 385 6789, contact@hatinhtravel.demo, TP. Hà Tĩnh
- Form demo-safe (`preventDefault`)
- Bản đồ: embed TP. Hà Tĩnh

---

## Vấn đề còn lại (ngoài scope core)

| Mục | Ghi chú |
|---|---|
| 12 trang phụ (`index2–4`, `blog`, `tour-details`…) | Chưa Việt hóa — không nằm trong plan Tier A |
| Link footer → `blog.html` | Trang blog vẫn EN nếu user click |
| Section clients | Ẩn CSS; ảnh logo đối tác không có trong crawl |
| Favicon | Path `duruthemes.com/.../favicon.png` — file có thể thiếu, không ảnh hưởng layout |
| Video gallery | Link YouTube gốc template (Miami…) — chỉ ảnh thumb đã đổi |

---

## Cách kiểm tra lại

```bash
cd demo-ha-tinh-showcase
python tools/deep_fix.py
python tools/audit_travol.py
python -m http.server 8080
```

Mở: `http://localhost:8080/travol-duruthemes/index.html` và 5 trang còn lại.
