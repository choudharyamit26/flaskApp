from quart import Blueprint, request, jsonify
from quart_jwt_extended import jwt_required
from app.services.book_service import BookService
from app.schemas.book import BookSchema
from marshmallow import ValidationError

books_bp = Blueprint("books", __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@books_bp.route("", methods=["GET"])
async def get_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    title = request.args.get("title", "")
    if title:
        result, status_code = await BookService.search_by_title(title, page, per_page)
    else:
        result, status_code = await BookService.get_all(page, per_page)
    if result["success"] and "data" in result:
        result["data"] = books_schema.dump(result["data"])
    return jsonify(result), status_code

@books_bp.route("/<int:book_id>", methods=["GET"])
async def get_book(book_id):
    result, status_code = await BookService.get_by_id(book_id)
    if result["success"]:
        result["data"] = book_schema.dump(result["data"])
    return jsonify(result), status_code

@books_bp.route("/", methods=["POST"])
@jwt_required
async def create_book():
    book_data = await request.get_json()
    validation_errors = book_schema.validate(book_data)
    if validation_errors:
        return (
            jsonify({
                "success": False,
                "message": "Validation error",
                "errors": validation_errors,
            }),
            400,
        )
    result, status_code = await BookService.create(book_data)
    if result["success"]:
        result["data"] = book_schema.dump(result["data"])
    return jsonify(result), status_code

@books_bp.route("/<int:book_id>", methods=["PUT"])
@jwt_required
async def update_book(book_id):
    book_data = await request.get_json()
    validation_errors = book_schema.validate(book_data, partial=True)
    if validation_errors:
        return (
            jsonify({
                "success": False,
                "message": "Validation error",
                "errors": validation_errors,
            }),
            400,
        )
    result, status_code = await BookService.update(book_id, book_data)
    if result["success"]:
        result["data"] = book_schema.dump(result["data"])
    return jsonify(result), status_code

@books_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required
async def delete_book(book_id):
    result, status_code = await BookService.delete(book_id)
    return jsonify(result), status_code

@books_bp.route("/search", methods=["GET"])
async def search_books():
    title = request.args.get("title", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    result, status_code = await BookService.search_by_title(title, page, per_page)
    if result["success"] and "data" in result:
        result["data"] = books_schema.dump(result["data"])
    return jsonify(result), status_code
