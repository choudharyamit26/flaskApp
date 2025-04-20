from quart import Blueprint, request, jsonify
from quart_jwt_extended import jwt_required
from app.services.author_service import AuthorService
from app.schemas.author import AuthorSchema
from marshmallow import ValidationError

authors_bp = Blueprint("authors", __name__)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

@authors_bp.route("", methods=["GET"])
async def get_authors():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    name = request.args.get("name", "")
    if name:
        result, status_code = await AuthorService.search_by_name(name, page, per_page)
    else:
        result, status_code = await AuthorService.get_all(page, per_page)
    if result["success"] and "data" in result:
        result["data"] = authors_schema.dump(result["data"])
    return jsonify(result), status_code

@authors_bp.route("/<int:author_id>", methods=["GET"])
async def get_author(author_id):
    result, status_code = await AuthorService.get_by_id(author_id)
    if result["success"]:
        result["data"] = author_schema.dump(result["data"])
    return jsonify(result), status_code

@authors_bp.route("/", methods=["POST"])
@jwt_required
async def create_author():
    author_data = await request.get_json()
    validation_errors = author_schema.validate(author_data)
    if validation_errors:
        return (
            jsonify({
                "success": False,
                "message": "Validation error",
                "errors": validation_errors,
            }),
            400,
        )
    result, status_code = await AuthorService.create(author_data)
    if result["success"]:
        result["data"] = author_schema.dump(result["data"])
    return jsonify(result), status_code

@authors_bp.route("/<int:author_id>", methods=["PUT"])
@jwt_required
async def update_author(author_id):
    author_data = await request.get_json()
    validation_errors = author_schema.validate(author_data, partial=True)
    if validation_errors:
        return (
            jsonify({
                "success": False,
                "message": "Validation error",
                "errors": validation_errors,
            }),
            400,
        )
    result, status_code = await AuthorService.update(author_id, author_data)
    if result["success"]:
        result["data"] = author_schema.dump(result["data"])
    return jsonify(result), status_code

authors_bp.route("/<int:author_id>", methods=["DELETE"])
@jwt_required
async def delete_author(author_id):
    result, status_code = await AuthorService.delete(author_id)
    return jsonify(result), status_code

authors_bp.route("/search", methods=["GET"])
async def search_authors():
    name = request.args.get("name", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    result, status_code = await AuthorService.search_by_name(name, page, per_page)
    if result["success"] and "data" in result:
        result["data"] = authors_schema.dump(result["data"])
    return jsonify(result), status_code
