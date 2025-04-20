from app.extensions import async_db as db
from app.models.book import Book
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from quart import current_app
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class BookRepository:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = select(Book).options(
                    selectinload(Book.author), selectinload(Book.publisher)
                )
                result = await session.execute(stmt)
                books = result.scalars().all()
                # Manual pagination (since paginate is not available in async)
                start = (page - 1) * per_page
                end = start + per_page
                return books[start:end]
        except Exception as e:
            raise Exception(f"Error fetching books: {str(e)}")

    @staticmethod
    async def get_by_id(book_id):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Book)
                    .options(selectinload(Book.author), selectinload(Book.publisher))
                    .where(Book.id == book_id)
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching book by id: {str(e)}")

    @staticmethod
    async def get_by_isbn(isbn):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Book)
                    .options(selectinload(Book.author), selectinload(Book.publisher))
                    .where(Book.isbn == isbn)
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error fetching book by isbn: {str(e)}")

    @staticmethod
    async def create(book):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                session.add(book)
                await session.commit()
                return book
        except Exception as e:
            raise Exception(f"Error creating book: {str(e)}")

    @staticmethod
    async def update(book):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.commit()
                return book
        except Exception as e:
            raise Exception(f"Error updating book: {str(e)}")

    @staticmethod
    async def delete(book):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                await session.delete(book)
                await session.commit()
        except Exception as e:
            raise Exception(f"Error deleting book: {str(e)}")

    @staticmethod
    async def search_by_title(title, page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Book)
                    .options(selectinload(Book.author), selectinload(Book.publisher))
                    .where(Book.title.ilike(f"%{title}%"))
                )
                result = await session.execute(stmt)
                books = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return books[start:end]
        except Exception as e:
            raise Exception(f"Error searching books: {str(e)}")

    @staticmethod
    async def get_by_author(author_id, page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Book)
                    .options(selectinload(Book.author), selectinload(Book.publisher))
                    .where(Book.author_id == author_id)
                )
                result = await session.execute(stmt)
                books = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return books[start:end]
        except Exception as e:
            raise Exception(f"Error fetching books by author: {str(e)}")

    @staticmethod
    async def get_by_publisher(publisher_id, page=1, per_page=10):
        try:
            async_session = current_app.async_session
            async with async_session() as session:
                stmt = (
                    select(Book)
                    .options(selectinload(Book.author), selectinload(Book.publisher))
                    .where(Book.publisher_id == publisher_id)
                )
                result = await session.execute(stmt)
                books = result.scalars().all()
                start = (page - 1) * per_page
                end = start + per_page
                return books[start:end]
        except Exception as e:
            raise Exception(f"Error fetching books by publisher: {str(e)}")
