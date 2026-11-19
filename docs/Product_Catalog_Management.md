1. Introduction (Phần giới thiệu)
1.1 Purpose (Mục đích)
Tài liệu này xác định và mô tả chi tiết các yêu cầu về chức năng và phi chức năng đối với Module Quản lý Sản phẩm & Danh mục (Catalog). Tài liệu làm cơ sở kỹ thuật phục vụ trực tiếp cho nhóm phát triển (Developer) viết mã nguồn, đội ngũ kiểm thử (Tester) xây dựng kịch bản kiểm tra, quản lý dự án (Project Manager) theo dõi tiến độ và bàn giao cho khách hàng.

1.2 Scope (Phạm vi)
Tên sản phẩm phần mềm: Hệ thống Quản lý Bán hàng - Module Quản lý Sản phẩm & Danh mục (Catalog).

Hệ thống sẽ làm: Cho phép thêm mới sản phẩm, chỉnh sửa giá bán, cập nhật thông tin mô tả, phân loại danh mục hàng hóa, tìm kiếm sản phẩm nhanh chóng trên giao diện bán hàng và lưu trữ dữ liệu vào cơ sở dữ liệu SQLite cục bộ.

Hệ thống sẽ không làm: Không tích hợp tính năng quản lý tồn kho đa chi nhánh/nhà kho phức tạp, không đồng bộ dữ liệu catalog qua nền tảng đám mây hay sàn thương mại điện tử bên ngoài ở phiên bản cục bộ này.

Mục tiêu và lợi ích kinh doanh: Chuẩn hóa danh mục sản phẩm và bảng giá cho cửa hàng bán lẻ, giúp nhân viên thu ngân/bán hàng tra cứu và chọn mặt hàng nhanh chóng khi tạo đơn, hỗ trợ quản lý danh mục hàng hóa gọn gàng, chính xác.

1.3 Definitions, Acronyms, and Abbreviations (Định nghĩa, từ viết tắt)
SRS: Software Requirements Specification (Tài liệu Yêu cầu Phần mềm).

FR: Functional Requirement (Yêu cầu chức năng của hệ thống).

NFR: Non-Functional Requirement (Yêu cầu phi chức năng).

Catalog: Danh mục sản phẩm và phân loại hàng hóa trong hệ thống bán hàng.

SQLite: Hệ quản trị cơ sở dữ liệu quan hệ dạng tệp cục bộ dùng cho ứng dụng desktop.

M2: Thành viên 2 (Vai trò phụ trách Module Quản lý Sản phẩm & Danh mục).

1.4 References (Tài liệu tham khảo)
Tiêu chuẩn quốc tế IEEE Std 830-1998 về lập tài liệu yêu cầu phần mềm.

Tài liệu định hướng đề tài đồ án môn học: Đề tài 8 - Hệ thống Quản lý Bán hàng.

1.5 Overview (Tổng quan tài liệu)
Cấu trúc tài liệu tiếp theo gồm: Phần 2 mô tả tổng quan góc nhìn, chức năng và ràng buộc hệ thống; Phần 3 liệt kê chi tiết các yêu cầu chức năng, hiệu năng và giao diện; Phần 4 chứa phụ lục sơ đồ UML minh họa (bao gồm Use Case Diagram và Sequence Diagram theo phân công của TV2).

2. Overall Description (Mô tả tổng quan)
2.1 Product Perspective (Góc nhìn sản phẩm)
Đây là một module thành phần cốt lõi bên trong ứng dụng Retail Management System, hoạt động như một phần mềm độc lập chạy trên máy tính cá nhân (Desktop App), kết nối trực tiếp với cơ sở dữ liệu nhúng SQLite cục bộ mà không phụ thuộc vào hệ thống đám mây bên ngoài.

2.2 Product Functions (Các chức năng chính của sản phẩm)
Quản lý danh mục hàng hóa (thêm sản phẩm mới, phân loại danh mục).

Chỉnh sửa giá bán và cập nhật thông tin mô tả sản phẩm.

Tìm kiếm và tra cứu sản phẩm nhanh chóng ngay trên giao diện bán hàng theo thời gian thực.

2.3 User Characteristics (Đặc điểm người dùng)
Nhân viên thu ngân / Bán hàng: Có kỹ năng sử dụng máy tính cơ bản, sử dụng tính năng tìm kiếm sản phẩm nhanh trên giao diện bán hàng để phục vụ khách hàng tại quầy.

Quản trị viên / Nhóm trưởng (Admin): Có chuyên môn CNTT và nghiệp vụ quản lý danh mục, chịu trách nhiệm thêm sản phẩm, sửa giá, cập nhật mô tả, phân loại danh mục và kiểm soát toàn vẹn dữ liệu catalog.

2.4 Constraints (Các ràng buộc)
Ngôn ngữ lập trình: Phát triển bằng ngôn ngữ Python (phiên bản 3.x).

Cơ sở dữ liệu: Bắt buộc sử dụng SQLite làm bộ lưu trữ cục bộ.

Thời gian và quy mô: Dự án phục vụ cho phạm vi cửa hàng bán lẻ độc lập, vận hành trên máy tính cá nhân có cấu hình thông thường.

