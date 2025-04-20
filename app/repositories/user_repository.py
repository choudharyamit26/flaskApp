from app.extensions import async_db as db
from app.models.user import User
from quart import current_app
from sqlalchemy.future import select


class UserRepository:
    @staticmethod
    async def create(user):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                session.add(user)
                await session.commit()
                return user
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    @staticmethod
    async def get_by_id(user_id):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching user by id: {str(e)}")

    @staticmethod
    async def get_by_username(username):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = select(User).where(User.username == username)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching user by username: {str(e)}")

    @staticmethod
    async def get_by_email(email):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = select(User).where(User.email == email)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching user by email: {str(e)}")

    @staticmethod
    async def update(user):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.commit()
                return user
        except Exception as e:
            raise Exception(f"Error updating user: {str(e)}")

    @staticmethod
    async def delete(user):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.delete(user)
                await session.commit()
                return True
        except Exception as e:
            raise Exception(f"Error deleting user: {str(e)}")
