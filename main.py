from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


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
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User")


class Offer(db.Model):
    __tablename__ = "offer"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("order.executor_id"))

    order = db.relationship('Order')


db.create_all()

users = []

with open("users.json") as file:
    users_from_json = json.load(file)

    for user in users_from_json:
        user.id = User(id=user.id, first_name=user.first_name, last_name=user.last_name, age=user.age, email=user.email,
                       role=user.role, phone=user.phone)
        users.append(user.id)

db.session.add_all(users)
db.session.commit()


if __name__ == '__main__':
    app.run()
