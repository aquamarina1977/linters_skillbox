from flask import jsonify, request, render_template, redirect, url_for
from models import app, db, Book, ReceivingBook, Student, Author
from datetime import datetime, timedelta, date

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


@app.route('/books', methods=['GET'])
def books():
    books = Book.query.all()
    if books:
        return jsonify([{'name': b.name, 'count': b.count, 'release_date': b.release_date.isoformat()} for b in books])
    else:
        return jsonify({'message': 'No books found'}), 404



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


@app.route('/issue_book', methods=['POST'])
def issue_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    book = Book.query.get(book_id)
    if book and book.count > 0:
        new_record = ReceivingBook(book_id=book_id, student_id=student_id)
        db.session.add(new_record)
        book.count -= 1
        db.session.commit()
        return jsonify({'message': 'Book issued successfully'}), 200
    return jsonify({'error': 'Book not available'}), 400


@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    record = ReceivingBook.query.filter_by(book_id=book_id, student_id=student_id, date_of_return=None).first()
    if record:
        record.date_of_return = datetime.utcnow()
        book = Book.query.get(book_id)
        book.count += 1
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'}), 200
    return jsonify({'error': 'Record not found'}), 400


@app.route('/search_books/<string:keyword>', methods=['GET'])
def search_books_by_keyword(keyword):
    books = Book.query.filter(Book.name.ilike(f'%{keyword}%')).all()

    if books:
        return jsonify([{
            'id': b.id,
            'name': b.name,
            'release_date': b.release_date.isoformat()
        } for b in books])
    else:
        return jsonify({'message': 'No books found matching the query'}), 404