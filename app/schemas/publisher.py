from marshmallow import Schema, fields, validate
from app.models.publisher import Publisher


class PublisherSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    founding_year = fields.Int()
    website = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    books = fields.List(
        fields.Nested("app.schemas.book.BookSummarySchema"), dump_only=True
    )


class BookSummarySchema(Schema):
    id = fields.Int()
    title = fields.Str()
