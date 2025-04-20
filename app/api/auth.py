from quart import Blueprint, request, jsonify
from quart_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.schemas.user import UserSchema
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)
user_schema = UserSchema()

@auth_bp.route("/register", methods=["POST"])
async def register():
    user_data = user_schema.load(await request.get_json())
    result, status_code = await AuthService.register(
        username=user_data.get("username"),
        email=user_data.get("email"),
        password=user_data.get("password"),
    )
    return jsonify(result), status_code

@auth_bp.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return (
            jsonify({"success": False, "message": "Email and password are required"}),
            400,
        )
    result, status_code = await AuthService.login(email, password)
    return jsonify(result), status_code

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required
async def refresh():
    user_id = await get_jwt_identity()
    result, status_code = await AuthService.refresh(user_id)
    return jsonify(result), status_code

@auth_bp.route("/change-password", methods=["POST"])
@jwt_required
async def change_password():
    user_id = await get_jwt_identity()
    data = await request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not old_password or not new_password:
        return (
            jsonify({"success": False, "message": "Old and new passwords are required"}),
            400,
        )
    result, status_code = await AuthService.change_password(
        user_id, old_password, new_password
    )
    return jsonify(result), status_code
