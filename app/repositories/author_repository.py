from quart import current_app
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.author import Author


class AuthorRepository:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = select(Author).options(selectinload(Author.books))
                result = await session.execute(stmt)
                authors = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return authors[start:end]
        except Exception as e:
            raise Exception(f"Error fetching authors: {str(e)}")

    @staticmethod
    async def get_by_id(author_id):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Author)
                    .options(selectinload(Author.books))
                    .where(Author.id == author_id)
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching author by id: {str(e)}")

    @staticmethod
    async def create(author):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                session.add(author)
                await session.commit()
                return author
        except Exception as e:
            raise Exception(f"Error creating author: {str(e)}")

    @staticmethod
    async def update(author):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.commit()
                return author
        except Exception as e:
            raise Exception(f"Error updating author: {str(e)}")

    @staticmethod
    async def delete(author):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.delete(author)
                await session.commit()
                return True
        except Exception as e:
            raise Exception(f"Error deleting author: {str(e)}")

    @staticmethod
    async def search_by_name(name, page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Author)
                    .options(selectinload(Author.books))
                    .where(
                        (Author.first_name.ilike(f"%{name}%"))
                        | (Author.last_name.ilike(f"%{name}%"))
                    )
                )
                result = await session.execute(stmt)
                authors = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return authors[start:end]
        except Exception as e:
            raise Exception(f"Error searching authors: {str(e)}")
