# Software Requirements Specification (SRS)
## Module: Quản lý Khách hàng & Tích điểm (Customer & Loyalty)
**Dự án:** Hệ thống Quản lý Bán hàng (Retail Management System - Đề tài 8)  
**Nhóm trưởng / M1:** Nguyễn Trần Minh Quân  

---

## 1. Introduction (Phần giới thiệu)
### 1.1 Purpose (Mục đích)
Tài liệu này xác định và mô tả chi tiết các yêu cầu về chức năng và phi chức năng đối với **Module Quản lý Khách hàng & Tích điểm (M1)**[cite: 1, 2]. Tài liệu làm cơ sở kỹ thuật phục vụ trực tiếp cho nhóm phát triển viết mã nguồn, kiểm thử chức năng, đồng bộ tích hợp với các module khác và theo dõi tiến độ đồ án[cite: 1, 2].

### 1.2 Scope (Phạm vi)
- **Tên sản phẩm phần mềm:** Hệ thống Quản lý Bán hàng - Module Quản lý Khách hàng & Tích điểm[cite: 1, 2].
- **Hệ thống sẽ làm:** Cho phép thêm mới khách hàng (tự động sinh mã `KHxxx`), tìm kiếm tra cứu nhanh theo số điện thoại hoặc mã khách hàng, cập nhật thông tin liên lạc, quản lý xóa bản ghi theo điều kiện điểm tích lũy, cộng/đổi điểm và cập nhật hạng thành viên (`Bronze`, `Silver`, `Gold`, `Platinum`) lưu trên cơ sở dữ liệu SQLite cục bộ (`retail_shop.db`)[cite: 1, 2, 6, 12].
- **Hệ thống sẽ không làm:** Không tích hợp gửi tin nhắn SMS/Email tự động qua nhà mạng bên thứ ba hoặc thanh toán trực tuyến qua cổng ngân hàng ở phiên bản cục bộ này[cite: 1, 2].
- **Mục tiêu và lợi ích kinh doanh:** Chuẩn hóa dữ liệu khách hàng cho cửa hàng bán lẻ, giúp tra cứu nhanh khi thanh toán đơn hàng và duy trì chương trình khách hàng thân thiết minh bạch, nhất quán[cite: 1, 2].

### 1.3 Definitions, Acronyms, and Abbreviations (Định nghĩa, từ viết tắt)
- **SRS:** Software Requirements Specification (Tài liệu Yêu cầu Phần mềm)[cite: 1, 2].
- **FR:** Functional Requirement (Yêu cầu chức năng của hệ thống)[cite: 1, 2].
- **NFR:** Non-Functional Requirement (Yêu cầu phi chức năng)[cite: 1, 2].
- **SQLite:** Hệ quản trị cơ sở dữ liệu quan hệ dạng tệp cục bộ (`retail_shop.db`)[cite: 1, 2, 12].
- **M1:** Thành viên 1 (Vai trò Nhóm trưởng kiêm phụ trách Module Quản lý Khách hàng & Tích điểm)[cite: 1, 2].
- **M3 / M4 / M5:** Các module phối hợp trong hệ thống (CSDL & tích hợp chung, Thanh toán & Hóa đơn, POS & Dashboard)[cite: 1].

### 1.4 References (Tài liệu tham khảo)
- Tiêu chuẩn quốc tế IEEE Std 830-1998 về lập tài liệu yêu cầu phần mềm[cite: 1, 2].
- Tài liệu định hướng đề tài đồ án môn học: *Đề tài 8 - Hệ thống Quản lý Bán hàng*[cite: 1, 2].
- Tài liệu quy tắc nghiệp vụ: `docs/Business_Rules.md` (`BR-CUS`, `BR-PNT`, `BR-LVL`, `BR-RDM`, `BR-INT`)[cite: 1].

### 1.5 Overview (Tổng quan tài liệu)
Cấu trúc tài liệu gồm 4 phần: Phần 1 giới thiệu mục đích và phạm vi; Phần 2 mô tả tổng quan hệ thống, người dùng, ràng buộc và phụ thuộc; Phần 3 quy định chi tiết giao diện, chức năng, hiệu năng, cơ sở dữ liệu và thuộc tính hệ thống; Phần 4 chứa phụ lục các sơ đồ mô hình hóa[cite: 1, 2].

