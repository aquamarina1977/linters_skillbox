from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, default=1)
    release_date = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    average_score = db.Column(db.Float, nullable=False)
    scholarship = db.Column(db.Boolean, nullable=False)

    @classmethod
    def get_students_with_scholarship(cls):
        return cls.query.filter_by(scholarship=True).all()

    @classmethod
    def get_students_above_average_score(cls, score):
        return cls.query.filter(cls.average_score > score).all()


class ReceivingBook(db.Model):
    __tablename__ = 'receiving_books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    date_of_issue = db.Column(db.DateTime, nullable=False)
    date_of_return = db.Column(db.DateTime)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.utcnow() - self.date_of_issue).days



"""with app.app_context():
    db.create_all()"""
