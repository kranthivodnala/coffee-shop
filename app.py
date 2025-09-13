from flask import Flask, jsonify, request, render_template, send_from_directory
from models import db, MenuItem, Order, init_db
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
db_file = os.environ.get("DATABASE_URL", "sqlite:///coffee_shop.db")
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    init_db()

# ----- Frontend route -----
@app.route("/")
def index():
    return render_template("index.html")

# Static files (JS/CSS) served from /static by Flask automatically.

# ----- Menu endpoints -----
@app.route("/api/menu", methods=["GET"])
def list_menu():
    items = MenuItem.query.all()
    return jsonify([item.to_dict() for item in items]), 200

@app.route("/api/menu", methods=["POST"])
def create_menu_item():
    data = request.json or {}
    name = data.get("name")
    price = data.get("price")
    description = data.get("description", "")
    if not name or price is None:
        return jsonify({"error": "name and price required"}), 400
    item = MenuItem(name=name, price=float(price), description=description)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route("/api/menu/<int:item_id>", methods=["GET"])
def get_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200

@app.route("/api/menu/<int:item_id>", methods=["PUT"])
def update_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    data = request.json or {}
    item.name = data.get("name", item.name)
    if "price" in data:
        item.price = float(data["price"])
    item.description = data.get("description", item.description)
    db.session.commit()
    return jsonify(item.to_dict()), 200

@app.route("/api/menu/<int:item_id>", methods=["DELETE"])
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"deleted": item_id}), 200

# ----- Orders endpoints -----
@app.route("/api/orders", methods=["GET"])
def list_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders]), 200

@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.json or {}
    items = data.get("items")  # expected: list of menu item ids
    customer = data.get("customer", "Guest")
    if not items or not isinstance(items, list):
        return jsonify({"error": "items (list of menu item ids) required"}), 400
    # Validate items and compute total
    menu_items = MenuItem.query.filter(MenuItem.id.in_(items)).all()
    if len(menu_items) != len(items):
        return jsonify({"error": "one or more menu item ids invalid"}), 400
    total = sum(mi.price for mi in menu_items)
    order = Order(customer_name=customer, total=float(total), items=",".join(map(str, items)))
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict()), 200

# Health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))