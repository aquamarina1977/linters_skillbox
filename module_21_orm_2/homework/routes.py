import csv
from flask import jsonify, request, render_template, redirect, url_for
from models import app, db, Book, ReceivingBook, Student, Author
from datetime import datetime, timedelta, date
from sqlalchemy import func

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        name = request.form.get('name')
        author_id = request.form.get('author_id')
        release_year = request.form.get('release_date')
        count = request.form.get('count', 1)

        release_date = date(int(release_year), 1, 1)
        new_book = Book(name=name, author_id=author_id, release_date=release_date, count=count)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']

        new_author = Author(name=name, surname=surname)
        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for('get_authors'))
    return render_template('add_author.html')

@app.route('/add_receiving_book', methods=['GET', 'POST'])
def add_receiving_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        student_id = request.form['student_id']
        date_of_issue = request.form['date_of_issue']

        new_receiving = ReceivingBook(
            book_id=int(book_id),
            student_id=int(student_id),
            date_of_issue=datetime.strptime(date_of_issue, '%Y-%m-%d')
        )
        db.session.add(new_receiving)
        db.session.commit()
        return redirect(url_for('debtors'))
    return render_template('add_receiving_book.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        email = request.form['email']
        average_score = request.form['average_score']
        scholarship = request.form['scholarship']

        new_student = Student(
            name=name,
            surname=surname,
            phone=phone,
            email=email,
            average_score=float(average_score),
            scholarship=bool(int(scholarship))
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('get_students'))
    return render_template('add_student.html')

@app.route('/books', methods=['GET'])
def books():
    books = Book.query.all()
    if books:
        return jsonify([{'name': b.name, 'count': b.count, 'release_date': b.release_date.isoformat()} for b in books])
    else:
        return jsonify({'message': 'No books found'}), 404

@app.route('/debtors', methods=['GET'])
def debtors():
    fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
    debtors = ReceivingBook.query.filter(ReceivingBook.date_of_return == None, ReceivingBook.date_of_issue < fourteen_days_ago).all()
    result = []
    if debtors:
        for debtor in debtors:
            student = Student.query.get(debtor.student_id)
            book = Book.query.get(debtor.book_id)
            result.append({
                'student': f'{student.name} {student.surname}',
                'book': book.name,
                'days_with_book': debtor.count_date_with_book
            })
        return jsonify(result)
    else:
        return jsonify({'message': 'No debtors found'}), 404

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    if authors:
        return jsonify([{'id': a.id, 'name': a.name, "surname": a.surname} for a in authors])
    else:
        return jsonify({'message': 'No authors found'}), 404

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    if students:
        return jsonify([{'id': s.id, 'name': f'{s.name} {s.surname}', 'phone': s.phone, 'email': s.email} for s in students])
    else:
        return jsonify({'message': 'No students found'}), 404

@app.route('/students/upload', methods=['POST'])
def upload_students():
    file = request.files['file']
    reader = csv.DictReader(file.read().decode('utf-8').splitlines(), delimiter=';')
    students = [dict(row) for row in reader]

    db.session.bulk_insert_mappings(Student, students)
    db.session.commit()
    return "Students uploaded successfully", 201

@app.route('/books/remaining/<int:author_id>', methods=['GET'])
def get_remaining_books(author_id):
    total_books = db.session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
    return jsonify({"remaining_books": total_books if total_books else 0})

@app.route('/students/top', methods=['GET'])
def get_top_students():
    current_year = datetime.now().year
    top_students = db.session.query(ReceivingBook.student_id, func.count(ReceivingBook.book_id).label('count')).filter(
        func.strftime("%Y", ReceivingBook.date_of_issue) == str(current_year)
    ).group_by(ReceivingBook.student_id).order_by(func.count(ReceivingBook.book_id).desc()).limit(10).all()

    students = [{"student_id": student_id, "books_count": count} for student_id, count in top_students]
    return jsonify(students)

@app.route('/books/popular', methods=['GET'])
def get_popular_book():
    popular_book = db.session.query(ReceivingBook.book_id, func.count(ReceivingBook.student_id).label('count')).join(
        Student).filter(Student.average_score > 4.0).group_by(ReceivingBook.book_id).order_by(
        func.count(ReceivingBook.student_id).desc()).first()

    if popular_book:
        book_info = db.session.query(Book).get(popular_book.book_id)
        return jsonify({"book_id": popular_book.book_id, "name": book_info.name, "count": popular_book.count})
    return jsonify({"message": "No popular book found."})

@app.route('/books/average', methods=['GET'])
def get_average_books():
    current_month = datetime.now().month
    current_year = datetime.now().year

    counts = db.session.query(
        ReceivingBook.student_id, func.count(ReceivingBook.book_id).label('book_count')
    ).filter(
        func.strftime("%m", ReceivingBook.date_of_issue) == f'{current_month:02}',
        func.strftime("%Y", ReceivingBook.date_of_issue) == str(current_year)
    ).group_by(ReceivingBook.student_id).all()

    book_counts = [count.book_count for count in counts]

    if book_counts:
        average_books = sum(book_counts) / len(book_counts)
        return jsonify({"average_books": average_books})

    return jsonify({"average_books": 0})
