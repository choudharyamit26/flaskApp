from app.repositories.insights_repository import InsightsRepository
from app.repositories.book_repository import BookRepository
from app.models.insights import Insight


class InsightService:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            insights = await InsightsRepository.get_all(page, per_page)
            return {
                "success": True,
                "data": insights,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(insights),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def get_by_id(insight_id):
        try:
            insight = await InsightsRepository.get_by_id(insight_id)
            if not insight:
                return {"success": False, "message": "Insight not found"}, 404
            return {"success": True, "data": insight}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def create(data):
        try:
            book = await BookRepository.get_by_id(data["book_id"])
            if not book:
                return {"success": False, "message": "Book not found"}, 404
            insight = Insight(
                title=data.get("title"),
                description=data.get("description"),
                book_id=data.get("book_id"),
            )
            await InsightsRepository.create(insight)
            # Re-fetch with book eagerly loaded
            insight = await InsightsRepository.get_by_id(insight.id)
            return {"success": True, "data": insight}, 201
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def update(insight_id, data):
        try:
            insight = await InsightsRepository.get_by_id(insight_id)
            if not insight:
                return {"success": False, "message": "Insight not found"}, 404
            if "book_id" in data:
                book = await BookRepository.get_by_id(data["book_id"])
                if not book:
                    return {"success": False, "message": "Book not found"}, 404
                insight.book_id = data["book_id"]
            if "title" in data:
                insight.title = data["title"]
            if "description" in data:
                insight.description = data["description"]
            await InsightsRepository.update(insight)
            # Re-fetch with book eagerly loaded
            insight = await InsightsRepository.get_by_id(insight.id)
            return {"success": True, "data": insight}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def delete(insight_id):
        try:
            insight = await InsightsRepository.get_by_id(insight_id)
            if not insight:
                return {"success": False, "message": "Insight not found"}, 404
            await InsightsRepository.delete(insight)
            return {"success": True, "message": "Insight deleted successfully"}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500
