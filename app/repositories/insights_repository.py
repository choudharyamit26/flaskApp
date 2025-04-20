from quart import current_app
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.insights import Insight


class InsightsRepository:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = select(Insight).options(selectinload(Insight.book))
                result = await session.execute(stmt)
                insights = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return insights[start:end]
        except Exception as e:
            raise Exception(f"Error fetching insights: {str(e)}")

    @staticmethod
    async def get_by_id(insight_id):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Insight)
                    .options(selectinload(Insight.book))
                    .where(Insight.id == insight_id)
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching insight by id: {str(e)}")

    @staticmethod
    async def create(insight):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                session.add(insight)
                await session.commit()
                return insight
        except Exception as e:
            raise Exception(f"Error creating insight: {str(e)}")

    @staticmethod
    async def update(insight):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.commit()
                return insight
        except Exception as e:
            raise Exception(f"Error updating insight: {str(e)}")

    @staticmethod
    async def delete(insight):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.delete(insight)
                await session.commit()
                return True
        except Exception as e:
            raise Exception(f"Error deleting insight: {str(e)}")
