from marshmallow import Schema, fields, validate
from app.models.author import Author


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    biography = fields.Str()
    birth_date = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    books = fields.List(
        fields.Nested("app.schemas.book.BookSummarySchema"), dump_only=True
    )


class BookSummarySchema(Schema):
    id = fields.Int()
    title = fields.Str()
