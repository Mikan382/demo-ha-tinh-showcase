# Rà soát colorlib-deluxe (5 trang core)

**Ngày:** 2026-06-12  
**Phạm vi:** `index.html`, `about.html`, `rooms.html`, `restaurant.html`, `contact.html`  
**Brand:** Deluxe Hotel Ha Tinh — khách sạn phổ thông, dễ dùng

## Kết luận: ĐẠT

`python tools/audit_colorlib_wanderway.py` → COLORLIB PASS

---

## Theo trang

| Trang | Hero / tiêu đề | Ảnh (mapping) | Ghi chú |
|---|---|---|---|
| `index.html` | Lựa chọn lưu trú tiện nghi tại Hà Tĩnh | IMG08/17 hero; phòng IMG09/29/45/60 | Nav VI 5 mục |
| `about.html` | Giới thiệu khách sạn | shared-images | Counter VI |
| `rooms.html` | Danh sách phòng, giá VNĐ | Phòng → shared-images | |
| `restaurant.html` | Thực đơn, nhà hàng | IMG26/40 menu | Lorem đã thay |
| `contact.html` | Liên hệ Thiên Cầm | og/hero | Form demo-safe |

---

## Đã sửa trong pass này

- `COLORLIB_VI` + `COLORLIB_IMG`: map toàn bộ `images/*` → `shared-images` (menu-1..8, about.jpg)
- Hero, form booking, giá USD → VNĐ, room names VI
- Gỡ script `preview.colorlib.com/s9cc`, timepicker CSS/JS
- Sửa path insta `preview.colorlib.com/.../shared-images` → đúng relative
- Lorem / Little Blind Text → nội dung VI

## Ngoài scope core

- `blog.html`, `blog-single.html`, `room-single.html` chưa audit từng trang
- Google Maps embed contact vẫn có thể báo lỗi API (demo)

## Kiểm tra lại

```bash
cd demo-ha-tinh-showcase
python tools/deep_fix.py
python tools/audit_colorlib_wanderway.py
python -m http.server 8080
# http://localhost:8080/colorlib-deluxe/index.html
```
