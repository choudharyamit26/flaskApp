from decimal import Decimal
import pytest
from app.repositories.book_repository import BookRepository
from app.models.book import Book
from sqlalchemy.exc import IntegrityError
import datetime


class TestBookRepository:
    def test_get_all(self, db_session, sample_book):
        # Create additional books for pagination testing
        for i in range(5):
            book = Book(
                title=f"Test Book {i}",
                isbn=f"123456789{i}",
                publication_date=datetime.date(2020, 1, 1),
                price=19.99,
                description=f"Description {i}",
                author_id=sample_book.author_id,
                publisher_id=sample_book.publisher_id,
            )
            db_session.add(book)
        db_session.commit()

        # Test first page
        result = BookRepository.get_all(page=1, per_page=3)
        assert result.items is not None
        assert len(result.items) == 3
        assert result.page == 1
        assert result.per_page == 3
        assert result.total == 6  # 5 new books + 1 sample book

        # Test second page
        result = BookRepository.get_all(page=2, per_page=3)
        assert len(result.items) == 3
        assert result.page == 2

    def test_get_by_id(self, db_session, sample_book):
        book = BookRepository.get_by_id(sample_book.id)
        assert book is not None
        assert book.id == sample_book.id
        assert book.title == "Test Book"

        # Test with non-existent ID
        non_existent = BookRepository.get_by_id(9999)
        assert non_existent is None

    def test_get_by_isbn(self, db_session, sample_book):
        book = BookRepository.get_by_isbn(sample_book.isbn)
        assert book is not None
        assert book.id == sample_book.id
        assert book.isbn == "1234567890123"

        # Test with non-existent ISBN
        non_existent = BookRepository.get_by_isbn("9999999999999")
        assert non_existent is None

    def test_create(self, db_session, sample_author, sample_publisher):
        new_book = Book(
            title="New Book",
            isbn="9876543210123",
            publication_date=datetime.date(2021, 2, 2),
            price=39.99,
            description="A new test book",
            author_id=sample_author.id,
            publisher_id=sample_publisher.id,
        )

        created = BookRepository.create(new_book)
        assert created is not None
        assert created.id is not None
        assert created.title == "New Book"
        assert created.isbn == "9876543210123"

        # Verify in database
        db_book = db_session.get(Book, created.id)
        assert db_book is not None
        assert db_book.title == "New Book"

    def test_create_duplicate_isbn(
        self, db_session, sample_book, sample_author, sample_publisher
    ):
        new_book = Book(
            title="Duplicate ISBN Book",
            isbn=sample_book.isbn,  # Use existing ISBN to cause conflict
            publication_date=datetime.date(2021, 2, 2),
            price=39.99,
            description="A test book with duplicate ISBN",
            author_id=sample_author.id,
            publisher_id=sample_publisher.id,
        )

        with pytest.raises(IntegrityError):
            BookRepository.create(new_book)

    def test_update(self, db_session, sample_book):
        sample_book.title = "Updated Title"
        sample_book.price = 49.99

        updated = BookRepository.update(sample_book)
        assert updated is not None
        assert updated.title == "Updated Title"
        assert updated.price == Decimal("49.99")

        # Verify in database
        db_session.expire_all()
        db_book = db_session.get(Book, sample_book.id)
        assert db_book.title == "Updated Title"
        assert db_book.price == Decimal("49.99")

    def test_delete(self, db_session, sample_book):
        BookRepository.delete(sample_book)

        # Verify deletion
        db_session.expire_all()
        db_book = db_session.get(Book, sample_book.id)
        assert db_book is None

    def test_search_by_title(self, db_session, sample_book):
        # Create additional books with various titles
        titles = [
            "Python Programming",
            "Advanced Python",
            "Flask Web Development",
            "SQLAlchemy ORM",
        ]

        for title in titles:
            book = Book(
                title=title,
                isbn=f"ISBN-{title.replace(' ', '-')}",
                publication_date=datetime.date(2021, 1, 1),
                price=29.99,
                description=f"Description for {title}",
                author_id=sample_book.author_id,
                publisher_id=sample_book.publisher_id,
            )
            db_session.add(book)
        db_session.commit()

        # Search for "Python"
        result = BookRepository.search_by_title("Python", page=1, per_page=10)
        assert len(result.items) == 2
        assert all("Python" in book.title for book in result.items)

        # Search for "Flask"
        result = BookRepository.search_by_title("Flask", page=1, per_page=10)
        assert len(result.items) == 1
        assert "Flask" in result.items[0].title

        # Test with no match
        result = BookRepository.search_by_title("JavaScript", page=1, per_page=10)
        assert len(result.items) == 0

    def test_get_by_author(self, db_session, sample_book, sample_author):
        # Create additional books for the same author
        for i in range(3):
            book = Book(
                title=f"Author Book {i}",
                isbn=f"AuthISBN{i}",
                publication_date=datetime.date(2022, 1, 1),
                price=19.99,
                description=f"Book {i} by test author",
                author_id=sample_author.id,
                publisher_id=sample_book.publisher_id,
            )
            db_session.add(book)
        db_session.commit()

        result = BookRepository.get_by_author(sample_author.id, page=1, per_page=10)
        assert result.items is not None
        assert len(result.items) == 4  # 3 new books + 1 sample book
        assert all(book.author_id == sample_author.id for book in result.items)

    def test_get_by_publisher(self, db_session, sample_book, sample_publisher):
        # Create additional books for the same publisher
        for i in range(3):
            book = Book(
                title=f"Publisher Book {i}",
                isbn=f"PubISBN{i}",
                publication_date=datetime.date(2022, 1, 1),
                price=19.99,
                description=f"Book {i} by test publisher",
                author_id=sample_book.author_id,
                publisher_id=sample_publisher.id,
            )
            db_session.add(book)
        db_session.commit()

        result = BookRepository.get_by_publisher(
            sample_publisher.id, page=1, per_page=10
        )
        assert result.items is not None
        assert len(result.items) == 4  # 3 new books + 1 sample book
        assert all(book.publisher_id == sample_publisher.id for book in result.items)
