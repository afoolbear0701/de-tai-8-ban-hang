import re
import sqlite3


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


class CustomerManager:
    def __init__(self, db_name="retail_shop.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Khởi tạo bảng customers với điểm tích lũy và hạng thành viên."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT,
                    address TEXT,
                    points INTEGER DEFAULT 0,
                    member_level TEXT DEFAULT 'Bronze'
                )
            ''')

    def _clean_text(self, value: str | None) -> str:
        return " ".join((value or "").strip().split())

    def _clean_phone(self, phone: str | None) -> str:
        return re.sub(r"\D", "", phone or "")

    def _is_valid_phone(self, phone: str) -> bool:
        """BR-CUS-03: Số điện thoại hợp lệ gồm 10-11 chữ số."""
        return bool(re.fullmatch(r"\d{10,11}", phone or ""))

    def _is_valid_email(self, email: str) -> bool:
        """BR-CUS-03: Nếu có nhập email phải đúng định dạng ten@tenmien.com."""
        if not email:
            return True
        return bool(EMAIL_REGEX.match(email))

    def generate_next_customer_id(self) -> str:
        """BR-CUS-01: Tự động sinh mã định dạng KH + 3 chữ số (KH001, KH002...)."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM customers")
            rows = cursor.fetchall()

        max_num = 0
        for (cid,) in rows:
            match = re.fullmatch(r"KH(\d{3})", (cid or "").strip().upper())
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num

        return f"KH{max_num + 1:03d}"

    def add_customer(self, name, phone, email="", address=""):
        clean_name = self._clean_text(name)
        clean_phone = self._clean_phone(phone)
        clean_email = (email or "").strip().lower()
        clean_address = self._clean_text(address)

        if len(clean_name) < 2:
            return False, "Tên khách hàng phải có ít nhất 2 ký tự."
        if not self._is_valid_phone(clean_phone):
            return False, "Số điện thoại không hợp lệ (phải gồm 10-11 chữ số)."
        if not self._is_valid_email(clean_email):
            return False, "Email không hợp lệ (ví dụ: ten@domain.com)."

        new_id = self.generate_next_customer_id()

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO customers (id, name, phone, email, address, points, member_level)
                    VALUES (?, ?, ?, ?, ?, 0, 'Bronze')
                ''', (new_id, clean_name, clean_phone, clean_email, clean_address))
            return True, f"Thêm khách hàng {clean_name} ({new_id}) thành công."
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: customers.phone" in str(e):
                return False, f"Số điện thoại {clean_phone} đã tồn tại trong hệ thống!"
            if "UNIQUE constraint failed: customers.id" in str(e):
                return False, f"ID khách hàng {new_id} đã tồn tại trong hệ thống!"
            return False, "Lỗi khi thêm khách hàng."

    def get_customer_by_id(self, customer_id):
        cid = (customer_id or "").strip().upper()
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE id = ?", (cid,))
            row = cursor.fetchone()
        if row:
            return {
                "id": row[0], "name": row[1], "phone": row[2],
                "email": row[3], "address": row[4],
                "points": row[5], "member_level": row[6],
            }
        return None

    def search_customer(self, query):
        """Tìm kiếm theo số điện thoại hoặc mã khách hàng KHxxx."""
        raw = (query or "").strip()
        upper_q = raw.upper()
        clean_phone = self._clean_phone(raw)

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if re.fullmatch(r"KH\d{3}", upper_q):
                cursor.execute("SELECT * FROM customers WHERE id = ?", (upper_q,))
            else:
                cursor.execute("SELECT * FROM customers WHERE phone = ?", (clean_phone,))
            row = cursor.fetchone()

        if row:
            return {
                "id": row[0], "name": row[1], "phone": row[2],
                "email": row[3], "address": row[4],
                "points": row[5], "member_level": row[6],
            }
        return None

    def update_customer(self, customer_id, name=None, phone=None, email=None, address=None):
        cid = (customer_id or "").strip().upper()
        clean_phone = self._clean_phone(phone) if phone is not None else None
        if clean_phone is not None and not self._is_valid_phone(clean_phone):
            return False, "Số điện thoại không hợp lệ (phải gồm 10-11 chữ số)."

        clean_email = (email or "").strip().lower() if email is not None else None
        if clean_email is not None and not self._is_valid_email(clean_email):
            return False, "Email không hợp lệ (ví dụ: ten@domain.com)."

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE id = ?", (cid,))
            if not cursor.fetchone():
                return False, f"Khách hàng với ID {cid} không tồn tại."

            fields = []
            values = []
            if name is not None:
                clean_name = self._clean_text(name)
                if len(clean_name) < 2:
                    return False, "Tên khách hàng phải có ít nhất 2 ký tự."
                fields.append("name = ?")
                values.append(clean_name)
            if clean_phone is not None:
                fields.append("phone = ?")
                values.append(clean_phone)
            if clean_email is not None:
                fields.append("email = ?")
                values.append(clean_email)
            if address is not None:
                fields.append("address = ?")
                values.append(self._clean_text(address))

            if not fields:
                return False, "Không có dữ liệu nào để cập nhật."

            values.append(cid)
            try:
                cursor.execute(f'''
                    UPDATE customers SET {", ".join(fields)} WHERE id = ?
                ''', values)
                if cursor.rowcount == 0:
                    return False, "Không cập nhật được thông tin."
                return True, "Cập nhật thông tin khách hàng thành công."
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: customers.phone" in str(e):
                    return False, f"Số điện thoại {clean_phone} đã tồn tại trong hệ thống!"
                return False, "Lỗi khi cập nhật khách hàng."

    def delete_customer(self, identifier, by_id=True):
        """BR-CUS-04: Không xóa cứng nếu khách hàng đã có điểm tích lũy."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if by_id:
                key = (identifier or "").strip().upper()
                cursor.execute("SELECT points FROM customers WHERE id = ?", (key,))
            else:
                key = self._clean_phone(identifier)
                cursor.execute("SELECT points FROM customers WHERE phone = ?", (key,))

            row = cursor.fetchone()
            if not row:
                return False, "Không tìm thấy khách hàng để xóa."
            if (row[0] or 0) > 0:
                return False, "Không thể xóa khách hàng đã có lịch sử điểm tích lũy (BR-CUS-04)."

            if by_id:
                cursor.execute("DELETE FROM customers WHERE id = ?", (key,))
            else:
                cursor.execute("DELETE FROM customers WHERE phone = ?", (key,))
            return True, "Xóa khách hàng thành công."

    def get_member_level(self, points: int) -> str:
        """BR-LVL-01: Phân hạng theo mốc điểm Bronze (0-99), Silver (100-499), Gold (500-1499), Platinum (>=1500)."""
        safe_points = max(0, int(points or 0))
        if safe_points >= 1500:
            return "Platinum"
        if safe_points >= 500:
            return "Gold"
        if safe_points >= 100:
            return "Silver"
        return "Bronze"

    def add_points(self, customer_id, points_to_add):
        cid = (customer_id or "").strip().upper()
        if points_to_add <= 0:
            return False, "Số điểm cộng thêm phải lớn hơn 0."
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT points FROM customers WHERE id = ?", (cid,))
            result = cursor.fetchone()
            if not result:
                return False, "Không tìm thấy khách hàng để cộng điểm."
            new_points = (result[0] or 0) + int(points_to_add)
            new_level = self.get_member_level(new_points)
            cursor.execute(
                "UPDATE customers SET points = ?, member_level = ? WHERE id = ?",
                (new_points, new_level, cid),
            )
            return True, f"Cộng {points_to_add} điểm thành công. Hạng hiện tại: {new_level}"

    def redeem_points(self, customer_id, points_to_use):
        cid = (customer_id or "").strip().upper()
        if points_to_use <= 0:
            return False, "Số điểm sử dụng phải lớn hơn 0."
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT points FROM customers WHERE id = ?", (cid,))
            result = cursor.fetchone()
            if not result:
                return False, "Không tìm thấy khách hàng để trừ điểm."
            current_points = result[0] or 0
            if current_points < points_to_use:
                return False, "Điểm tích lũy không đủ để sử dụng."
            new_points = current_points - int(points_to_use)
            new_level = self.get_member_level(new_points)
            cursor.execute(
                "UPDATE customers SET points = ?, member_level = ? WHERE id = ?",
                (new_points, new_level, cid),
            )
            return True, f"Trừ {points_to_use} điểm thành công. Hạng hiện tại: {new_level}"

    def get_all_customers(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers ORDER BY id")
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "phone": row[2],
                    "email": row[3],
                    "address": row[4],
                    "points": row[5],
                    "member_level": row[6],
                }
                for row in rows
            ]