---

## 2. Overall Description (Mô tả tổng quan)
### 2.1 Product Perspective (Góc nhìn sản phẩm)
Đây là một module thành phần cốt lõi bên trong ứng dụng **Retail Management System**, được xây dựng bằng Python/Flask và kết nối trực tiếp với cơ sở dữ liệu nhúng SQLite cục bộ (`retail_shop.db`), phục vụ cả chạy kiểm thử độc lập module và tích hợp vào hệ thống chung của nhóm[cite: 1, 2, 5, 12].

### 2.2 Product Functions (Các chức năng chính của sản phẩm)
- Quản lý thông tin chi tiết cá nhân khách hàng và tự động sinh mã `KHxxx`[cite: 1, 2].
- Tra cứu, tìm kiếm khách hàng theo số điện thoại hoặc mã khách hàng[cite: 1, 2].
- Cập nhật thông tin liên lạc và kiểm soát xóa bản ghi theo quy tắc nghiệp vụ[cite: 1, 2].
- Cộng điểm, đổi điểm và cập nhật hạng thành viên (`Bronze`, `Silver`, `Gold`, `Platinum`)[cite: 1].

### 2.3 User Characteristics (Đặc điểm người dùng)
- **Nhân viên thu ngân / Bán hàng:** Có kỹ năng sử dụng máy tính cơ bản, thực hiện thêm khách hàng, tra cứu thông tin và thao tác tích/đổi điểm tại quầy[cite: 1, 2].
- **Quản trị viên / Nhóm trưởng (M1):** Có chuyên môn CNTT, quản lý cấu trúc cơ sở dữ liệu, kiểm soát toàn vẹn dữ liệu và phối hợp tích hợp với các module khác[cite: 1, 2].

### 2.4 Constraints (Các ràng buộc)
- **Ngôn ngữ lập trình:** Phát triển bằng ngôn ngữ Python (phiên bản 3.x) và Flask[cite: 1, 2, 5].
- **Cơ sở dữ liệu:** Bắt buộc sử dụng SQLite (`retail_shop.db`) làm bộ lưu trữ cục bộ[cite: 1, 2, 12].
- **Thời gian và quy mô:** Phục vụ phạm vi cửa hàng bán lẻ độc lập, vận hành trên máy tính cá nhân và đồng bộ mã nguồn qua Git/GitHub[cite: 1, 2].

### 2.5 Assumptions and Dependencies (Các giả định và phụ thuộc)
- **Giả định:** Người dùng nhập chính xác thông tin định danh và số điện thoại duy nhất cho mỗi khách hàng[cite: 1, 2].
- **Phụ thuộc:**
  - Phối hợp với **M4 (Thanh toán & Hóa đơn)** và **M5 (POS & Dashboard)** để cập nhật điểm/hạng thành viên và tra cứu khách hàng nhanh khi bán hàng[cite: 1].
  - Phối hợp với **M3 (CSDL) & tích hợp chung** để thống nhất schema bảng `customers` trước khi gộp code lên nhánh chính[cite: 1].

---

## 3. Specific Requirements (Yêu cầu chi tiết)
### 3.1 External Interfaces (Giao diện bên ngoài)
- **Giao diện người dùng (UI):** Giao diện web HTML phục vụ qua Flask (`index.html`, `edit.html`, `search.html`) gồm form thêm khách hàng, ô tìm kiếm, bảng danh sách khách hàng, nút sửa/xóa, form tích/đổi điểm và thông báo phản hồi[cite: 1, 2, 5, 7, 8, 9].
- **Giao diện phần cứng:** Tương thích với màn hình độ phân giải từ HD (1366x768) trở lên, sử dụng chuột và bàn phím tiêu chuẩn[cite: 1, 2].
- **Giao diện phần mềm:** Tương tác giữa `app.py`, `CustomerManager` (`src/customer.py`) và driver SQLite chuẩn (`sqlite3`)[cite: 1, 2, 5, 6].
- **Giao diện truyền thông:** Hoạt động cục bộ (Offline), đồng bộ mã nguồn qua Git/GitHub[cite: 1, 2].

