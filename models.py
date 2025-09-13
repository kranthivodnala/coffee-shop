from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), default="")
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "price": self.price}

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), default="Guest")
    items = db.Column(db.String(500))  # CSV of menu item ids
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "customer_name": self.customer_name, "items": [int(i) for i in self.items.split(",") if i], "total": self.total, "created_at": self.created_at.isoformat()}

def init_db():
    db.create_all()
    # If no items, add sample menu
    if MenuItem.query.count() == 0:
        sample = [
            MenuItem(name="Espresso", description="Strong espresso shot", price=2.5),
            MenuItem(name="Cappuccino", description="Espresso + steamed milk + foam", price=3.5),
            MenuItem(name="Latte", description="Espresso + steamed milk", price=3.0),
            MenuItem(name="Blueberry Muffin", description="Fresh baked muffin", price=2.0)
        ]
        db.session.bulk_save_objects(sample)
        db.session.commit()
