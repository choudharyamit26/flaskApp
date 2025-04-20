from unittest.mock import patch, MagicMock
import datetime
from app.services.book_service import BookService
from app.models.book import Book
from app.models.author import Author
from app.models.publisher import Publisher


class TestBookService:
    @patch("app.repositories.book_repository.BookRepository.get_all")
    def test_get_all(self, mock_get_all):
        # Mock the repository response
        mock_pagination = MagicMock()
        mock_pagination.items = [
            Book(id=1, title="Test Book 1", isbn="1234567890"),
            Book(id=2, title="Test Book 2", isbn="0987654321"),
        ]
        mock_pagination.page = 1
        mock_pagination.per_page = 10
        mock_pagination.total = 2
        mock_pagination.pages = 1

        mock_get_all.return_value = mock_pagination

        # Call the service
        result, status_code = BookService.get_all(page=1, per_page=10)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["total"] == 2
        mock_get_all.assert_called_once_with(1, 10)

    @patch("app.repositories.book_repository.BookRepository.get_by_id")
    def test_get_by_id_success(self, mock_get_by_id):
        # Mock the repository response
        mock_book = Book(
            id=1,
            title="Test Book",
            isbn="1234567890",
            publication_date=datetime.date(2020, 1, 1),
            price=29.99,
            description="Test description",
            author_id=1,
            publisher_id=1,
        )
        mock_get_by_id.return_value = mock_book

        # Call the service
        result, status_code = BookService.get_by_id(1)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert result["data"] == mock_book
        mock_get_by_id.assert_called_once_with(1)

    @patch("app.repositories.book_repository.BookRepository.get_by_id")
    def test_get_by_id_not_found(self, mock_get_by_id):
        # Mock the repository response for not found
        mock_get_by_id.return_value = None

        # Call the service
        result, status_code = BookService.get_by_id(999)

        # Assert
        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Book not found"
        mock_get_by_id.assert_called_once_with(999)

    @patch("app.repositories.book_repository.BookRepository.create")
    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    @patch("app.repositories.book_repository.BookRepository.get_by_isbn")
    def test_create_success(
        self, mock_get_by_isbn, mock_get_author, mock_get_publisher, mock_create
    ):
        # Mock data
        book_data = {
            "title": "New Book",
            "isbn": "1234567890123",
            "publication_date": "2021-01-01",
            "price": 29.99,
            "description": "New book description",
            "author_id": 1,
            "publisher_id": 1,
        }

        # Mock the repository responses
        mock_get_by_isbn.return_value = None  # ISBN doesn't exist
        mock_get_author.return_value = Author(
            id=1, first_name="Test", last_name="Author"
        )
        mock_get_publisher.return_value = Publisher(id=1, name="Test Publisher")

        def create_side_effect(book):
            book.id = 1
            return book

        mock_create.side_effect = create_side_effect

        # Call the service
        result, status_code = BookService.create(book_data)

        # Assert
        assert status_code == 201
        assert result["success"] is True
        assert result["message"] == "Book created successfully"
        assert result["data"].title == "New Book"
        assert result["data"].isbn == "1234567890123"
        mock_get_by_isbn.assert_called_once_with("1234567890123")
        mock_get_author.assert_called_once_with(1)
        mock_get_publisher.assert_called_once_with(1)
        mock_create.assert_called_once()

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_create_author_not_found(self, mock_get_author):
        # Mock data
        book_data = {
            "title": "New Book",
            "isbn": "1234567890123",
            "publication_date": "2021-01-01",
            "price": 29.99,
            "description": "New book description",
            "author_id": 999,  # Non-existent author
            "publisher_id": 1,
        }

        # Mock the repository response
        mock_get_author.return_value = None  # Author not found

        # Call the service
        result, status_code = BookService.create(book_data)

        # Assert
        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Author not found"
        mock_get_author.assert_called_once_with(999)

    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    def test_create_publisher_not_found(self, mock_get_publisher, mock_get_author):
        # Mock data
        book_data = {
            "title": "New Book",
            "isbn": "1234567890123",
            "publication_date": "2021-01-01",
            "price": 29.99,
            "description": "New book description",
            "author_id": 1,
            "publisher_id": 999,  # Non-existent publisher
        }

        # Mock the repository responses
        mock_get_author.return_value = Author(
            id=1, first_name="Test", last_name="Author"
        )
        mock_get_publisher.return_value = None  # Publisher not found

        # Call the service
        result, status_code = BookService.create(book_data)

        # Assert
        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Publisher not found"
        mock_get_author.assert_called_once_with(1)
        mock_get_publisher.assert_called_once_with(999)

    @patch("app.repositories.publisher_repository.PublisherRepository.get_by_id")
    @patch("app.repositories.book_repository.BookRepository.get_by_isbn")
    @patch("app.repositories.author_repository.AuthorRepository.get_by_id")
    def test_create_duplicate_isbn(
        self, mock_get_author, mock_get_by_isbn, mock_get_publisher
    ):
        # Mock data
        book_data = {
            "title": "New Book",
            "isbn": "1234567890123",  # Duplicate ISBN
            "publication_date": "2021-01-01",
            "price": 29.99,
            "description": "New book description",
            "author_id": 1,
            "publisher_id": 1,
        }

        # Mock the repository responses
        mock_get_by_isbn.return_value = Book(
            id=2, title="Existing Book", isbn="1234567890123"
        )  # ISBN exists
        mock_get_author.return_value = Author(
            id=1, first_name="Test", last_name="Author"
        )
        mock_get_publisher.return_value = Publisher(id=1, name="Test Publisher")

        # Call the service
        result, status_code = BookService.create(book_data)

        # Assert
        assert status_code == 400
        assert result["success"] is False
        assert result["message"] == "ISBN already exists"
        mock_get_by_isbn.assert_called_once_with("1234567890123")

    @patch("app.repositories.book_repository.BookRepository.update")
    @patch("app.repositories.book_repository.BookRepository.get_by_id")
    def test_update_success(self, mock_get_by_id, mock_update):
        # Mock data
        book_data = {
            "title": "Updated Title",
            "price": 39.99,
            "description": "Updated description",
        }

        # Mock the repository responses
        mock_book = Book(
            id=1,
            title="Test Book",
            isbn="1234567890",
            publication_date=datetime.date(2020, 1, 1),
            price=29.99,
            description="Test description",
            author_id=1,
            publisher_id=1,
        )
        mock_get_by_id.return_value = mock_book

        def update_side_effect(book):
            # Verify the object was updated before saving
            assert book.title == "Updated Title"
            assert book.price == 39.99
            assert book.description == "Updated description"
            return book

        mock_update.side_effect = update_side_effect

        # Call the service
        result, status_code = BookService.update(1, book_data)

        # Assert
        assert status_code == 200
        assert result["success"] is True
        assert result["message"] == "Book updated successfully"
        assert result["data"].title == "Updated Title"
        assert result["data"].price == 39.99
        mock_get_by_id.assert_called_once_with(1)
        mock_update.assert_called_once()

    @patch("app.repositories.book_repository.BookRepository.get_by_id")
    def test_update_not_found(self, mock_get_by_id):
        # Mock the repository response for not found
        mock_get_by_id.return_value = None

        # Call the service
        result, status_code = BookService.update(999, {"title": "New Title"})

        # Assert
        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "Book not found"
        mock_get_by_id.assert_called_once_with(999)
