from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from flask_restx import Api, Resource, fields
from models import get_book_by_id, update_book, delete_book, add_book, get_author_by_id
from schemas import BookSchema
from marshmallow import ValidationError

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

author_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "Authors API",
        "description": "API для управления авторами",
        "version": "1.0.0"
    },
    "paths": {
        "/authors": {
            "post": {
                "summary": "Добавить нового автора",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Author"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Автор успешно добавлен"
                    },
                    "400": {
                        "description": "Ошибка валидации"
                    }
                }
            }
        },
        "/authors/{author_id}": {
            "get": {
                "summary": "Получить информацию об авторе",
                "parameters": [
                    {
                        "in": "path",
                        "name": "author_id",
                        "schema": {
                            "type": "integer"
                        },
                        "required": True,
                        "description": "Идентификатор автора"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Успешный ответ"
                    },
                    "404": {
                        "description": "Автор не найден"
                    }
                }
            },
            "delete": {
                "summary": "Удалить автора и все его книги",
                "responses": {
                    "200": {
                        "description": "Автор и его книги успешно удалены"
                    },
                    "404": {
                        "description": "Автор не найден"
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Author": {
                "type": "object",
                "properties": {
                    "first_name": {
                        "type": "string",
                        "description": "Имя автора"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Фамилия автора"
                    },
                    "middle_name": {
                        "type": "string",
                        "description": "Отчество автора"
                    }
                },
                "required": ["first_name", "last_name"]
            }
        }
    }
}

book_model = api.model('Book', {
    'title': fields.String(required=True, description="Название книги"),
    'author_id': fields.Integer(required=True, description="ID автора")
})

class BookList(Resource):
    @swag_from('books_spec.yaml')
    def post(self):
        """Добавление новой книги
        ---
        responses:
          201:
            description: Книга добавлена
          400:
            description: Ошибка валидации
          404:
            description: Автор не найден
        """
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
    @swag_from('books_get_spec.yaml')
    def get(self, book_id: int):
        """Получение книги по ID
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID книги
        responses:
          200:
            description: Книга найдена
          404:
            description: Книга не найдена
        """
        book = get_book_by_id(book_id)
        if book:
            schema = BookSchema()
            return schema.dump(book), 200
        return {"message": "Book not found"}, 404

    @api.expect(book_model)
    @swag_from('books_put_spec.yaml')
    def put(self, book_id: int):
        """Обновление книги
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID книги
        requestBody:
          description: Обновляемые данные книги
          required: true
        responses:
          200:
            description: Книга обновлена
          404:
            description: Книга или автор не найдены
        """
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

    @swag_from('books_delete_spec.yaml')
    def delete(self, book_id: int):
        """Удаление книги
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID книги
        responses:
          200:
            description: Книга удалена
          404:
            description: Книга не найдена
        """
        if delete_book(book_id):
            return {"message": "Book deleted successfully"}, 200
        return {"message": "Book not found"}, 404

author_model = api.model('Author', {
    'first_name': fields.String(required=True, description="First name of the author"),
    'last_name': fields.String(required=True, description="Last name of the author"),
    'middle_name': fields.String(description="Middle name of the author")
})

class AuthorResource(Resource):
    @api.expect(author_model)
    @api.doc(author_spec)
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

    def delete(self, author_id: int):
        if delete_author_and_books(author_id):
            return {"message": "Author and all associated books deleted successfully"}, 200
        return {"message": "Author not found"}, 404
