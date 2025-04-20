from quart import Blueprint, request, jsonify
from quart_jwt_extended import jwt_required
from app.services.insights import InsightService
from app.schemas.insights import InsightSchema
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

insights_bp = Blueprint("insights", __name__)
insight_schema = InsightSchema()
insights_schema = InsightSchema(many=True)


@insights_bp.route("/", methods=["GET"])
@jwt_required
async def get_insights():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    result, status_code = await InsightService.get_all(page, per_page)
    if result["success"]:
        result["data"] = insights_schema.dump(result["data"])
    return jsonify(result), status_code
