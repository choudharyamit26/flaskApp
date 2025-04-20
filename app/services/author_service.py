from app.repositories.author_repository import AuthorRepository
from app.models.author import Author


class AuthorService:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            authors = await AuthorRepository.get_all(page, per_page)
            return {
                "success": True,
                "data": authors,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(authors),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def get_by_id(author_id):
        try:
            author = await AuthorRepository.get_by_id(author_id)
            if not author:
                return {"success": False, "message": "Author not found"}, 404
            return {"success": True, "data": author}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def create(author_data):
        try:
            if isinstance(author_data, Author):
                author = author_data
            else:
                author = Author(
                    first_name=author_data.get("first_name"),
                    last_name=author_data.get("last_name"),
                    biography=author_data.get("biography"),
                    birth_date=author_data.get("birth_date"),
                )
            await AuthorRepository.create(author)
            # Re-fetch with books eagerly loaded
            author = await AuthorRepository.get_by_id(author.id)
            return {
                "success": True,
                "data": author,
                "message": "Author created successfully",
            }, 201
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def update(author_id, author_data):
        try:
            author = await AuthorRepository.get_by_id(author_id)
            if not author:
                return {"success": False, "message": "Author not found"}, 404
            if isinstance(author_data, dict):
                if "first_name" in author_data:
                    author.first_name = author_data["first_name"]
                if "last_name" in author_data:
                    author.last_name = author_data["last_name"]
                if "biography" in author_data:
                    author.biography = author_data["biography"]
                if "birth_date" in author_data:
                    author.birth_date = author_data["birth_date"]
            elif isinstance(author_data, Author):
                if author_data.first_name:
                    author.first_name = author_data.first_name
                if author_data.last_name:
                    author.last_name = author_data.last_name
                if author_data.biography:
                    author.biography = author_data.biography
                if author_data.birth_date:
                    author.birth_date = author_data.birth_date
            await AuthorRepository.update(author)
            # Re-fetch with books eagerly loaded
            author = await AuthorRepository.get_by_id(author.id)
            return {
                "success": True,
                "data": author,
                "message": "Author updated successfully",
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def delete(author_id):
        try:
            author = await AuthorRepository.get_by_id(author_id)
            if not author:
                return {"success": False, "message": "Author not found"}, 404
            if hasattr(author, "books") and len(author.books) > 0:
                return {
                    "success": False,
                    "message": "Cannot delete author with books. Remove books first.",
                }, 400
            success = await AuthorRepository.delete(author)
            if success:
                return {"success": True, "message": "Author deleted successfully"}, 200
            else:
                return {
                    "success": False,
                    "message": "Failed to delete author due to dependencies",
                }, 400
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def search_by_name(name, page=1, per_page=10):
        try:
            authors = await AuthorRepository.search_by_name(name, page, per_page)
            return {
                "success": True,
                "data": authors,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(authors),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500
