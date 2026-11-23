import os
import sys
from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if os.path.isdir(SRC_DIR) and SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from customer import CustomerManager  # noqa: E402

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-de-tai-8")

DB_PATH = os.path.join(BASE_DIR, "retail_shop.db")
cm = CustomerManager(db_name=DB_PATH)


@app.route("/")
def home():
    customers = cm.get_all_customers()
    return render_template("index.html", customers=customers)


@app.route("/add", methods=["POST"])
def add_customer():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()

    if not name or not phone:
        flash("Vui lòng nhập đầy đủ tên và số điện thoại.", "warning")
        return redirect(url_for("home"))

    success, msg = cm.add_customer(
        name=name, phone=phone, email=email, address=address
    )
    flash(msg, "success" if success else "danger")
    return redirect(url_for("home"))


@app.route("/search", methods=["GET"])
def search_customer():
    query = request.args.get("phone", "").strip()
    if not query:
        flash("Vui lòng nhập số điện thoại hoặc mã KH để tìm.", "warning")
        return redirect(url_for("home"))

    customer = cm.search_customer(query)
    if customer:
        return render_template("search.html", customer=customer)

    flash("Không tìm thấy khách hàng phù hợp.", "info")
    return redirect(url_for("home"))


@app.route("/delete/<customer_id>", methods=["POST"])
def delete_customer(customer_id):
    success, msg = cm.delete_customer(customer_id, by_id=True)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("home"))


@app.route("/edit/<customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        if not name or not phone:
            flash("Tên và số điện thoại không được để trống!", "warning")
            return redirect(url_for("edit_customer", customer_id=customer_id))

        success, msg = cm.update_customer(
            customer_id, name=name, phone=phone, email=email, address=address
        )
        flash(msg, "success" if success else "danger")
        if success:
            return redirect(url_for("home"))
        return redirect(url_for("edit_customer", customer_id=customer_id))

    customer = cm.get_customer_by_id(customer_id)
    if customer is None:
        flash("Không tìm thấy khách hàng để sửa.", "danger")
        return redirect(url_for("home"))
    return render_template("edit.html", customer=customer)


@app.route("/points/<customer_id>", methods=["POST"])
def update_points(customer_id):
    action = request.form.get("action", "")
    raw_points = request.form.get("points", "0").strip()

    try:
        points = int(raw_points)
    except ValueError:
        flash("Số điểm phải là số nguyên hợp lệ.", "warning")
        return redirect(url_for("home"))

    if action == "add":
        success, msg = cm.add_points(customer_id, points)
    elif action == "redeem":
        success, msg = cm.redeem_points(customer_id, points)
    else:
        flash("Thao tác điểm không hợp lệ.", "warning")
        return redirect(url_for("home"))

    flash(msg, "success" if success else "danger")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)