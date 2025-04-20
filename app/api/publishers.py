from quart import Blueprint, request, jsonify
from quart_jwt_extended import jwt_required
from app.services.publisher_service import PublisherService
from app.schemas.publisher import PublisherSchema
from marshmallow import ValidationError
import logging

# Set up logging
logger = logging.getLogger(__name__)

publishers_bp = Blueprint("publishers", __name__)
publisher_schema = PublisherSchema()
publishers_schema = PublisherSchema(many=True)


@publishers_bp.route("", methods=["GET"])
async def get_publishers():
    """Get all publishers with pagination and optional filtering by name"""
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    name = request.args.get("name", "")
    if name:
        result, status_code = await PublisherService.search_by_name(
            name, page, per_page
        )
    else:
        result, status_code = await PublisherService.get_all(page, per_page)
    if result["success"] and "data" in result:
        result["data"] = publishers_schema.dump(result["data"])
    return jsonify(result), status_code


@publishers_bp.route("/<int:publisher_id>", methods=["GET"])
async def get_publisher(publisher_id):
    """Get a specific publisher by ID"""
    result, status_code = await PublisherService.get_by_id(publisher_id)
    if result["success"]:
        result["data"] = publisher_schema.dump(result["data"])
    return jsonify(result), status_code


@publishers_bp.route("/", methods=["POST"])
@jwt_required
async def create_publisher():
    """Create a new publisher"""
    publisher_data = await request.get_json()
    validation_errors = publisher_schema.validate(publisher_data)
    if validation_errors:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Validation error",
                    "errors": validation_errors,
                }
            ),
            400,
        )
    result, status_code = await PublisherService.create(publisher_data)
    if result["success"]:
        result["data"] = publisher_schema.dump(result["data"])
    return jsonify(result), status_code


@publishers_bp.route("/<int:publisher_id>", methods=["PUT"])
@jwt_required
async def update_publisher(publisher_id):
    """Update an existing publisher"""
    publisher_data = await request.get_json()
    validation_errors = publisher_schema.validate(publisher_data, partial=True)
    if validation_errors:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Validation error",
                    "errors": validation_errors,
                }
            ),
            400,
        )
    result, status_code = await PublisherService.update(
        publisher_id, publisher_data
    )
    if result["success"]:
        result["data"] = publisher_schema.dump(result["data"])
    return jsonify(result), status_code


@publishers_bp.route("/<int:publisher_id>", methods=["DELETE"])
@jwt_required
async def delete_publisher(publisher_id):
    """Delete a publisher"""
    result, status_code = await PublisherService.delete(publisher_id)
    return jsonify(result), status_code


@publishers_bp.route("/search", methods=["GET"])
async def search_publishers():
    """Search publishers by name with pagination"""
    name = request.args.get("name", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    result, status_code = await PublisherService.search_by_name(
        name, page, per_page
    )
    if result["success"] and "data" in result:
        result["data"] = publishers_schema.dump(result["data"])
    return jsonify(result), status_code
