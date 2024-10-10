from flask import Flask, render_template, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from models import init_db, get_all_books, add_book, get_books_by_author, DATA, increment_book_views, get_book_by_id

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class BookForm(FlaskForm):
    book_title = StringField('Book title', validators=[InputRequired()])
    author_name = StringField('Author full name', validators=[InputRequired()])
    submit = SubmitField('Add new book')

@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    form = BookForm()
    if form.validate_on_submit():
        book_title = form.book_title.data
        author_name = form.author_name.data
        add_book(book_title, author_name)
        flash('Book successfully added!', 'success')
        return redirect('/books')
    return render_template('add_book.html', form=form)


@app.route('/books_by_author', methods=['GET'])
def books_by_author_form():
    return render_template('author_search_form.html')

@app.route('/books_by_author_results', methods=['POST'])
def books_by_author_results():
    author_name = request.form.get('author_name')
    if not author_name:
        return "Author name is required", 400

    books = get_books_by_author(author_name)
    return render_template('author_books.html', author_name=author_name, books=books)

@app.route('/books')
def all_books():
    books = get_all_books()
    return render_template('index.html', books=books)

@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = get_book_by_id(book_id)
    if book:
        increment_book_views(book.id)
        return render_template('book_detail.html', book=book)
    flash('Book not found', 'error')
    return redirect('/books')

if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
