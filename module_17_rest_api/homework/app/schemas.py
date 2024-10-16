from marshmallow import Schema, fields, validates, ValidationError, post_load
from models import get_author_by_id, Book, Author


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(missing=None)

    @post_load
    def create_author(self, data: dict) -> Author:
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)

    @validates('author_id')
    def validate_author(self, author_id: int):
        if not get_author_by_id(author_id):
            raise ValidationError(f"Author with ID {author_id} does not exist.")

    @post_load
    def create_book(self, data: dict) -> Book:
        return Book(**data)


