from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import random
from models import db, User, Coffee
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/skillbox_db")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


def populate_database():
    with app.app_context():
        if User.query.first() or Coffee.query.first():
            print("Database already populated")
            return

        coffees = []
        for _ in range(10):
            response = requests.get("https://random-data-api.com/api/coffee/random_coffee")
            if response.status_code == 200:
                coffee_data = response.json()
                coffee = Coffee(
                    title=coffee_data["blend_name"],
                    origin=coffee_data["origin"],
                    intensifier=coffee_data["intensifier"],
                    notes=coffee_data["notes"].split(", ")
                )
                db.session.add(coffee)
                coffees.append(coffee)

        db.session.commit()

        for _ in range(10):
            response = requests.get("https://random-data-api.com/api/address/random_address")
            if response.status_code == 200:
                address_data = response.json()
                user = User(
                    name=f"User_{random.randint(1, 1000)}",
                    has_sale=random.choice([True, False]),
                    address={
                        "street": address_data["street_address"],
                        "city": address_data["city"],
                        "state": address_data["state"],
                        "country": address_data["country"]
                    },
                    coffee_id=random.choice(coffees).id
                )
                db.session.add(user)

        db.session.commit()
        print("Database populated")

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    if not data or "name" not in data or "address" not in data or "coffee_id" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = User(
        name=data["name"],
        has_sale=data.get("has_sale", False),
        address=data["address"],
        coffee_id=data["coffee_id"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "name": new_user.name, "coffee": new_user.coffee.title}), 201


@app.route("/search_coffee", methods=["GET"])
def search_coffee():
    query = request.args.get("query")
    result = Coffee.query.filter(Coffee.title.ilike(f"%{query}%")).all()
    return jsonify([{"id": c.id, "title": c.title} for c in result])


@app.route("/unique_notes", methods=["GET"])
def unique_notes():
    all_notes = db.session.query(Coffee.notes).all()
    unique_notes = set(note for sublist in all_notes for note in sublist[0] if sublist[0])
    return jsonify(list(unique_notes))


@app.route("/users_by_country", methods=["GET"])
def users_by_country():
    country = request.args.get("country")
    users = User.query.filter(User.address["country"].astext == country).all()
    return jsonify([{"id": u.id, "name": u.name, "country": u.address['country']} for u in users])


if __name__ == "__main__":
    populate_database()
    app.run(debug=True, host="0.0.0.0", port=8000)

