# Ha Tinh Travel Showcase

Dự án này là bộ sưu tập các template website (Webflow, Framer, HTML thuần...) được crawl và tùy biến lại thành hệ thống giao diện mẫu phục vụ cho chiến dịch quảng bá du lịch, nghỉ dưỡng tại tỉnh Hà Tĩnh (như Thiên Cầm, Kẻ Gỗ, Đồng Lộc, Hương Tích).

## Tổng quan các Template

Thư mục `demo-ha-tinh-showcase` bao gồm nhiều giao diện đa dạng, từ trang giới thiệu resort sang trọng đến các nền tảng đặt tour du lịch:

- `asatha-luxury-webflow`: Template resort cao cấp, đã tích hợp fix lỗi grid và layout chuyên sâu cho Webflow.
- `travol-duruthemes`: Template đặt tour du lịch hiện đại, tối ưu hiển thị danh sách các điểm đến.
- `hotale-resort`: Giao diện khách sạn/resort cổ điển, thanh lịch.
- Các hệ thống Webflow/Framer/React khác (như `moonlit-react`, `luxestay-framer`, `colorlib-deluxe`...).

## Các Tuỳ chỉnh & Cải tiến đã thực hiện (Post-Crawl Fixes)

Để giải quyết các vấn đề thường gặp khi thay thế tự động hình ảnh và nội dung tiếng Việt vào template gốc (dẫn tới lỗi vỡ layout, tràn chữ), chúng tôi đã tiến hành Audit và chuẩn hóa lại toàn bộ codebase:

### 1. Chuẩn hóa Navigation & Cấu trúc Menu
Hợp nhất menu trên toàn bộ các trang thành một cấu trúc chuẩn nhất quán, bao gồm 6 mục:
1. Trang chủ
2. Giới thiệu
3. Phòng/Tour
4. Ẩm thực
5. Thư viện
6. Liên hệ

Mọi trang HTML sinh thừa (nhân bản nội dung) hay các mục lục dư thừa do parser tự tạo đều đã được gỡ bỏ sạch sẽ.

### 2. Sửa lỗi Vỡ Layout do Ảnh (Image Proportions)
Các template tĩnh thường thiết kế dựa trên tỉ lệ vàng của ảnh gốc. Để ngăn chặn lỗi phình to container khi thêm ảnh có kích thước đa dạng:
- Áp dụng class `.auto-crop-image` cho tất cả các ảnh Thumbnail/Grid.
- Sử dụng thuộc tính `width: 100% !important; aspect-ratio: 4/3 !important; object-fit: cover !important;` giúp hình ảnh hiển thị sắc nét, đồng đều trên mọi thiết bị.

### 3. Sửa lỗi Tràn chữ (Text Overflow)
Văn bản tiếng Việt thường dài hơn tiếng Anh, gây tràn dòng và đè lên các nút tương tác (điển hình ở `travol-duruthemes` và lưới bài viết).
- Các thẻ Heading (tiêu đề tour, tên resort) đã được giới hạn cứng bằng CSS (`-webkit-line-clamp: 2`, `text-overflow: ellipsis`, `display: -webkit-box`).
- Xử lý các container có chiều cao cố định (`height`) bị lỗi overflow, đảm bảo tính thẩm mỹ cho trạng thái `hover`.

### 4. Khôi phục & Bảo vệ Hiệu ứng (Animations)
Các hiệu ứng cuộn, hover phức tạp (đặc biệt của Webflow IX2) yêu cầu giữ nguyên các thuộc tính định danh. 
- Mọi logic tùy biến nội dung đã được khoanh vùng ở cấp node văn bản và `src` ảnh.
- Thuộc tính `data-w-id` và hệ thống class của Webflow được bảo vệ 100%, bảo đảm web vận hành mượt mà với đầy đủ hiệu ứng như bản gốc.

---

> _Tài liệu tham chiếu chi tiết về quá trình sửa lỗi CSS và các trick xử lý Webflow/Framer có tại file `README_TEMPLATE_CRAWL_ISSUES.md`._
