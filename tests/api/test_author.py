import pytest
from sqlalchemy.future import select
from app.models import Book


def test_create_author(client, auth_header):
    response = client.post(
        "/api/authors",
        json={
            "first_name": "Ernest",
            "last_name": "Hemingway",
            "biography": "American novelist",
            "birth_date": "1899-07-21",
        },
        headers=auth_header,
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["data"]["first_name"] == "Ernest"
    assert response.json["data"]["last_name"] == "Hemingway"


def test_create_author_validation_error(client, auth_header):
    response = client.post(
        "/api/authors",
        json={
            # Missing required first_name
            "last_name": "Hemingway"
        },
        headers=auth_header,
    )
    assert response.status_code == 400
    assert response.json["success"] is False


def test_get_authors(client, create_test_data):
    response = client.get("/api/authors/")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 2
    assert response.json["data"][0]["first_name"] == "Jane"
    assert response.json["data"][1]["first_name"] == "George"


def test_get_author_by_id(client, create_test_data):
    author_id = create_test_data["authors"][0]["id"]
    response = client.get(f"/api/authors/{author_id}")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["first_name"] == "Jane"
    assert response.json["data"]["last_name"] == "Austen"


def test_get_nonexistent_author(client):
    response = client.get("/api/authors/999")
    assert response.status_code == 404
    assert response.json["success"] is False


def test_update_author(client, auth_header, create_test_data):
    author_id = create_test_data["authors"][0]["id"]
    response = client.put(
        f"/api/authors/{author_id}",
        json={"biography": "Updated biography"},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["biography"] == "Updated biography"
    assert response.json["data"]["first_name"] == "Jane"


@pytest.mark.asyncio
async def test_delete_author(client, auth_header, create_test_data, async_session):
    author_id = create_test_data["authors"][0]["id"]

    # First, delete all books associated with this author
    async with async_session() as session:
        books = await session.execute(
            select(Book).where(Book.author_id == author_id)
        )
        books = books.scalars().all()
        for book in books:
            await session.delete(book)
        await session.commit()

    response = client.delete(f"/api/authors/{author_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json["success"] is True

    # Verify author is deleted
    response = client.get(f"/api/authors/{author_id}")
    assert response.status_code == 404


def test_search_authors(client, create_test_data):
    response = client.get("/api/authors/search?name=Jane")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["first_name"] == "Jane"
