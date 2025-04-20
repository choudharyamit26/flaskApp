from marshmallow import Schema, fields, validate


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    isbn = fields.Str(validate=validate.Length(equal=13))
    publication_date = fields.Date()
    price = fields.Decimal(as_string=True)
    description = fields.Str()
    author_id = fields.Int(required=True)
    publisher_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested("AuthorSummarySchema", dump_only=True)
    publisher = fields.Nested("PublisherSummarySchema", dump_only=True)


class AuthorSummarySchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()


class PublisherSummarySchema(Schema):
    id = fields.Int()
    name = fields.Str()


class BookSummarySchema(Schema):
    id = fields.Int()
    title = fields.Str()
