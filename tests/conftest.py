import pytest
from app import create_app
from app.models import Author, Publisher, Book, User
from datetime import date


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app("testing")
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def anyio_backend():
    """Specify the async backend for testing."""
    return 'asyncio'


@pytest.fixture
def event_loop():
    """Create an asyncio event loop for testing."""
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def async_session(app):
    """Provide an async session for testing."""
    async_session = app.async_session

    async def _get_session():
        async with async_session() as session:
            yield session

    return _get_session


@pytest.fixture
def auth_header(client):
    """Create a test user and return auth header with access token."""
    # Create a test user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    # Login to get access token
    response = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "password123"}
    )

    access_token = response.json["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def sample_author(async_session):
    """Create a sample author for testing."""
    async def create_author():
        async with async_session() as session:
            author = Author(
                first_name="Test",
                last_name="Author",
                biography="A test author biography",
                birth_date=date(1990, 1, 1),
            )
            session.add(author)
            await session.commit()
            return author
    return create_author


@pytest.fixture
def sample_publisher(async_session):
    """Create a sample publisher for testing."""
    async def create_publisher():
        async with async_session() as session:
            publisher = Publisher(
                name="Test Publisher", founding_year=2000, website="https://testpublisher.com"
            )
            session.add(publisher)
            await session.commit()
            return publisher
    return create_publisher


@pytest.fixture
def sample_book(async_session, sample_author, sample_publisher):
    """Create a sample book for testing."""
    async def create_book():
        async with async_session() as session:
            author = await sample_author()
            publisher = await sample_publisher()
            book = Book(
                title="Test Book",
                isbn="1234567890123",
                publication_date=date(2020, 1, 1),
                price=29.99,
                description="A test book description",
                author_id=author.id,
                publisher_id=publisher.id,
            )
            session.add(book)
            await session.commit()
            return book
    return create_book


@pytest.fixture
def sample_user(async_session):
    """Create a sample user for testing."""
    async def create_user():
        async with async_session() as session:
            user = User(username="testuser", email="test@example.com", password="password123")
            session.add(user)
            await session.commit()
            return user
    return create_user


@pytest.fixture(scope="function")
def create_test_data(app):
    """Create a comprehensive set of test data for integration tests."""
    async def create_data():
        async with app.async_session() as session:
            # Create test authors
            author1 = Author(
                first_name="Jane",
                last_name="Austen",
                biography="Classic English novelist",
                birth_date=date(1775, 12, 16),
            )
            author2 = Author(
                first_name="George",
                last_name="Orwell",
                biography="English novelist and essayist",
                birth_date=date(1903, 6, 25),
            )

            # Create test publishers
            publisher1 = Publisher(
                name="Penguin Books", founding_year=1935, website="https://www.penguin.com"
            )
            publisher2 = Publisher(
                name="HarperCollins",
                founding_year=1989,
                website="https://www.harpercollins.com",
            )

            session.add_all([author1, author2, publisher1, publisher2])
            await session.commit()

            # Create test books
            book1 = Book(
                title="Pride and Prejudice",
                isbn="9780141439518",
                publication_date=date(1813, 1, 28),
                price=9.99,
                description="A romantic novel by Jane Austen",
                author_id=author1.id,
                publisher_id=publisher1.id,
            )

            book2 = Book(
                title="1984",
                isbn="9780451524935",
                publication_date=date(1949, 6, 8),
                price=12.99,
                description="A dystopian novel by George Orwell",
                author_id=author2.id,
                publisher_id=publisher2.id,
            )

            session.add_all([book1, book2])
            await session.commit()

            test_data = {
                "authors": [
                    {
                        "id": author1.id,
                        "first_name": author1.first_name,
                        "last_name": author1.last_name,
                    },
                    {
                        "id": author2.id,
                        "first_name": author2.first_name,
                        "last_name": author2.last_name,
                    },
                ],
                "publishers": [
                    {"id": publisher1.id, "name": publisher1.name},
                    {"id": publisher2.id, "name": publisher2.name},
                ],
                "books": [
                    {"id": book1.id, "title": book1.title, "author_id": book1.author_id},
                    {"id": book2.id, "title": book2.title, "author_id": book2.author_id},
                ],
            }

            return test_data
    return create_data
