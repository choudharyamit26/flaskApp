from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.publisher_repository import PublisherRepository
from app.models.book import Book


class BookService:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            books = await BookRepository.get_all(page, per_page)
            return {
                "success": True,
                "data": books,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(books),
                    "pages": 1,  # For real pagination, implement total count
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def get_by_id(book_id):
        try:
            book = await BookRepository.get_by_id(book_id)
            if not book:
                return {"success": False, "message": "Book not found"}, 404
            return {"success": True, "data": book}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def create(book_data):
        try:
            author = await AuthorRepository.get_by_id(book_data.get("author_id"))
            if not author:
                return {"success": False, "message": "Author not found"}, 404
            publisher = await PublisherRepository.get_by_id(book_data.get("publisher_id"))
            if not publisher:
                return {"success": False, "message": "Publisher not found"}, 404
            if book_data.get("isbn"):
                existing_book = await BookRepository.get_by_isbn(book_data.get("isbn"))
                if existing_book:
                    return {"success": False, "message": "ISBN already exists"}, 400
            book = Book(
                title=book_data.get("title"),
                isbn=book_data.get("isbn"),
                publication_date=book_data.get("publication_date"),
                price=book_data.get("price"),
                description=book_data.get("description"),
                author_id=book_data.get("author_id"),
                publisher_id=book_data.get("publisher_id"),
            )
            await BookRepository.create(book)
            # Re-fetch with author and publisher eagerly loaded
            book = await BookRepository.get_by_id(book.id)
            return {
                "success": True,
                "data": book,
                "message": "Book created successfully",
            }, 201
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def update(book_id, book_data):
        try:
            book = await BookRepository.get_by_id(book_id)
            if not book:
                return {"success": False, "message": "Book not found"}, 404
            if "author_id" in book_data:
                author = await AuthorRepository.get_by_id(book_data["author_id"])
                if not author:
                    return {"success": False, "message": "Author not found"}, 404
                book.author_id = book_data["author_id"]
            if "publisher_id" in book_data:
                publisher = await PublisherRepository.get_by_id(book_data["publisher_id"])
                if not publisher:
                    return {"success": False, "message": "Publisher not found"}, 404
                book.publisher_id = book_data["publisher_id"]
            if "isbn" in book_data and book_data["isbn"] != book.isbn:
                existing_book = await BookRepository.get_by_isbn(book_data["isbn"])
                if existing_book:
                    return {"success": False, "message": "ISBN already exists"}, 400
                book.isbn = book_data["isbn"]
            if "title" in book_data:
                book.title = book_data["title"]
            if "publication_date" in book_data:
                book.publication_date = book_data["publication_date"]
            if "price" in book_data:
                book.price = book_data["price"]
            if "description" in book_data:
                book.description = book_data["description"]
            await BookRepository.update(book)
            # Re-fetch with author and publisher eagerly loaded
            book = await BookRepository.get_by_id(book.id)
            return {
                "success": True,
                "data": book,
                "message": "Book updated successfully",
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def delete(book_id):
        try:
            book = await BookRepository.get_by_id(book_id)
            if not book:
                return {"success": False, "message": "Book not found"}, 404
            await BookRepository.delete(book)
            return {"success": True, "message": "Book deleted successfully"}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def search_by_title(title, page=1, per_page=10):
        try:
            books = await BookRepository.search_by_title(title, page, per_page)
            return {
                "success": True,
                "data": books,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(books),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def get_by_author(author_id, page=1, per_page=10):
        try:
            author = await AuthorRepository.get_by_id(author_id)
            if not author:
                return {"success": False, "message": "Author not found"}, 404
            books = await BookRepository.get_by_author(author_id, page, per_page)
            return {
                "success": True,
                "data": books,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(books),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def get_by_publisher(publisher_id, page=1, per_page=10):
        try:
            publisher = await PublisherRepository.get_by_id(publisher_id)
            if not publisher:
                return {"success": False, "message": "Publisher not found"}, 404
            books = await BookRepository.get_by_publisher(publisher_id, page, per_page)
            return {
                "success": True,
                "data": books,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(books),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500
