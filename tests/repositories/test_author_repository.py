import pytest
from app.repositories.author_repository import AuthorRepository
from app.models.author import Author
from sqlalchemy.exc import IntegrityError


class TestAuthorRepository:
    def test_get_all(self, db_session, sample_author):
        # Create additional authors for pagination testing
        for i in range(5):
            author = Author(
                first_name=f"Test{i}",
                last_name=f"Author{i}",
                biography=f"Biography {i}",
                birth_date=None,
            )
            db_session.add(author)
        db_session.commit()

        # Test first page
        result = AuthorRepository.get_all(page=1, per_page=3)
        assert result.items is not None
        assert len(result.items) == 3
        assert result.page == 1
        assert result.per_page == 3
        assert result.total == 6  # 5 new authors + 1 sample author

        # Test second page
        result = AuthorRepository.get_all(page=2, per_page=3)
        assert len(result.items) == 3
        assert result.page == 2

    def test_get_by_id(self, db_session, sample_author):
        author = AuthorRepository.get_by_id(sample_author.id)
        assert author is not None
        assert author.id == sample_author.id
        assert author.first_name == "Test"
        assert author.last_name == "Author"

        # Test with non-existent ID
        non_existent = AuthorRepository.get_by_id(9999)
        assert non_existent is None

    def test_create(self, db_session):
        new_author = Author(
            first_name="New",
            last_name="Author",
            biography="A new test author",
            birth_date=None,
        )

        created = AuthorRepository.create(new_author)
        assert created is not None
        assert created.id is not None
        assert created.first_name == "New"
        assert created.last_name == "Author"

        # Verify in database
        db_author = db_session.get(Author, created.id)
        assert db_author is not None
        assert db_author.first_name == "New"

    def test_update(self, db_session, sample_author):
        sample_author.first_name = "Updated"
        sample_author.biography = "Updated biography"

        updated = AuthorRepository.update(sample_author)
        assert updated is not None
        assert updated.first_name == "Updated"
        assert updated.biography == "Updated biography"

        # Verify in database
        db_session.expire_all()
        db_author = db_session.get(Author, sample_author.id)
        assert db_author.first_name == "Updated"
        assert db_author.biography == "Updated biography"

    def test_delete_author_without_books(self, db_session, sample_author):
        # Ensure the author has no books
        assert sample_author.books.count() == 0

        result = AuthorRepository.delete(sample_author)
        assert result is True

        # Verify deletion
        db_session.expire_all()
        db_author = db_session.get(Author, sample_author.id)
        assert db_author is None

    def test_delete_author_with_books(self, db_session, sample_author, sample_book):
        # Verify the author has books
        assert sample_author.books.count() > 0

        result = AuthorRepository.delete(sample_author)
        assert result is False

        # Verify author still exists
        db_session.expire_all()
        db_author = db_session.get(Author, sample_author.id)
        assert db_author is not None

    def test_search_by_name(self, db_session, sample_author):
        # Create additional authors for search testing
        names = [("John", "Doe"), ("Jane", "Smith"), ("John", "Smith"), ("Jane", "Doe")]

        for first, last in names:
            author = Author(
                first_name=first,
                last_name=last,
                biography=f"Biography for {first} {last}",
                birth_date=None,
            )
            db_session.add(author)
        db_session.commit()

        # Search by first name
        result = AuthorRepository.search_by_name("John", page=1, per_page=10)
        assert len(result.items) == 2
        assert all("John" in author.first_name for author in result.items)

        # Search by last name
        result = AuthorRepository.search_by_name("Doe", page=1, per_page=10)
        assert len(result.items) == 2
        assert all("Doe" in author.last_name for author in result.items)

        # Test partial match
        result = AuthorRepository.search_by_name("Sm", page=1, per_page=10)
        assert len(result.items) == 2
        assert all("Sm" in author.last_name for author in result.items)

        # Test with no match
        result = AuthorRepository.search_by_name("XYZ", page=1, per_page=10)
        assert len(result.items) == 0
