def test_create_book(client, auth_header, create_test_data):
    author_id = create_test_data["authors"][0]["id"]
    publisher_id = create_test_data["publishers"][0]["id"]

    response = client.post(
        "/api/books",
        json={
            "title": "Sense and Sensibility",
            "isbn": "9780141439662",
            "author_id": author_id,
            "publisher_id": publisher_id,
        },
        headers=auth_header,
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["data"]["title"] == "Sense and Sensibility"
    assert response.json["data"]["author_id"] == author_id
    assert response.json["data"]["publisher_id"] == publisher_id


def test_create_book_validation_error(client, auth_header, create_test_data):
    response = client.post(
        "/api/books",
        json={
            # Missing required title
            "isbn": "9780141439662",
            "author_id": create_test_data["authors"][0]["id"],
            "publisher_id": create_test_data["publishers"][0]["id"],
        },
        headers=auth_header,
    )
    assert response.status_code == 400
    assert response.json["success"] is False


def test_get_books(client, create_test_data):
    response = client.get("/api/books/")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 2
    assert response.json["data"][0]["title"] == "Pride and Prejudice"
    assert response.json["data"][1]["title"] == "1984"


def test_get_book_by_id(client, create_test_data):
    book_id = create_test_data["books"][0]["id"]
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["title"] == "Pride and Prejudice"
    assert response.json["data"]["isbn"] == "9780141439518"


def test_get_nonexistent_book(client):
    response = client.get("/api/books/999")
    assert response.status_code == 404
    assert response.json["success"] is False


def test_update_book(client, auth_header, create_test_data):
    book_id = create_test_data["books"][0]["id"]
    response = client.put(
        f"/api/books/{book_id}",
        json={"price": 14.99, "description": "Updated description"},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["price"] == "14.99"
    assert response.json["data"]["description"] == "Updated description"
    assert response.json["data"]["title"] == "Pride and Prejudice"


def test_update_book_invalid_publisher(client, auth_header, create_test_data):
    book_id = create_test_data["books"][0]["id"]
    response = client.put(
        f"/api/books/{book_id}",
        json={"publisher_id": 999},  # Non-existent publisher
        headers=auth_header,
    )
    assert response.status_code == 404
    assert response.json["success"] is False
    assert "Publisher not found" in response.json["message"]


def test_delete_book(client, auth_header, create_test_data):
    book_id = create_test_data["books"][0]["id"]
    response = client.delete(f"/api/books/{book_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json["success"] is True

    # Verify book is deleted
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 404


def test_search_books(client, create_test_data):
    response = client.get("/api/books/search?title=Pride")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["title"] == "Pride and Prejudice"


def test_get_books_by_author(client, create_test_data):
    author_id = create_test_data["authors"][0]["id"]
    response = client.get(f"/api/books/author/{author_id}")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["title"] == "Pride and Prejudice"


def test_get_books_by_publisher(client, create_test_data):
    publisher_id = create_test_data["publishers"][0]["id"]
    response = client.get(f"/api/books/publisher/{publisher_id}")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["title"] == "Pride and Prejudice"