### 3.2 Functional Requirements (Yêu cầu chức năng)
- **FR-C01 (Thêm khách hàng):** Hệ thống cho phép thêm mới khách hàng khi nhập hợp lệ họ tên (tối thiểu 2 ký tự) và số điện thoại (10–11 chữ số, duy nhất), kiểm tra định dạng email nếu có nhập, khởi tạo mặc định `points = 0` và `member_level = 'Bronze'`[cite: 1, 2, 3, 6].
- **FR-C02 (Sinh mã tự động):** Hệ thống tự động tạo mã định danh theo định dạng `KH` + 3 chữ số (`KH001`, `KH002`, ...) tăng dần và không dùng lại mã đã cấp[cite: 1, 2, 3, 6].
- **FR-C03 (Tìm kiếm khách hàng):** Hệ thống trả về kết quả tra cứu chính xác khi người dùng tìm theo số điện thoại hoặc mã khách hàng `KHxxx`[cite: 1, 2, 3].
- **FR-C04 (Cập nhật và xóa khách hàng):** Hệ thống cho phép cập nhật thông tin khách hàng, kiểm tra trùng số điện thoại và chặn xóa cứng nếu khách hàng đã có điểm tích lũy (`points > 0`)[cite: 1, 6].
- **FR-C05 (Tích/đổi điểm & phân hạng):** Hệ thống hỗ trợ cộng/trừ điểm và tự động cập nhật `member_level` theo mốc điểm (`Bronze`, `Silver`, `Gold`, `Platinum`)[cite: 1, 6].

### 3.3 Performance Requirements (Yêu cầu hiệu năng)
- **Thời gian phản hồi:** Thao tác thêm, tra cứu, cập nhật và tính điểm hoàn tất với độ trễ dưới 1 giây[cite: 1, 2].
- **Khả năng lưu trữ:** Hỗ trợ lưu trữ hiệu quả bảng `customers` quy mô dưới 100.000 bản ghi trên môi trường cục bộ[cite: 1, 2].

### 3.4 Logical Database Requirements (Yêu cầu cơ sở dữ liệu)
- Lưu trữ trong tệp cơ sở dữ liệu SQLite (`retail_shop.db`) với bảng `customers` gồm các trường: `id` (Primary Key), `name` (`NOT NULL`), `phone` (`UNIQUE`, `NOT NULL`), `email`, `address`, `points` (`INTEGER DEFAULT 0`), `member_level` (`TEXT DEFAULT 'Bronze'`)[cite: 1, 2, 6, 12].

### 3.5 Design Constraints (Ràng buộc thiết kế)
- Phân tách rõ tầng xử lý nghiệp vụ & CSDL (`CustomerManager` trong `src/customer.py`), tầng điều hướng (`app.py`) và tầng hiển thị (`templates/*.html`)[cite: 1, 5, 6, 7, 8, 9].

### 3.6 Software System Attributes (Các thuộc tính hệ thống)
- **Độ bảo mật (Security):** Sử dụng câu lệnh SQL tham số hóa (`?`) để chống SQL Injection, chuẩn hóa và kiểm tra dữ liệu đầu vào[cite: 1, 2, 6].
- **Tính sẵn sàng (Availability):** Tự động khởi tạo bảng nếu chưa có (`CREATE TABLE IF NOT EXISTS`) và hoạt động ổn định ngoại tuyến[cite: 1, 2, 6].
- **Khả năng bảo trì (Maintainability):** Mã nguồn rõ ràng, đặt tên nhất quán, tuân thủ quy chuẩn đặt tên file và dễ mở rộng[cite: 1, 2].
- **Tính di động (Portability):** Chạy được trên các môi trường hỗ trợ Python 3.x và SQLite[cite: 1, 2, 6].

---

## 4. Appendices (Phụ lục)
- **Sơ đồ Use Case (Use Case Diagram):** 
- **Sơ đồ Quan hệ Thực thể (ERD - Entity Relationship Diagram):** 
- **Sơ đồ Tuần tự (Sequence Diagram):**
- **Sơ đồ hoạt động (Activity Diagram - Luồng thêm khách hàng):** 