# Design: Hoàn thiện catalog 9 demo — Travello crawl + cleanup

**Ngày:** 2026-06-18  
**Scope:** demo-ha-tinh-showcase  
**Mục tiêu:** Đưa catalog từ 6 demo hiển thị lên 9, thêm Travello (colorlib) làm template thứ 9.

---

## Hiện trạng

| # | Template | Status |
|---|---|---|
| 1 | travol-duruthemes | Hiển thị ✅ |
| 2 | asatha-luxury-webflow | Hiển thị ✅ |
| 3 | moonlit-react | Hiển thị ✅ |
| 4 | mountain-lodge-framer | Hiển thị ✅ |
| 5 | luxestay-framer | Hiển thị ✅ |
| 6 | colorlib-deluxe | Hiển thị ✅ |
| 7 | hotale-resort | AUDIT PASS, **ẩn** khỏi index.html |
| 8 | wanderway-framer | AUDIT PASS, **ẩn** khỏi index.html |
| 9 | travello-colorlib | Chưa crawl |

`seaside-webflow` trong `template-scrapes/` là scrape sai — đã xóa. Thay bằng Travello.

---

## Approach: Crawl-first + Song song (Approach B)

```
T=0   → [Background] node scrape.mjs travello-colorlib    # ~5-10 phút
T=0   → [Foreground] Xóa 17 variant pages khỏi hotale-resort/
T=0   → [Foreground] Thêm card hotale + wanderway vào index.html
T+10  → [Foreground] Copy scrape → demo/travello-colorlib/
        → Replace ảnh (AGENT_GUIDE travel tier)
        → Replace text → VI ("Hà Tĩnh Discovery")
        → Fix layout (checklist README_TEMPLATE_CRAWL_ISSUES.md)
        → Thêm card Travello vào index.html (#9)
```

---

## Phase 1: Cleanup variant pages — hotale-resort

**Nguyên tắc:** Giữ page type đầu tiên (default), xóa các numbered variant và with-frame.

17 files cần xóa:

```
about-us-2.html, about-us-3.html
blog-2-columns-with-frame.html, blog-3-columns-with-frame.html, blog-4-columns-with-frame.html
blog-full-both-sidebar.html, blog-full-both-sidebar-with-frame.html
blog-full-left-sidebar.html, blog-full-left-sidebar-with-frame.html
blog-full-right-sidebar.html, blog-full-right-sidebar-with-frame.html
blog-grid-2-columns-no-space.html, blog-grid-3-columns-no-space.html, blog-grid-4-columns-no-space.html
room-grid-style-2.html, room-grid-style-3.html, room-grid-style-4.html
```

travol-duruthemes: không có variant → skip.

> **Lưu ý implementation:** Grep pattern chỉ bắt được các file có suffix rõ ràng. Trước khi xóa, implementation cần kiểm tra nav links của `hotale-resort/index.html` để xác nhận danh sách đầy đủ — có thể còn thêm variants như `blog-3-columns.html`, `blog-grid-4-columns.html` không nằm trong 17 file trên.

---

## Phase 2: Thêm hotale + wanderway vào index.html

Thêm 2 card vào `<main class="grid">` trong `index.html`:

**Card hotale-resort:**
- Thumb image: `assets/shared-images/08_hospitality_hospitality_beachfront_resort.png` (IMG08)
- Tag: `Classic Resort`
- Brand: `Thiên Cầm Resort`
- Concept: `Khách sạn ven biển — phòng nghỉ, ẩm thực, booking trực tiếp.`
- Link: `hotale-resort/index.html`

**Card wanderway-framer:**
- Thumb image: `assets/shared-images/01_hero_hero_thien_cam_beach_sunrise.png` (IMG01)
- Tag: `Modern Travel`
- Brand: `Wander Hà Tĩnh`
- Concept: `Travel agency hiện đại — tour, điểm đến, đặt chỗ.`
- Link: `wanderway-framer/index.html`

---

## Phase 3: Crawl Travello

**URL:** `https://preview.colorlib.com/theme/travello/`  
**Slug:** `travello-colorlib`

Thêm vào `template-scrapes/scrape.mjs` SITES array:
```js
{ slug: 'travello-colorlib', url: 'https://preview.colorlib.com/theme/travello/' },
```

Chạy: `node scrape.mjs travello-colorlib`

**Pages crawl được:** index.html, about.html, destinations.html, tours.html, tour-single.html, services.html, news.html, contact.html

---

## Phase 4: Port Travello → demo

### 4a. Copy
```
template-scrapes/travello-colorlib/ → demo-ha-tinh-showcase/travello-colorlib/
```

### 4b. Pages cần port đầy đủ (5 core)
`index.html`, `about.html`, `destinations.html`, `tours.html`, `contact.html`

`services.html`, `news.html`, `tour-single.html` — crawl về nhưng giữ nguyên EN, không link trong nav.

### 4c. Brand & nội dung VI

- **Brand:** Hà Tĩnh Discovery
- **Hero:** "Khám phá Hà Tĩnh — hành trình của riêng bạn"
- **Sub:** "Biển Thiên Cầm, hồ Kẻ Gỗ, Ngã ba Đồng Lộc — trải nghiệm văn hóa và thiên nhiên cùng chuyên gia địa phương."
- **CTA:** "Xem tour", "Tư vấn lịch trình"
- **Menu:** Trang chủ, Giới thiệu, Điểm đến, Tour, Liên hệ

### 4d. Image mapping (travel agency tier)

Khác travol bằng cách ưu tiên eco/culture/lake để tránh trùng visual:

| Section | Images |
|---|---|
| Hero slider | IMG03, IMG37, IMG41, IMG47 (hồ/eco) |
| Destinations | IMG04, IMG05, IMG06, IMG24, IMG25, IMG42 (điểm đến văn hóa) |
| Tours/services | IMG10, IMG21, IMG22, IMG23, IMG50 (hoạt động + culture) |
| Gallery | IMG13, IMG31, IMG33, IMG52, IMG53 |
| CTA background | IMG56, IMG18 |
| Contact bg | IMG43 |

### 4e. Layout risk mitigation

Trước khi viết CSS override bất kỳ:
1. Đọc CSS gốc — tìm rule thực tế (không đoán)
2. Đo kích thước ảnh gốc Travello (inspect hoặc header file)
3. Resolve CSS variables trong `:root`
4. Chỉ sau đó viết override

Nếu thử > 2 lần giá trị khác nhau → dừng, đọc lại source.

---

## Phase 5: Thêm Travello vào index.html (#9)

**Card travello-colorlib:**
- Thumb image: `assets/shared-images/03_hero_hero_ke_go_lake_morning.png` (IMG03)
- Tag: `Discovery Travel`
- Brand: `Hà Tĩnh Discovery`
- Concept: `Hành trình khám phá — điểm đến văn hóa, eco tour, tour địa phương.`
- Link: `travello-colorlib/index.html`

---

## Checklist trước khi báo done

- [ ] index.html hiển thị đúng 9 card
- [ ] hotale-resort/index.html mở không lỗi ảnh
- [ ] wanderway-framer/index.html mở không lỗi
- [ ] travello-colorlib/index.html mở không lỗi ảnh
- [ ] Nav Travello không dẫn ra colorlib.com
- [ ] Không còn brand "Travello", "colorlib" trong 5 trang core
- [ ] Mobile không vỡ layout (resize browser 375px)
- [ ] Form contact Travello không submit thật
