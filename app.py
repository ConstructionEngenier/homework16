import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import raw_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order = db.relationship("Order", foreign_keys=[order_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


db.create_all()

for user_data in raw_data.users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()

for order_data in raw_data.orders:
    new_order = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"],
    )
    db.session.add(new_order)
    db.session.commit()

for offer_data in raw_data.offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"],
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route('/users', methods=["POST", "GET"])
def get_all_users():
    if request.method == "GET":
        users = []
        for user in User.query.all():
            users.append(user.to_dict())
        return jsonify(users), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 201


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(user_id: int):
    if request.method == "GET":
        return jsonify(User.query.get(user_id).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        user = User.query.get(user_id)
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.age = user_data["age"]
        user.email = user_data["email"]
        user.role = user_data["role"]
        user.phone = user_data["phone"]
        db.session.add(user)
        db.session.commit()
        return "", 204
    elif request.method == "DELETE":
        user = User.query.get(user_id)
        db.session.delete (user)
        db.session.commit()
        return "", 204


@app.route('/orders', methods=["POST", "GET"])
def get_all_orders():
    if request.method == "GET":
        orders = []
        for order in Order.query.all():
            orders.append(order.to_dict())
        return jsonify(orders), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        orders_data = json.loads(request.data)
        new_order = Order(
            id=orders_data["id"],
            name=orders_data["name"],
            description=orders_data["description"],
            start_date=orders_data["start_date"],
            end_date=orders_data["end_date"],
            address=orders_data["address"],
            price=orders_data["price"],
            customer_id=orders_data["customer_id"],
            executor_id=orders_data["executor_id"],
        )
        db.session.add(new_order)
        db.session.commit()
        return "", 201


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_order(order_id: int):
    if request.method == "GET":
        return jsonify(Order.query.get(order_id).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "PUT":
        orders_data = json.loads(request.data)
        order = Order.query.get(order_id)
        order.name = orders_data["name"]
        order.description = orders_data["description"]
        order.start_date = orders_data["start_date"]
        order.end_date = orders_data["end_date"]
        order.address = orders_data["address"]
        order.price = orders_data["price"]
        order.customer_id = orders_data["customer_id"]
        order.executor_id = orders_data["executor_id"]
        db.session.add(order)
        db.session.commit()
        return "", 204
    elif request.method == "DELETE":
        order = Order.query.get(order_id)
        db.session.delete (order)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True, port=5002)
