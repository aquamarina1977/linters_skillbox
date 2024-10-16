from flask import Flask, request
from flask_restx import Api, Resource, fields
from models import get_book_by_id, update_book, delete_book, get_author_by_id, add_book, add_author, get_books_by_author_id, delete_author_and_books
from schemas import BookSchema, AuthorSchema
from marshmallow import ValidationError

app = Flask(__name__)
api = Api(app)

book_model = api.model('Book', {
    'title': fields.String(required=True, description="Title of the book"),
    'author_id': fields.Integer(required=True, description="ID of the author")
})

class BookList(Resource):
    def post(self):
        data = request.json
        book_schema = BookSchema()

        try:
            new_book = book_schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author_id = new_book['author_id']
        author = get_author_by_id(author_id)
        if not author:
            return {"message": f"Author with ID {author_id} does not exist"}, 404

        book = add_book(new_book)
        return book_schema.dump(book), 201

class BookResource(Resource):
    def get(self, book_id: int):
        book = get_book_by_id(book_id)
        if book:
            schema = BookSchema()
            return schema.dump(book), 200
        return {"message": "Book not found"}, 404

    @api.expect(book_model)
    def put(self, book_id: int):
        data = request.json
        schema = BookSchema()

        try:
            updated_book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = get_author_by_id(updated_book['author_id'])
        if not author:
            return {"message": "Author not found"}, 404

        book = update_book(book_id, updated_book)
        if book:
            return schema.dump(book), 200
        return {"message": "Book not found"}, 404

    def delete(self, book_id: int):
        if delete_book(book_id):
            return {"message": "Book deleted successfully"}, 200
        return {"message": "Book not found"}, 404

    @api.expect(book_model, partial=True)
    def patch(self, book_id: int):
        data = request.json
        schema = BookSchema(partial=True)

        try:
            updated_book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = update_book(book_id, updated_book)
        if book:
            return schema.dump(book), 200
        return {"message": "Book not found"}, 404

api.add_resource(BookResource, '/api/books/<int:book_id>')

author_model = api.model('Author', {
    'first_name': fields.String(required=True, description="First name of the author"),
    'last_name': fields.String(required=True, description="Last name of the author"),
    'middle_name': fields.String(description="Middle name of the author")
})

class AuthorResource(Resource):
    @api.expect(author_model)
    def post(self):
        data = request.json
        schema = AuthorSchema()

        try:
            new_author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(new_author)
        return schema.dump(author), 201

    def get(self, author_id: int):
        author = get_author_by_id(author_id)
        if not author:
            return {"message": "Author not found"}, 404

        books = get_books_by_author_id(author_id)
        book_schema = BookSchema(many=True)
        return {
            "author": AuthorSchema().dump(author),
            "books": book_schema.dump(books)
        }, 200

    # Удаление автора вместе с его книгами (DELETE)
    def delete(self, author_id: int):
        if delete_author_and_books(author_id):
            return {"message": "Author and all associated books deleted successfully"}, 200
        return {"message": "Author not found"}, 404

api.add_resource(AuthorResource, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    app.run(debug=True)

