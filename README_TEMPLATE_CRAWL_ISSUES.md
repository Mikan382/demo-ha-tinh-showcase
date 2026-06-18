# Vấn Đề Thường Gặp Khi Thay Thế Nội Dung Template Crawl

Khi crawl các template thương mại (Webflow, Framer, WordPress...) về làm demo, chúng ta thường sử dụng script để thay thế hàng loạt hình ảnh và văn bản gốc bằng nội dung tùy biến. Tuy nhiên, thao tác này thường xuyên dẫn đến tình trạng "vỡ nát" layout. Dưới đây là bảng tổng hợp các nguyên nhân cốt lõi và các tình huống phổ biến nhất.

---

## 1. Vỡ Layout Do Phụ Thuộc Kích Thước Ảnh Gốc (Intrinsic Dimension Trap)

Đây là nguyên nhân phổ biến và nghiêm trọng nhất.

*   **Nguyên nhân:** Người thiết kế template thường không thiết lập `width` và `height` cố định cho khung chứa ảnh (container). Thay vào đó, họ thả nổi container (thường dùng Flexbox) và để kích thước tự nhiên của ảnh gốc (placeholder image) quyết định chiều rộng/cao của toàn bộ bố cục. Ảnh gốc được chọn lọc cẩn thận để có tỉ lệ hoàn hảo ráp nối với nhau.
*   **Hậu quả khi thay ảnh:** Khi bạn chèn một ảnh khác có tỉ lệ (aspect ratio) khác (ví dụ: thay ảnh vuông bằng ảnh chữ nhật dọc), container sẽ bị phình to hoặc thu hẹp lại. Điều này phá vỡ cấu trúc lưới (Grid/Flexbox), tạo ra các khoảng trống lớn, đẩy các phần tử khác lệch khỏi vị trí, hoặc làm cho các hình ảnh không còn đồng đều.
*   **Cách khắc phục:** 
    *   Sử dụng CSS Grid với các tỉ lệ phân chia cột cố định (`1fr 2fr...`).
    *   Ép buộc khung chứa ảnh phải có tỉ lệ cố định (vd: `aspect-ratio: 1/1` hoặc `16/9`).
    *   Luôn luôn thêm `width: 100%; height: 100%; object-fit: cover;` cho thẻ `<img>` bên trong.

## 2. Tràn Text / Đè Lên Element Khác (Text Overflow)

*   **Nguyên nhân:** Văn bản mẫu trong template thường rất ngắn và lý tưởng (ví dụ: "John Doe", "Read More"). Container chứa text thường được set `height` cố định, hoặc các element xung quanh được canh lề dựa trên việc text chỉ có đúng 1 dòng.
*   **Hậu quả khi thay chữ:** Khi thay bằng nội dung tiếng Việt thực tế dài hơn (ví dụ: "Nguyễn Văn Chánh", "Xem chi tiết ưu đãi"), văn bản sẽ rớt xuống dòng 2 hoặc 3. Nếu container bị fix cứng chiều cao, chữ sẽ tràn ra ngoài (overflow) đè lên các nút bấm, che khuất hình ảnh, hoặc làm vỡ khung giao diện.
*   **Cách khắc phục:** Gỡ bỏ các chiều cao cố định (`height: 100px`) và thay bằng `min-height`. Xử lý overflow (`overflow: hidden`, `text-overflow: ellipsis`, `display: -webkit-box; -webkit-line-clamp: 3;` nếu cần giới hạn dòng).

## 3. Lệch Lạc Các Thành Phần Absolute Positioning

*   **Nguyên nhân:** Các nhãn (badges, ví dụ: "Sale", "New") hoặc nút bấm thường được căn chỉnh bằng CSS `position: absolute` so với kích thước gốc của ảnh (vd: cách top 20px, left 20px).
*   **Hậu quả:** Khi ảnh mới làm khung chứa phình to hoặc thu nhỏ, các thành phần absolute này có thể nằm chơ vơ giữa khung hình, lấn ra ngoài lề, hoặc đè lên phần tử quan trọng khác.
*   **Cách khắc phục:** Đảm bảo container cha có `position: relative` và kích thước ổn định (không thay đổi theo ảnh).

## 4. Bẫy CSS "Padding Hack"

*   **Nguyên nhân:** Ở các template cũ (hoặc code tay), để giữ tỉ lệ khung hình chuẩn cho ảnh (ví dụ 16:9) trước khi CSS `aspect-ratio` ra đời, người ta dùng thẻ div bọc ngoài và set `padding-top: 56.25%`. 
*   **Hậu quả:** Nếu script tự động inject CSS ép `height: 300px` lên thẻ div này, chiều cao thực tế sẽ bị cộng dồn thành `300px + 56.25% width`, khiến khung hình bị dài ngoằng một cách quái dị.
*   **Cách khắc phục:** Cần kiểm tra và loại bỏ `padding` nếu áp dụng `height` cứng, hoặc sử dụng `aspect-ratio` hiện đại thay cho padding hack.

