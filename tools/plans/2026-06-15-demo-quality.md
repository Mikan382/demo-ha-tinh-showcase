# Demo Quality Fix — 8 Templates Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement task-by-task.

**Goal:** Đưa 8 template demo Hà Tĩnh lên chất lượng "Figma prototype" — không còn text tiếng Anh lộ, không render trắng, copy tiếng Việt tự nhiên.

**Architecture:** Tất cả sửa chữa đi qua `tools/fix_showcase.py` (pipeline idempotent). Không sửa trực tiếp HTML. Chạy `python tools/fix_showcase.py` → kiểm tra bằng screenshot Playwright sau mỗi task.

**Tech Stack:** Python 3, `fix_showcase.py` pipeline, Playwright MCP để verify, serve.py port 8765.

---

## Tổng quan vấn đề theo template

| Template | Trạng thái | Vấn đề cụ thể |
|---|---|---|
| travol-duruthemes | ✅ Tốt | Không cần fix |
| colorlib-deluxe | ✅ Tốt | Không cần fix |
| moonlit-react | ✅ Tốt | Không cần fix |
| hotale-resort | ✅ Tốt | Không cần fix |
| **mountain-lodge-framer** | ❌ Broken | 19 elements `opacity:0` inline → blank sections |
| **wanderway-framer** | ⚠️ Mix EN/VI | 3 chuỗi EN/VI lẫn lộn |
| **luxestay-framer** | ⚠️ EN body | 3 đoạn body copy còn tiếng Anh |
| **asatha-luxury-webflow** | ⚠️ EN paragraphs | 2 paragraph tiếng Anh + 1 chuỗi prefix mixed |

---

## Task 1: Fix mountain-lodge — blank sections

**Root cause:** Framer scrape đóng băng scroll animations ở trạng thái initial (`opacity: 0; transform: translateY(20px)`). Offline không có IntersectionObserver trigger → 19 sections ở lại `opacity:0`.

**File:** `tools/fix_showcase.py`

- [ ] **Step 1:** Thêm constant `MOUNTAIN_POLISH` sau `HOTALE_POLISH`:

```python
MOUNTAIN_POLISH = """<style id="mountain-polish">
/* Reveal Framer scroll-triggered sections frozen at opacity:0 in offline snapshot */
#main [style*="opacity: 0"]{opacity:1!important;transform:none!important}
</style>"""
```

- [ ] **Step 2:** Thêm inject call trong branch mountain-lodge của `process_html` (sau `fix_mountain`):

Tìm đoạn:
```python
        else:
            html = fix_mountain(html)
            html = _apply_vi_list(html, FRAMER_VI)
```

Thêm dòng `inject_head` vào sau `fix_mountain`:
```python
        else:
            html = fix_mountain(html)
            html = inject_head(html, MOUNTAIN_POLISH, "mountain-polish")
            html = _apply_vi_list(html, FRAMER_VI)
```

- [ ] **Step 3:** Chạy pipeline:
```
python tools\fix_showcase.py
```
Kết quả mong đợi: `updated N html files`

- [ ] **Step 4:** Verify bằng screenshot — navigate `http://localhost:8765/mountain-lodge-framer/` và scroll qua toàn trang. Các section phải hiện nội dung, không còn blank trắng.

---

## Task 2: Fix wanderway — 3 chuỗi EN/VI lẫn lộn

**Root cause:** FRAMER_VI thay partial words ("Traveler" → không có) → để lại artifacts. Các chuỗi cụ thể:

| Chuỗi hiện tại (broken) | Chuỗi đúng |
|---|---|
| `"One Happy Du lịcher at a Time!"` | `"Mỗi hành trình là một kỷ niệm đáng nhớ!"` |
| `"Khám phá thế giới with us: follow our social media for daily travel inspiration and updates!"` | `"Theo dõi chúng tôi để cập nhật cảm hứng du lịch và ưu đãi mới nhất từ Hà Tĩnh!"` |
| `"Let Us Take You to Đáng nhớ điểm đến!"` | `"Để chúng tôi đưa bạn đến những điểm đến đáng nhớ!"` |

**File:** `tools/fix_showcase.py` → `FRAMER_VI_EXTRA` list

- [ ] **Step 1:** Thêm 3 entry vào cuối `FRAMER_VI_EXTRA` (trước dấu `]`):

```python
    # wanderway: artifacts từ partial word replacement
    ("One Happy Du lịcher at a Time!", "Mỗi hành trình là một kỷ niệm đáng nhớ!"),
    (
        "Khám phá thế giới with us: follow our social media for daily travel inspiration and updates!",
        "Theo dõi chúng tôi để cập nhật cảm hứng du lịch và ưu đãi mới nhất từ Hà Tĩnh!",
    ),
    ("Let Us Take You to Đáng nhớ điểm đến!", "Để chúng tôi đưa bạn đến những điểm đến đáng nhớ!"),
```

- [ ] **Step 2:** Chạy pipeline + verify screenshot wanderway homepage, kiểm tra 3 heading/subheading trên.

---

## Task 3: Fix luxestay — English body copy

**Các chuỗi cần dịch:**

| Chuỗi EN | Thay bằng |
|---|---|
| `"Step outside and Hà Tĩnh begins - temples, waterfalls, rice fields, and coastline, all within reach"` | `"Bước ra ngoài là Hà Tĩnh — chùa chiền, thác nước, đồng lúa và bờ biển, tất cả đều gần tầm tay"` |
| `"Luxestay Ha Tinh is a 32-room retreat where the island does the talking and guests keep coming back to listen."` | `"LuxeStay Hà Tĩnh là khu nghỉ dưỡng ven biển với không gian được thiết kế để lắng nghe tiếng biển và trở về mỗi mùa hè."` |
| `"More than a way, a complete escape"` | `"Hơn cả một kỳ nghỉ — là lối thoát hoàn toàn"` |

