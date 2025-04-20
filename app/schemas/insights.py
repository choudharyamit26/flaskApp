from marshmallow import Schema, fields, validate
from app.models.insights import Insight


class InsightSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    book_id = fields.Int()
    book = fields.Nested("app.schemas.book.BookSummarySchema", dump_only=True)


class BookSummarySchema(Schema):
    id = fields.Int()
    title = fields.Str()
