from quart import current_app
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.publisher import Publisher


class PublisherRepository:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = select(Publisher).options(selectinload(Publisher.books))
                result = await session.execute(stmt)
                publishers = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return publishers[start:end]
        except Exception as e:
            raise Exception(f"Error fetching publishers: {str(e)}")

    @staticmethod
    async def get_by_id(publisher_id):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Publisher)
                    .options(selectinload(Publisher.books))
                    .where(Publisher.id == publisher_id)
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching publisher by id: {str(e)}")

    @staticmethod
    async def create(publisher):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                session.add(publisher)
                await session.commit()
                return publisher
        except Exception as e:
            raise Exception(f"Error creating publisher: {str(e)}")

    @staticmethod
    async def update(publisher):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.commit()
                return publisher
        except Exception as e:
            raise Exception(f"Error updating publisher: {str(e)}")

    @staticmethod
    async def delete(publisher):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.delete(publisher)
                await session.commit()
                return True
        except Exception as e:
            raise Exception(f"Error deleting publisher: {str(e)}")

    @staticmethod
    async def search_by_name(name, page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Publisher)
                    .options(selectinload(Publisher.books))
                    .where(Publisher.name.ilike(f"%{name}%"))
                )
                result = await session.execute(stmt)
                publishers = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return publishers[start:end]
        except Exception as e:
            raise Exception(f"Error searching publishers: {str(e)}")