2.5 Assumptions and Dependencies (Các giả định và phụ thuộc)
Giả định: Người quản trị nhập đúng định dạng giá bán (số dương hợp lệ) và phân loại danh mục khi thêm hoặc cập nhật sản phẩm.

Phụ thuộc: Module Quản lý Sản phẩm & Danh mục cung cấp dữ liệu sản phẩm và đơn giá cho luồng/Module Bán hàng & Đặt hàng (Order Management) khi lập hóa đơn thanh toán.

3. Specific Requirements (Yêu cầu chi tiết)
3.1 External Interfaces (Giao diện bên ngoài)
Giao diện người dùng (UI): Giao diện dạng cửa sổ ứng dụng (Desktop UI) với các thành phần: Ô tìm kiếm sản phẩm nhanh trên màn hình bán hàng, Bảng hiển thị danh sách sản phẩm/danh mục (Data Grid) và Form nhập/chỉnh sửa thông tin sản phẩm.

Giao diện phần cứng: Tương thích với màn hình độ phân giải từ HD (1366x768) trở lên, sử dụng chuột và bàn phím tiêu chuẩn.

Giao diện phần mềm: Tương tác với thư viện giao diện Python và Driver kết nối SQLite.

Giao diện truyền thông: Hoạt động cục bộ (Offline), không yêu cầu giao thức mạng phức tạp ngoại trừ việc đồng bộ mã nguồn qua Git.

3.2 Functional Requirements (Yêu cầu chức năng)
FR-P01 (Thêm sản phẩm & phân loại danh mục): Hệ thống phải cho phép thêm sản phẩm mới kèm thông tin cơ bản (Tên sản phẩm, Giá bán, Mô tả, Danh mục) và gán sản phẩm vào danh mục tương ứng.

FR-P02 (Sinh mã sản phẩm tự động): Hệ thống phải tự động tạo mã định danh duy nhất (ví dụ: SP001, SP002) cho mỗi sản phẩm mới được thêm vào.

FR-P03 (Sửa giá & cập nhật mô tả sản phẩm): Hệ thống phải cho phép cập nhật giá bán và nội dung mô tả của sản phẩm hiện có, đảm bảo lưu trữ chính xác vào cơ sở dữ liệu.

FR-P04 (Tìm kiếm sản phẩm nhanh trên giao diện bán hàng): Hệ thống phải cho phép tìm kiếm sản phẩm tức thì theo tên sản phẩm, mã sản phẩm hoặc danh mục ngay trên giao diện bán hàng.

3.3 Performance Requirements (Yêu cầu hiệu năng)
Thời gian phản hồi: Thao tác tìm kiếm sản phẩm trên giao diện bán hàng phải trả kết quả với độ trễ dưới 1 giây.

Khả năng lưu trữ: Hỗ trợ lưu trữ hiệu quả bảng danh mục sản phẩm quy mô dưới 100.000 bản ghi mà không làm chậm ứng dụng.

3.4 Logical Database Requirements (Yêu cầu cơ sở dữ liệu)
Lưu trữ dưới dạng tệp cơ sở dữ liệu quan hệ SQLite với bảng Categories (ví dụ: id, name, description) và bảng Products bao gồm các trường: id (Primary Key), code (UNIQUE), name, price, description, category_id (Foreign Key tham chiếu danh mục).

Đảm bảo tính toàn vẹn dữ liệu thông qua ràng buộc UNIQUE trên mã sản phẩm (code) và kiểm tra tính hợp lệ của trường giá (price >= 0).

3.5 Design Constraints (Ràng buộc thiết kế)
Kiến trúc mã nguồn phải tuân thủ hướng đối tượng (OOP) phân tách rõ tầng giao diện và tầng xử lý logic dữ liệu.

3.6 Software System Attributes (Các thuộc tính hệ thống)
Độ bảo mật (Security): Giới hạn quyền truy cập tệp cơ sở dữ liệu cục bộ, kiểm tra dữ liệu đầu vào chống lỗi chèn mã độc (SQL Injection).

Tính sẵn sàng (Availability): Ứng dụng khởi động nhanh chóng và hoạt động ổn định ngoại tuyến.

Khả năng bảo trì (Maintainability): Mã nguồn được chú thích rõ ràng, tuân thủ quy chuẩn đặt tên file, dễ dàng mở rộng tính năng.

Tính di động (Portability): Có thể đóng gói chạy trên các hệ điều hành phổ biến hỗ trợ Python và SQLite.

4. Appendices (Phụ lục)
Sơ đồ Use Case (Use Case Diagram): Mô tả các tác nhân (Admin, Nhân viên bán hàng) và các ca sử dụng của Module Sản phẩm & Danh mục (thêm sản phẩm, sửa giá, cập nhật mô tả, phân loại danh mục, tìm kiếm sản phẩm trên giao diện bán hàng).

Sơ đồ Tuần tự (Sequence Diagram): Mô tả luồng tương tác chi tiết giữa UI, tầng xử lý logic và SQLite cho các thao tác cốt lõi (thêm/cập nhật sản phẩm và tìm kiếm sản phẩm nhanh trên màn hình bán hàng).
