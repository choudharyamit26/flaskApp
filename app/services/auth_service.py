from app.repositories.user_repository import UserRepository
from quart_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash
from app.models.user import User


class AuthService:
    @staticmethod
    async def register(username, email, password):
        try:
            if await UserRepository.get_by_username(username):
                return {"success": False, "message": "Username already exists"}, 400
            if await UserRepository.get_by_email(email):
                return {"success": False, "message": "Email already registered"}, 400
            user = User(username=username, email=email, password=password)
            await UserRepository.create(user)
            return {
                "success": True,
                "message": "User registered successfully",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }, 201
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def login(email, password):
        try:
            user = await UserRepository.get_by_email(email)
            if user and user.check_password(password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return {
                    "success": True,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"id": user.id, "username": user.username, "email": user.email},
                }, 200
            return {"success": False, "message": "Invalid credentials"}, 401
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def refresh(user_id):
        try:
            user = await UserRepository.get_by_id(user_id)
            if not user:
                return {"success": False, "message": "User not found"}, 404
            access_token = create_access_token(identity=user.id)
            return {"success": True, "access_token": access_token}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def change_password(user_id, old_password, new_password):
        try:
            user = await UserRepository.get_by_id(user_id)
            if not user:
                return {"success": False, "message": "User not found"}, 404
            if not user.check_password(old_password):
                return {"success": False, "message": "Incorrect password"}, 401
            user.password_hash = generate_password_hash(new_password)
            await UserRepository.update(user)
            return {"success": True, "message": "Password changed successfully"}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500
