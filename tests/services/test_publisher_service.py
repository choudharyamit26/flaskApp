import pytest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
from app.services.publisher_service import PublisherService
from app.models.publisher import Publisher


class TestPublisherService:
    @patch("app.repositories.publisher_repository.PublisherRepository.get_all")
    def test_get_all(self, mock_get_all):
        # Prepare a simple namespace for pagination metadata
        mock_pagination = SimpleNamespace(
            items=[
                Publisher(id=1, name="Publisher 1", founding_year=2000),
                Publisher(id=2, name="Publisher 2", founding_year=2005),
            ],
            page=1,
            per_page=10,
            total=2,
            pages=1,
        )
        mock_get_all.return_value = mock_pagination

        # Call service
        result, status_code = PublisherService.get_all(page=1, per_page=10)

        # Assertions
        assert status_code == 200
        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["pagination"] == mock_pagination
        mock_get_all.assert_called_once_with(1, 10)

    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    def test_get_by_id_success(self, mock_get_by_id):
        mock_publisher = Publisher(
            id=1,
            name="Test Publisher",
            founding_year=2000,
            website="https://testpublisher.com",
        )
        mock_get_by_id.return_value = mock_publisher

        result, status_code = PublisherService.get_by_id(1)

        assert status_code == 200
        assert result["success"] is True
        assert result["data"] == mock_publisher
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    def test_get_by_id_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result, status_code = PublisherService.get_by_id(999)

        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Publisher not found"
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.repositories.publisher_repository.PublisherRepository.create")
    def test_create(self, mock_create):
        publisher_data = {
            "name": "New Publisher",
            "founding_year": 2010,
            "website": "https://newpublisher.com",
        }

        def side_effect(publisher):
            publisher.id = 1
            return publisher

        mock_create.side_effect = side_effect

        result, status_code = PublisherService.create(publisher_data)

        assert status_code == 201
        assert result["success"] is True
        assert result["message"] == "Publisher created successfully"
        assert result["data"].name == "New Publisher"
        assert result["data"].founding_year == 2010
        mock_create.assert_called_once()

    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    @patch("app.repositories.publisher_repository.PublisherRepository.update")
    def test_update_success(self, mock_update, mock_get_by_id):
        publisher_data = {
            "name": "Updated Publisher",
            "website": "https://updated-publisher.com",
        }
        mock_publisher = Publisher(
            id=1,
            name="Test Publisher",
            founding_year=2000,
            website="https://testpublisher.com",
        )
        mock_get_by_id.return_value = mock_publisher

        def update_side_effect(publisher):
            assert publisher.name == "Updated Publisher"
            assert publisher.website == "https://updated-publisher.com"
            return publisher

        mock_update.side_effect = update_side_effect

        result, status_code = PublisherService.update(1, publisher_data)

        assert status_code == 200
        assert result["success"] is True
        assert result["message"] == "Publisher updated successfully"
        assert result["data"].name == "Updated Publisher"
        assert result["data"].website == "https://updated-publisher.com"
        mock_get_by_id.assert_called_once_with(1)
        mock_update.assert_called_once()

    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    def test_update_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result, status_code = PublisherService.update(999, {"name": "Updated"})

        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Publisher not found"
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    @patch("app.repositories.publisher_repository.PublisherRepository.delete")
    def test_delete_success(self, mock_delete, mock_get_by_id):
        mock_publisher = Publisher(
            id=1,
            name="Test Publisher",
            founding_year=2000,
            website="https://testpublisher.com",
        )
        mock_get_by_id.return_value = mock_publisher
        mock_delete.return_value = True

        result, status_code = PublisherService.delete(1)

        assert status_code == 200
        assert result["success"] is True
        assert result["message"] == "Publisher deleted successfully"
        mock_get_by_id.assert_called_once_with(1)
        mock_delete.assert_called_once_with(mock_publisher)

    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    def test_delete_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result, status_code = PublisherService.delete(999)

        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Publisher not found"
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.repositories.publisher_repository.PublisherRepository.search_by_name")
    def test_search_by_name(self, mock_search):
        mock_pagination = SimpleNamespace(
            items=[
                Publisher(id=1, name="O'Reilly Media", founding_year=1978),
                Publisher(id=2, name="Apress Media", founding_year=1999),
            ],
            page=1,
            per_page=10,
            total=2,
            pages=1,
        )
        mock_search.return_value = mock_pagination

        result, status_code = PublisherService.search_by_name(
            "Media", page=1, per_page=10
        )

        assert status_code == 200
        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["pagination"] == mock_pagination
        mock_search.assert_called_once_with("Media", 1, 10)
