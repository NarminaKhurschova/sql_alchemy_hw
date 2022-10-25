from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"


db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    orders = db.relationship("Order", foreign_keys=["customer_id"])
    # offers = db.relationship("Offer")


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer_user = db.relationship("User", foreign_keys=[customer_id])

    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_user = db.relationship("User", foreign_keys=[executor_id])


class Offer(db.Model):
    __tablename__ = "offer"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("order.executor_id"))

    order = db.relationship("Order")


with app.app_context():
    db.create_all()


with open("users.json") as file:
    users_from_json = json.load(file)

    for user in users_from_json:
        user_s = User(id=user["id"], first_name=user["first_name"], last_name=user["last_name"], age=user["age"],
                  email=user["email"], role=user["role"], phone=user["phone"])
        db.session.addl(user_s)
        db.session.commit()

with open("orders.json") as file_o:
    orders_from_json = json.load(file_o)

    for order in orders_from_json:
        order_s = Order(id=order["id"], name=order["name"], description=order["description"],
                        start_date=order["start_date"], end_date=order["end_date"], address=order["address"],
                        price=order["price"], customer_id=order["customer_id"], executor_id=order["executor_id"])

with open("offers.json") as file_of:
    offers_from_json = json.load(file_of)

    for offer in offers_from_json:
        offer_s = Offer(id=offer["id"], order_id=offer["order_id"], executor_id=offer["executor_id"])


if __name__ == '__main__':
    app.run()
