from app.repositories.publisher_repository import PublisherRepository
from app.models.publisher import Publisher


class PublisherService:
    @staticmethod
    async def get_all(page=1, per_page=10):
        try:
            publishers = await PublisherRepository.get_all(page, per_page)
            return {
                "success": True,
                "data": publishers,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(publishers),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def get_by_id(publisher_id):
        try:
            publisher = await PublisherRepository.get_by_id(publisher_id)
            if not publisher:
                return {"success": False, "message": "Publisher not found"}, 404
            return {"success": True, "data": publisher}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def create(publisher_data):
        try:
            publisher = Publisher(
                name=publisher_data.get("name"),
                founding_year=publisher_data.get("founding_year"),
                website=publisher_data.get("website"),
            )
            await PublisherRepository.create(publisher)
            publisher = await PublisherRepository.get_by_id(publisher.id)
            return {
                "success": True,
                "data": publisher,
                "message": "Publisher created successfully",
            }, 201
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def update(publisher_id, publisher_data):
        try:
            publisher = await PublisherRepository.get_by_id(publisher_id)
            if not publisher:
                return {"success": False, "message": "Publisher not found"}, 404
            if "name" in publisher_data:
                publisher.name = publisher_data["name"]
            if "founding_year" in publisher_data:
                publisher.founding_year = publisher_data["founding_year"]
            if "website" in publisher_data:
                publisher.website = publisher_data["website"]
            await PublisherRepository.update(publisher)
            publisher = await PublisherRepository.get_by_id(publisher.id)
            return {
                "success": True,
                "data": publisher,
                "message": "Publisher updated successfully",
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def delete(publisher_id):
        try:
            publisher = await PublisherRepository.get_by_id(publisher_id)
            if not publisher:
                return {"success": False, "message": "Publisher not found"}, 404
            await PublisherRepository.delete(publisher)
            return {"success": True, "message": "Publisher deleted successfully"}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    async def search_by_name(name, page=1, per_page=10):
        try:
            publishers = await PublisherRepository.search_by_name(name, page, per_page)
            return {
                "success": True,
                "data": publishers,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(publishers),
                    "pages": 1,
                },
            }, 200
        except Exception as e:
            return {"success": False, "message": str(e)}, 500