**File:** `tools/fix_showcase.py` → `LUXESTAY_VI` list

- [ ] **Step 1:** Thêm 3 entry vào `LUXESTAY_VI` (sau các entry hiện có):

```python
    # luxestay: English body copy còn sót
    (
        "Step outside and Hà Tĩnh begins - temples, waterfalls, rice fields, and coastline, all within reach",
        "Bước ra ngoài là Hà Tĩnh — chùa chiền, thác nước, đồng lúa và bờ biển, tất cả đều gần tầm tay",
    ),
    (
        "Luxestay Ha Tinh is a 32-room retreat where the island does the talking and guests keep coming back to listen.",
        "LuxeStay Hà Tĩnh là khu nghỉ dưỡng ven biển với không gian được thiết kế để lắng nghe tiếng biển và trở về mỗi mùa hè.",
    ),
    ("More than a way, a complete escape", "Hơn cả một kỳ nghỉ — là lối thoát hoàn toàn"),
```

- [ ] **Step 2:** Chạy pipeline + verify screenshot luxestay homepage.

---

## Task 4: Fix asatha — English paragraphs

**Các chuỗi cần fix trong `fix_asatha_assets()`:**

| Chuỗi hiện tại | Thay bằng |
|---|---|
| `"Ke Go Retreat was created with one vision: mang đến trải nghiệm nghỉ dưỡng..."` | Xóa prefix EN → chỉ giữ phần tiếng Việt |
| `"From serene suites to curated experiences, Ke Go Retreat is more than a resort—it's a retreat for the soul. Here, every detail is thoughtfully designed to celebrate the art of living beautifully."` | Dịch hoàn toàn |

**File:** `tools/fix_showcase.py` → `fix_asatha_assets()` function

- [ ] **Step 1:** Thêm 2 `html.replace()` call vào `fix_asatha_assets()`, trước dòng `if "asatha-hide-vendor"`:

```python
    html = html.replace(
        "Ke Go Retreat was created with one vision: mang đến trải nghiệm nghỉ dưỡng cao cấp giữa thiên nhiên. Gắn với thiên nhiên và sự ấm áp — nơi mỗi khoảnh khắc đều đáng nhớ.",
        "Ke Go Retreat được tạo ra với một tầm nhìn: mang đến trải nghiệm nghỉ dưỡng cao cấp giữa thiên nhiên. Gắn với thiên nhiên và sự ấm áp — nơi mỗi khoảnh khắc đều đáng nhớ.",
    )
    html = html.replace(
        "From serene suites to curated experiences, Ke Go Retreat is more than a resort—it's a retreat for the soul. Here, every detail is thoughtfully designed to celebrate the art of living beautifully.",
        "Từ villa yên tĩnh đến những trải nghiệm được thiết kế riêng, Ke Go Retreat không chỉ là nơi nghỉ dưỡng — đây là không gian để tâm hồn tìm lại chính mình. Mỗi chi tiết đều được chăm chút để tôn vinh vẻ đẹp của sự sống.",
    )
```

- [ ] **Step 2:** Chạy pipeline + scroll asatha homepage để verify paragraph tại scroll ~800px.

---

## Task 5: Verify toàn bộ + run audit

- [ ] **Step 1:** Chạy pipeline lần cuối:
```
python tools\fix_showcase.py
```

- [ ] **Step 2:** Chạy audit:
```
python tools\audit_core.py
```
Kết quả mong đợi: `Found 0 pages with issues`

- [ ] **Step 3:** Screenshot từng template đã fix và verify:
  - `http://localhost:8765/mountain-lodge-framer/` — scroll qua → không còn blank sections
  - `http://localhost:8765/wanderway-framer/` — 3 heading fix đúng
  - `http://localhost:8765/luxestay-framer/` — body copy tiếng Việt
  - `http://localhost:8765/asatha-luxury-webflow/` — paragraphs tiếng Việt

---

## Task 6: Git init + commit

- [ ] **Step 1:** Khởi tạo git repo:
```
cd c:\scratch\demo-ha-tinh-showcase
git init
git add tools/fix_showcase.py tools/audit_core.py tools/verify_assets.py tools/plans/
git add assets/ serve.py
```

- [ ] **Step 2:** Add tất cả demo HTML (không add node_modules, temp files):
```
git add hotale-resort/ colorlib-deluxe/ moonlit-react/ wanderway-framer/ luxestay-framer/ mountain-lodge-framer/ asatha-luxury-webflow/ travol-duruthemes/
```

- [ ] **Step 3:** Commit:
```
git commit -m "feat: 8 Ha Tinh demo templates — Vietnamese copy, icon fixes, map fixes, render fixes"
```

---

## Notes quan trọng

- **Không sửa file HTML trực tiếp** — chỉ sửa `fix_showcase.py` và chạy pipeline
- **Pipeline idempotent** — chạy lại nhiều lần không làm hỏng thêm
- **mountain-lodge CSS scope**: dùng `#main` để tránh affect nav/footer có intentional opacity effects
- **Framer JS bundles** không được sửa — text trong minified JS sẽ không thay được
- **asatha `Trusted by +159,648 Customer's`** — để nguyên (UI widget, không phải editorial copy)
