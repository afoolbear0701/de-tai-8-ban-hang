const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const dbPool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'pos_system',
    waitForConnections: true,
    connectionLimit: 10
});

// 1. Lấy toàn bộ tồn kho + trạng thái cảnh báo
app.get('/api/inventory', async (req, res) => {
    try {
        const [rows] = await dbPool.query(`
            SELECT p.*, c.category_name,
            CASE
                WHEN p.stock_quantity <= 0 THEN 'OUT_OF_STOCK'
                WHEN p.stock_quantity <= p.min_stock_level THEN 'LOW_STOCK'
                ELSE 'IN_STOCK'
            END AS stock_status
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            ORDER BY p.stock_quantity ASC, p.product_id ASC
        `);
        res.json({ success: true, data: rows });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// 2. Lấy danh sách cảnh báo hàng sắp hết / hết hàng
app.get('/api/inventory/alerts', async (req, res) => {
    try {
        const [rows] = await dbPool.query(`
            SELECT product_id, barcode, product_name, stock_quantity, min_stock_level, unit
            FROM products
            WHERE stock_quantity <= min_stock_level
            ORDER BY stock_quantity ASC
        `);
        res.json({ success: true, count: rows.length, alerts: rows });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// 3. Cập nhật số lượng tồn kho (Nhập hàng / Điều chỉnh kiểm kê) & ghi log
app.post('/api/inventory/update', async (req, res) => {
    const { product_id, change_type, quantity_change, note } = req.body;
    const qtyDelta = parseInt(quantity_change, 10);

    if (!product_id || Number.isNaN(qtyDelta) || qtyDelta === 0) {
        return res.status(400).json({ success: false, message: 'Dữ liệu cập nhật tồn kho không hợp lệ!' });
    }

    const connection = await dbPool.getConnection();
    try {
        await connection.beginTransaction();

        const [currentRows] = await connection.query(
            'SELECT stock_quantity FROM products WHERE product_id = ?',
            [product_id]
        );
        if (currentRows.length === 0) {
            await connection.rollback();
            return res.status(404).json({ success: false, message: 'Không tìm thấy sản phẩm!' });
        }

        const newStock = Math.max(0, currentRows[0].stock_quantity + qtyDelta);

        await connection.query(
            'UPDATE products SET stock_quantity = ? WHERE product_id = ?',
            [newStock, product_id]
        );

        await connection.query(
            'INSERT INTO inventory_logs (product_id, change_type, quantity_change, note) VALUES (?, ?, ?, ?)',
            [product_id, change_type || 'ADJUST', qtyDelta, note || 'Cập nhật tồn kho']
        );

        await connection.commit();
        res.json({ success: true, message: 'Cập nhật tồn kho thành công!', new_stock: newStock });
    } catch (error) {
        await connection.rollback();
        res.status(500).json({ success: false, message: error.message });
    } finally {
        connection.release();
    }
});

// 4. Tra cứu sản phẩm theo Barcode / QR Code để đưa vào giỏ hàng
app.get('/api/barcode/:code', async (req, res) => {
    const code = decodeURIComponent(req.params.code || '').trim();
    try {
        const [rows] = await dbPool.query(
            'SELECT product_id, barcode, product_name, price, stock_quantity, min_stock_level, unit FROM products WHERE barcode = ?',
            [code]
        );

        if (rows.length === 0) {
            return res.status(404).json({ success: false, message: `Không tìm thấy sản phẩm với mã: ${code}` });
        }

        const product = rows[0];
        if (product.stock_quantity <= 0) {
            return res.status(400).json({ success: false, message: `Sản phẩm "${product.product_name}" đã hết hàng!` });
        }

        res.json({ success: true, product });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// 5. Kiểm tra tồn kho trước khi lập đơn / thanh toán
app.post('/api/inventory/check-stock', async (req, res) => {
    const { items } = req.body;
    if (!Array.isArray(items) || items.length === 0) {
        return res.status(400).json({ success: false, message: 'Danh sách sản phẩm kiểm tra trống!' });
    }

    try {
        const insufficientItems = [];
        for (const item of items) {
            const [rows] = await dbPool.query(
                'SELECT product_id, product_name, stock_quantity, unit FROM products WHERE product_id = ?',
                [item.product_id]
            );
            const product = rows[0];
            if (!product || product.stock_quantity < item.quantity) {
                insufficientItems.push({
                    product_id: item.product_id,
                    product_name: product ? product.product_name : 'Không tồn tại',
                    available: product ? product.stock_quantity : 0,
                    requested: item.quantity,
                    unit: product ? product.unit : ''
                });
            }
        }

        if (insufficientItems.length > 0) {
            return res.status(400).json({
                success: false,
                message: 'Không đủ tồn kho cho một số sản phẩm!',
                insufficientItems
            });
        }

        res.json({ success: true, message: 'Tất cả sản phẩm đều đủ tồn kho!' });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// 6. Trừ tồn kho sau khi thanh toán & trả về TỒN KHO MỚI
app.post('/api/inventory/checkout-deduct', async (req, res) => {
    const { order_id, items } = req.body;
    if (!Array.isArray(items) || items.length === 0) {
        return res.status(400).json({ success: false, message: 'Không có sản phẩm nào để trừ tồn!' });
    }

    const connection = await dbPool.getConnection();
    try {
        await connection.beginTransaction();
        const newInventory = [];

        for (const item of items) {
            const [rows] = await connection.query(
                'SELECT product_id, product_name, stock_quantity, unit FROM products WHERE product_id = ?',
                [item.product_id]
            );
            const product = rows[0];
            if (!product || product.stock_quantity < item.quantity) {
                await connection.rollback();
                return res.status(400).json({
                    success: false,
                    message: `Sản phẩm "${product ? product.product_name : item.product_id}" không đủ tồn kho để xuất bán!`
                });
            }

            const updatedQty = product.stock_quantity - item.quantity;
            await connection.query(
                'UPDATE products SET stock_quantity = ? WHERE product_id = ?',
                [updatedQty, item.product_id]
            );

            await connection.query(
                'INSERT INTO inventory_logs (product_id, change_type, quantity_change, note) VALUES (?, "EXPORT", ?, ?)',
                [item.product_id, -item.quantity, `Xuất bán đơn #${order_id || 'POS'}`]
            );

            newInventory.push({
                product_id: product.product_id,
                product_name: product.product_name,
                new_stock: updatedQty,
                unit: product.unit
            });
        }

        await connection.commit();
        res.json({
            success: true,
            message: 'Đã cập nhật tồn kho mới sau thanh toán!',
            new_inventory: newInventory
        });
    } catch (error) {
        await connection.rollback();
        res.status(500).json({ success: false, message: error.message });
    } finally {
        connection.release();
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Module 3 Server đang chạy tại http://localhost:${PORT}`);
});