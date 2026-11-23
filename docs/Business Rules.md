# Business Rules (Quy tắc nghiệp vụ)
## Module: Quản lý Khách hàng & Tích điểm (Customer & Loyalty)
**Dự án:** Hệ thống Quản lý Bán hàng (Retail Management System - Đề tài 8)  
**Phụ trách:** Thành viên 1 (Nhóm trưởng / M1)  
**Cơ sở dữ liệu:** SQLite (`retail_shop.db` — bảng `customers`)  

---

## 1. Quy tắc định danh & chuẩn hóa dữ liệu khách hàng (BR-CUS)

* **BR-CUS-01 (Định dạng mã khách hàng):** Mã khách hàng (`id`) phải có định dạng cố định **`KH` + 3 chữ số** (`KH001`, `KH002`, ..., `KH999`), tự động tăng dần theo bản ghi mới nhất và không dùng lại mã đã cấp.
* **BR-CUS-02 (Tính duy nhất của số điện thoại):** Số điện thoại (`phone`) là khóa định danh nghiệp vụ duy nhất (`UNIQUE`, `NOT NULL`) trong bảng `customers`. Hệ thống từ chối tạo mới nếu số điện thoại đã tồn tại và gợi ý mở hồ sơ khách hàng hiện có.
* **BR-CUS-03 (Kiểm tra tính hợp lệ của thông tin nhập vào):**
  * `name`: Bắt buộc nhập (`NOT NULL`), độ dài tối thiểu 2 ký tự, cắt khoảng trắng dư hai đầu.
  * `phone`: Chỉ gồm chữ số, độ dài 10–11 ký tự (chuẩn số điện thoại Việt Nam).
  * `email`: Nếu có nhập, phải đúng định dạng `ten@tenmien.com` (tránh lỗi gõ thiếu ký tự tên miền).
  * `address`: Chuẩn hóa chuỗi địa chỉ trước khi lưu vào SQLite.
* **BR-CUS-04 (Xóa / vô hiệu hóa khách hàng):** Không xóa cứng (`DELETE`) bản ghi khách hàng nếu đã phát sinh đơn hàng/lịch sử tích điểm để tránh mất dữ liệu đối soát ở module thanh toán (M4) và báo cáo doanh thu (M5). Nếu cần ngừng sử dụng, chuyển trạng thái sang không hoạt động (hoặc chỉ cho phép xóa bản ghi nháp/test chưa có giao dịch).

---

## 2. Quy tắc tích điểm thưởng (BR-PNT)

* **BR-PNT-01 (Công thức tích điểm theo giá trị hóa đơn):** Khi đơn hàng hoàn tất thanh toán thành công (phối hợp với **Module Thanh toán - M4** và **POS - M5**), điểm thưởng được tính dựa trên **số tiền thực thanh toán** (sau giảm giá/voucher, không tính phần thanh toán bằng điểm nếu có quy đổi):
  * Quy ước mặc định: **10.000 VNĐ = 1 điểm** (làm tròn xuống theo số nguyên: `earned_points = int(paid_amount // 10000)`).
* **BR-PNT-02 (Giá trị khởi tạo):** Khách hàng mới tạo trong bảng `customers` luôn có `points = 0` và `member_level = 'Bronze'`.
* **BR-PNT-03 (Điều kiện cộng điểm):** Điểm chỉ được cộng khi hóa đơn ở trạng thái **Đã thanh toán** (`PAID`). Nếu hóa đơn bị hủy hoặc hoàn trả sau đó, điểm cộng từ hóa đơn tương ứng phải được trừ lại (không để âm điểm dưới `0`).

---

## 3. Quy tắc hạng thành viên & đổi điểm (BR-LVL & BR-RDM)

* **BR-LVL-01 (Phân hạng thành viên theo tổng điểm tích lũy):** Cột `member_level` trong bảng `customers` tự động cập nhật theo mốc điểm `points`:

| Hạng thành viên (`member_level`) | Mốc điểm tích lũy (`points`) | Ưu đãi áp dụng |
| :--- | :--- | :--- |
| **Bronze** (Mặc định) | `0` – `99` điểm | Tích điểm tiêu chuẩn |
| **Silver** | `100` – `499` điểm | Giảm `2%` trên giá trị đơn hàng |
| **Gold** | `500` – `1.499` điểm | Giảm `5%` trên giá trị đơn hàng |
| **Platinum** | Từ `1.500` điểm trở lên | Giảm `8%` trên giá trị đơn hàng |

* **BR-LVL-02 (Chính sách giữ hạng / hạ hạng):** Khi điểm giảm do đổi quà hoặc hoàn đơn, hệ thống đánh giá lại `member_level` dựa trên mức điểm hiện tại để đảm bảo hạng luôn khớp với `points` trong cơ sở dữ liệu.
* **BR-RDM-01 (Quy tắc sử dụng / đổi điểm):**
  * Chỉ áp dụng khi khách hàng có cung cấp số điện thoại hoặc mã `KHxxx` và đạt tối thiểu `50` điểm.
  * Quy ước quy đổi: **1 điểm = 1.000 VNĐ** cấn trừ trực tiếp vào hóa đơn (tối đa không quá `50%` giá trị đơn hàng để tránh âm tiền thanh toán).
  * Mọi thao tác cộng/trừ điểm cần thực hiện trong transaction SQLite an toàn để tránh sai lệch khi nhiều thao tác diễn ra.

---

## 4. Quy tắc phối hợp liên module (Cross-Module Rules)

| Quy tắc | Module liên quan | Nội dung phối hợp |
| :--- | :--- | :--- |
| **BR-INT-01** | **M4 (Thanh toán & Hóa đơn)** | Truyền `customer_id` (nếu có khách hàng thành viên), giá trị hóa đơn sau chiết khấu và trạng thái thanh toán để M1 cập nhật `points` và `member_level`. |
| **BR-INT-02** | **M5 (POS & Dashboard)** | Tra cứu nhanh khách hàng theo SĐT/Mã KH ngay trên màn hình bán hàng POS và hiển thị thông tin hạng thành viên/điểm hiện có. |
| **BR-INT-03** | **M3 (CSDL) & Tích hợp chung** | Thống nhất schema bảng `customers` trước khi gộp code lên nhánh chính; loại bỏ dữ liệu test sai định dạng trước khi bàn giao bản chạy chung. |