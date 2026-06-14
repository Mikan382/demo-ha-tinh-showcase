# Demo showcase — 8 mẫu website du lịch & lưu trú Hà Tĩnh

Mở catalog: [index.html](index.html)

## Chạy local

```bash
python -m http.server 8080
```

Truy cập: http://localhost:8080/

## Cấu trúc

- `assets/shared-images/` — 60 ảnh PNG dùng chung
- `docs/` — nội dung và mapping ảnh theo template
- 8 template demo local

## Template

| Folder | Brand demo |
|---|---|
| travol-duruthemes | Ha Tinh Travel |
| hotale-resort | Thien Cam Resort |
| asatha-luxury-webflow | Ke Go Retreat |
| moonlit-react | Moonlit Hotel Ha Tinh |
| wanderway-framer | Wander Hà Tĩnh |
| mountain-lodge-framer | Ke Go Eco Lodge |
| luxestay-framer | LuxeStay Ha Tinh |
| colorlib-deluxe | Deluxe Hotel Ha Tinh |

Nguồn gốc crawl: `../template-scrapes/` (reference only, không sửa).

## Rà soát / sửa lại demo

```bash
python tools/deep_fix.py      # nội dung VI + ảnh theo template
python tools/fix_showcase.py  # asset hỏng, offline Framer, ẩn vendor
python tools/verify_assets.py # kiểm tra pattern lỗi phổ biến
```

Chi tiết audit: [docs/AUDIT_REPORT.md](docs/AUDIT_REPORT.md)
