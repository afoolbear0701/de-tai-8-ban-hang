CREATE DATABASE IF NOT EXISTS pos_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pos_system;

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(200) NOT NULL,
    category_id INT,
    price DECIMAL(12, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    min_stock_level INT NOT NULL DEFAULT 10,
    unit VARCHAR(30) DEFAULT 'Cái',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

CREATE TABLE inventory_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    change_type ENUM('IMPORT', 'EXPORT', 'ADJUST') NOT NULL,
    quantity_change INT NOT NULL,
    note VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE,
    loyalty_points INT DEFAULT 0
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'CASH',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL
);

CREATE TABLE order_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Dữ liệu mẫu phục vụ kiểm thử kho, cảnh báo & barcode demo
INSERT INTO categories (category_name, description) VALUES
('Đồ uống', 'Nước giải khát, nước suối, cà phê lon'),
('Bánh kẹo', 'Bánh quy, snack, kẹo'),
('Nhu yếu phẩm', 'Mì ăn liền, gia vị, đồ dùng thiết yếu');

INSERT INTO products (barcode, product_name, category_id, price, stock_quantity, min_stock_level, unit) VALUES
('8934588012228', 'Nước ngọt Coca-Cola 330ml', 1, 10000, 50, 15, 'Lon'),
('8934563138165', 'Mì Hảo Hảo Tôm Chua Cay', 3, 4500, 8, 20, 'Gói'),
('8936036021127', 'Bánh Oreo Vani 133g', 2, 18000, 3, 10, 'Hộp'),
('8935049500544', 'Nước suối Aquafina 500ml', 1, 5000, 100, 20, 'Chai'),
('QR_SP005', 'Cà phê sữa Highlands Lon 235ml', 1, 14000, 0, 10, 'Lon');

INSERT INTO inventory_logs (product_id, change_type, quantity_change, note) VALUES
(1, 'IMPORT', 50, 'Nhập hàng ban đầu'),
(2, 'IMPORT', 28, 'Nhập hàng ban đầu'),
(2, 'EXPORT', -20, 'Bán lẻ trước đó'),
(3, 'IMPORT', 15, 'Nhập hàng ban đầu'),
(3, 'EXPORT', -12, 'Bán lẻ trước đó'),
(4, 'IMPORT', 100, 'Nhập hàng ban đầu');