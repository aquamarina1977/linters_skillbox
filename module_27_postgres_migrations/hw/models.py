from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


db = SQLAlchemy()


class Coffee(Base):
    __tablename__ = "coffee"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    origin = db.Column(db.String(200))
    intensifier = db.Column(db.String(100))
    notes = db.Column(ARRAY(db.Text))


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String) #Новое поле
    patronomic = db.Column(db.String)  # Новое поле
    has_sale = db.Column(db.Boolean, default=False)
    address = db.Column(JSON)
    coffee_id = db.Column(db.Integer, db.ForeignKey("coffee.id"))
    coffee = db.relationship("Coffee")
