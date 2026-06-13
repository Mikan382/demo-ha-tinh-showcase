# Demo showcase — 10 mẫu website du lịch & lưu trú Hà Tĩnh

Mở catalog: [index.html](index.html)

## Chạy local

```bash
python -m http.server 8080
```

Truy cập: http://localhost:8080/

## Cấu trúc

- `assets/shared-images/` — 60 ảnh PNG dùng chung
- `docs/` — nội dung và mapping ảnh theo template
- 9 template demo local + `webflow-bali-travel/` (limitation)

## Template

| Folder | Brand demo |
|---|---|
| travol-duruthemes | Ha Tinh Travel |
| hotale-resort | Thien Cam Resort |
| asatha-luxury-webflow | Ke Go Retreat |
| seaside-webflow | Coastal Stay Ha Tinh |
| moonlit-react | Moonlit Hotel Ha Tinh |
| wanderway-framer | Wander Hà Tĩnh |
| mountain-lodge-framer | Ke Go Eco Lodge |
| luxestay-framer | LuxeStay Ha Tinh |
| colorlib-deluxe | Deluxe Hotel Ha Tinh |
| webflow-bali-travel | Discover Ha Tinh (preview gốc only) |

Nguồn gốc crawl: `../template-scrapes/` (reference only, không sửa).

## Rà soát / sửa lại demo

```bash
python tools/deep_fix.py      # nội dung VI + ảnh theo template
python tools/fix_showcase.py  # asset hỏng, offline Framer, ẩn vendor
python tools/verify_assets.py # kiểm tra pattern lỗi phổ biến
```

Chi tiết audit: [docs/AUDIT_REPORT.md](docs/AUDIT_REPORT.md)
