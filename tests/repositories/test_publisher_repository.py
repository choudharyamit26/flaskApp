import pytest
from app.repositories.publisher_repository import PublisherRepository
from app.models.publisher import Publisher
from app.models.book import Book
import datetime


class TestPublisherRepository:
    def test_get_all(self, db_session, sample_publisher):
        # Create additional publishers for pagination testing
        for i in range(5):
            publisher = Publisher(
                name=f"Test Publisher {i}",
                founding_year=2000 + i,
                website=f"https://publisher{i}.com",
            )
            db_session.add(publisher)
        db_session.commit()

        # Test first page
        result = PublisherRepository.get_all(page=1, per_page=3)
        assert result.items is not None
        assert len(result.items) == 3
        assert result.page == 1
        assert result.per_page == 3
        assert result.total == 6  # 5 new publishers + 1 sample publisher

        # Test second page
        result = PublisherRepository.get_all(page=2, per_page=3)
        assert len(result.items) == 3
        assert result.page == 2

    def test_get_by_id(self, db_session, sample_publisher):
        publisher = PublisherRepository.get_by_id(sample_publisher.id)
        assert publisher is not None
        assert publisher.id == sample_publisher.id
        assert publisher.name == "Test Publisher"

        # Test with non-existent ID
        non_existent = PublisherRepository.get_by_id(9999)
        assert non_existent is None

    def test_create(self, db_session):
        new_publisher = Publisher(
            name="New Publisher", founding_year=2010, website="https://newpublisher.com"
        )

        created = PublisherRepository.create(new_publisher)
        assert created is not None
        assert created.id is not None
        assert created.name == "New Publisher"
        assert created.founding_year == 2010

        # Verify in database
        db_publisher = db_session.get(Publisher, created.id)
        assert db_publisher is not None
        assert db_publisher.name == "New Publisher"

    def test_update(self, db_session, sample_publisher):
        sample_publisher.name = "Updated Publisher"
        sample_publisher.founding_year = 1995

        updated = PublisherRepository.update(sample_publisher)
        assert updated is not None
        assert updated.name == "Updated Publisher"
        assert updated.founding_year == 1995

        # Verify in database
        db_session.expire_all()
        db_publisher = db_session.get(Publisher, sample_publisher.id)
        assert db_publisher.name == "Updated Publisher"
        assert db_publisher.founding_year == 1995

    def test_delete_without_books(self, db_session, sample_publisher):
        # Create a publisher with no books
        new_publisher = Publisher(
            name="Publisher to Delete",
            founding_year=2015,
            website="https://deletetest.com",
        )
        db_session.add(new_publisher)
        db_session.commit()

        # Delete the publisher
        result = PublisherRepository.delete(new_publisher)
        assert result is True

        # Verify deletion
        db_session.expire_all()
        db_publisher = db_session.get(Publisher, new_publisher.id)
        assert db_publisher is None

    def test_delete_with_books(
        self, db_session, sample_publisher, sample_book, sample_author
    ):
        # Verify the publisher has books
        assert hasattr(sample_publisher, "books")
        assert sample_publisher.books.count() > 0

        book_id = sample_book.id

        # Delete the publisher
        result = PublisherRepository.delete(sample_publisher)
        assert result is True

        # Verify publisher is deleted
        db_session.expire_all()
        deleted_publisher = db_session.get(Publisher, sample_publisher.id)
        assert deleted_publisher is None

        # Verify book still exists but publisher_id is None
        db_book = db_session.get(Book, book_id)
        assert db_book is not None
        assert db_book.publisher_id is None

    def test_search_by_name(self, db_session):
        # Create publishers with various names
        names = [
            "O'Reilly Media",
            "Packt Publishing",
            "Manning Publications",
            "Apress Media",
            "No Starch Press",
        ]

        for name in names:
            publisher = Publisher(
                name=name,
                founding_year=2000,
                website=f"https://{name.lower().replace(' ', '')}.com",
            )
            db_session.add(publisher)
        db_session.commit()

        # Search for "Media"
        result = PublisherRepository.search_by_name("Media", page=1, per_page=10)
        assert len(result.items) == 2
        assert all("Media" in publisher.name for publisher in result.items)

        # Search for "Press"
        result = PublisherRepository.search_by_name("press", page=1, per_page=10)
        assert len(result.items) == 2
        print([publisher.name for publisher in result.items])
        assert all("press" in publisher.name.lower() for publisher in result.items)

        # Test with partial match
        result = PublisherRepository.search_by_name("Pack", page=1, per_page=10)
        assert len(result.items) == 1
        assert "Pack" in result.items[0].name

        # Test with no match
        result = PublisherRepository.search_by_name("XYZ", page=1, per_page=10)
        assert len(result.items) == 0