## 5. Script Gãy Do Thiếu Hình Ảnh Nền (Background Images)

*   **Nguyên nhân:** Hình ảnh trong Webflow/Framer không chỉ nằm ở thẻ `<img>` mà thường xuyên nằm trong CSS `background-image: url(...)`.
*   **Hậu quả:** Nếu script tự động chỉ đi tìm các thẻ `<img src="...">` để thay đổi, thì giao diện sẽ còn sót lại rất nhiều ảnh gốc (thường là các ảnh hero banner lớn nhất, quan trọng nhất). Nếu script thay đổi cả `style="..."` nhưng không khớp pattern, ảnh nền sẽ mất trắng.
*   **Cách khắc phục:** Script thay thế phải regex cả các thuộc tính `style="background-image:..."` và trong file `.css` đính kèm.

## 6. Mất Hiệu Ứng Hoạt Hình (Animations / Interactions)

*   **Nguyên nhân:** Webflow IX2 (Interactions) sử dụng các class đặc biệt hoặc `data-w-id` gắn trực tiếp trên thẻ HTML để trigger hiệu ứng cuộn, hover.
*   **Hậu quả:** Khi bạn dùng script Python/DOM parser để thay đổi cấu trúc HTML bên trong (hoặc lỡ tay xóa mất các attribute này), hiệu ứng sẽ chết. Hậu quả là màn hình trắng tinh, menu không xổ xuống, hoặc ảnh bị giấu mất vì ở trạng thái ban đầu của animation ảnh có `opacity: 0`.
*   **Cách khắc phục:** Chỉ thay thế nội dung của node văn bản (text node) hoặc thuộc tính `src`, tuyệt đối không thay đổi/xóa bỏ `data-w-id` hay class của element bọc ngoài.

## 7. Sửa Sai Vì Không Đọc Code Gốc (The "Assume Before Inspect" Trap)

*   **Nguyên nhân:** Khi layout bị vỡ sau khi thay ảnh, phản xạ tự nhiên là nhìn vào kết quả trực quan rồi đoán nguyên nhân, sau đó áp đặt CSS override theo cảm tính.
*   **Hậu quả thực tế (Asatha Webflow — Instagram grid):** Template có 5 ảnh Instagram dạng lưới stagger. Sau khi thay ảnh, button "Follow" nổi sai vị trí. Qua nhiều lần fix, hết đổi `align-items`, đến thêm `flex: 1.4` cho items 2,4, đến `aspect-ratio: 2/3`, đến `aspect-ratio: 4/5`... tất cả đều sai vì bỏ qua bước đọc code gốc. Sự thật chỉ lộ ra khi đọc file CSS gốc và đo kích thước pixel ảnh gốc:
    *   CSS gốc: `.insta-image-div { position: relative; }` — **không có height, không có aspect-ratio, không có flex value nào**.
    *   Tất cả 5 ảnh gốc: **1072×1072px (1:1 square)**.
    *   Stagger chỉ đến từ `margin-top: var(--space-md)` (24px) trên items 1,3,5.
    *   Fix đúng: 3 dòng CSS — `aspect-ratio: 1/1`, `flex: 1 1 0%`, `margin-top: 24px`.
*   **Quy trình bắt buộc trước khi viết bất kỳ CSS override nào:**
    1.  **Đọc CSS gốc** — tìm rule thực tế cho element bị vỡ (không đoán).
    2.  **Đo kích thước ảnh gốc** — đọc header file hoặc dùng DevTools để biết `width × height` thật.
    3.  **Resolve CSS variables** — tra giá trị thực của `var(--space-md)`, `var(--color-X)` trong `:root`.
    4.  **Chỉ sau đó** mới viết override để khôi phục đúng hành vi gốc.
*   **Dấu hiệu đang đi sai hướng:** Nếu phải thử nhiều hơn 2 lần với giá trị khác nhau (2/3, 4/5, 3/4...) mà vẫn không khớp — dừng lại, quay về đọc source.

---

## Tổng Kết

Một template tĩnh trông có vẻ hoàn hảo nhưng cấu trúc dưới mui xe (under the hood) thường rất mỏng manh và thiết kế theo dạng **"vừa khít cho demo"**. Để tái sử dụng template crawl vào thực tế, nguyên tắc bất di bất dịch là:
👉 **Đừng bao giờ thả nổi `width/height` cho ảnh.**
👉 **Luôn kiểm soát kích thước bằng `CSS Grid/Flex` ở Container cha, và dùng `object-fit: cover` cho thẻ <img> bên trong.**
👉 **Trước khi viết CSS override: đọc CSS gốc + đo kích thước ảnh gốc. Không đoán.**
