import pytest
from unittest.mock import patch, MagicMock
import datetime
from app.services.author_service import AuthorService
from app.models.author import Author


class TestAuthorService:
    @patch("app.repositories.author_repository.AuthorRepository.get_all")
    def test_get_all(self, mock_get_all):
        # Mock the repository response
        mock_pagination = MagicMock()
        mock_pagination.items = [
            Author(id=1, first_name="John", last_name="Doe"),
            Author(id=2, first_name="Jane", last_name="Smith"),
        ]
        mock_pagination.page = 1
        mock_pagination.per_page = 10
        mock_pagination.total = 2
        mock_pagination.pages = 1

        mock_get_all.return_value = mock_pagination

        # Call the service
        result, status_code = AuthorService.get_all(page=1, per_page=10)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["total"] == 2
        mock_get_all.assert_called_once_with(1, 10)

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_get_by_id_success(self, mock_get_by_id):
        # Mock the repository response
        mock_author = Author(
            id=1,
            first_name="Test",
            last_name="Author",
            biography="Test biography",
            birth_date=datetime.date(1990, 1, 1),
        )
        mock_get_by_id.return_value = mock_author

        # Call the service
        result, status_code = AuthorService.get_by_id(1)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert result["data"] == mock_author
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_get_by_id_not_found(self, mock_get_by_id):
        # Mock the repository response for not found
        mock_get_by_id.return_value = None

        # Call the service
        result, status_code = AuthorService.get_by_id(999)

        # Assert
        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Author not found"
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.repositories.author_repository.AuthorRepository.create")
    def test_create(self, mock_create):
        # Mock data
        author_data = {
            "first_name": "New",
            "last_name": "Author",
            "biography": "New author biography",
            "birth_date": "1995-05-15",
        }

        # Mock the repository response
        def side_effect(author):
            author.id = 1
            return author

        mock_create.side_effect = side_effect

        # Call the service
        result, status_code = AuthorService.create(author_data)

        # Assert
        assert status_code == 201
        assert result["success"] is True
        assert result["message"] == "Author created successfully"
        assert result["data"].first_name == "New"
        assert result["data"].last_name == "Author"
        assert mock_create.called

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    @patch("app.repositories.author_repository.AuthorRepository.update")
    def test_update_success(self, mock_update, mock_get_by_id):
        # Mock data
        author_data = {"first_name": "Updated", "biography": "Updated biography"}

        # Mock the repository response
        mock_author = Author(
            id=1,
            first_name="Test",
            last_name="Author",
            biography="Test biography",
            birth_date=datetime.date(1990, 1, 1),
        )
        mock_get_by_id.return_value = mock_author

        def update_side_effect(author):
            # Verify the object was updated before saving
            assert author.first_name == "Updated"
            assert author.biography == "Updated biography"
            return author

        mock_update.side_effect = update_side_effect

        # Call the service
        result, status_code = AuthorService.update(1, author_data)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert result["message"] == "Author updated successfully"
        assert result["data"].first_name == "Updated"
        assert result["data"].biography == "Updated biography"
        mock_get_by_id.assert_called_once_with(1)
        mock_update.assert_called_once()

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_update_not_found(self, mock_get_by_id):
        # Mock the repository response for not found
        mock_get_by_id.return_value = None

        # Call the service
        result, status_code = AuthorService.update(999, {"first_name": "Updated"})

        # Assert
        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Author not found"
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    @patch("app.repositories.author_repository.AuthorRepository.delete")
    def test_delete_success(self, mock_delete, mock_get_by_id):
        # Mock the repository responses
        mock_author = MagicMock()
        mock_author.books.count.return_value = 0  # Author has no books
        mock_get_by_id.return_value = mock_author
        mock_delete.return_value = True

        # Call the service
        result, status_code = AuthorService.delete(1)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert result["message"] == "Author deleted successfully"
        mock_get_by_id.assert_called_once_with(1)
        mock_delete.assert_called_once_with(mock_author)

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_delete_not_found(self, mock_get_by_id):
        # Mock the repository response for not found
        mock_get_by_id.return_value = None

        # Call the service
        result, status_code = AuthorService.delete(999)

        # Assert
        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Author not found"
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_delete_with_books(self, mock_get_by_id):
        # Mock the repository responses - author has books
        mock_author = MagicMock()
        mock_author.books.count.return_value = 2  # Author has 2 books
        mock_get_by_id.return_value = mock_author

        # Call the service
        result, status_code = AuthorService.delete(1)

        # Assert
        assert status_code == 400
        assert result["success"] is False
        assert (
            result["message"] == "Cannot delete author with books. Remove books first."
        )
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.repositories.author_repository.AuthorRepository.delete")
    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_delete_failed_dependencies(self, mock_get_by_id, mock_delete):
        # Mock repository responses - delete fails
        mock_author = MagicMock()
        mock_author.books.count.return_value = 0  # No books
        mock_get_by_id.return_value = mock_author
        mock_delete.return_value = False  # Delete fails

        # Call the service
        result, status_code = AuthorService.delete(1)

        # Assert
        assert status_code == 400
        assert result["success"] is False
        assert result["message"] == "Failed to delete author due to dependencies"

    @patch("app.repositories.author_repository.AuthorRepository.search_by_name")
    def test_search_by_name(self, mock_search):
        # Mock the repository response
        mock_pagination = MagicMock()
        mock_pagination.items = [
            Author(id=1, first_name="John", last_name="Doe"),
            Author(id=2, first_name="Jane", last_name="Doe"),
        ]
        mock_pagination.page = 1
        mock_pagination.per_page = 10
        mock_pagination.total = 2
        mock_pagination.pages = 1

        mock_search.return_value = mock_pagination

        # Call the service
        result, status_code = AuthorService.search_by_name("Doe", page=1, per_page=10)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["total"] == 2
        mock_search.assert_called_once_with("Doe", 1, 10)
