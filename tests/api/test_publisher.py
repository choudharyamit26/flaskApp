def test_create_publisher(client, auth_header):
    response = client.post(
        "/api/publishers/",
        json={
            "name": "Random House",
            "founding_year": 1927,
            "website": "https://www.randomhouse.com",
        },
        headers=auth_header,
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["data"]["name"] == "Random House"
    assert response.json["data"]["founding_year"] == 1927


def test_create_publisher_validation_error(client, auth_header):
    response = client.post(
        "/api/publishers/",
        json={
            # Missing required name
            "founding_year": 1927
        },
        headers=auth_header,
    )
    assert response.status_code == 400
    assert response.json["success"] is False


def test_get_publishers(client, create_test_data):
    response = client.get("/api/publishers/")
    assert response.status_code == 200
    assert response.json["success"] is True

    # Check that we have the expected publishers
    publishers = response.json["data"]
    assert len(publishers) == 2

    # Check publisher names (may be in different order)
    publisher_names = [p["name"] for p in publishers]
    assert "Penguin Books" in publisher_names
    assert "HarperCollins" in publisher_names


def test_get_publisher_by_id(client, create_test_data):
    publisher_id = create_test_data["publishers"][0]["id"]
    response = client.get(f"/api/publishers/{publisher_id}")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["name"] == "Penguin Books"
    assert response.json["data"]["founding_year"] == 1935


def test_get_nonexistent_publisher(client):
    response = client.get("/api/publishers/999")
    assert response.status_code == 404
    assert response.json["success"] is False


def test_update_publisher(client, auth_header, create_test_data):
    publisher_id = create_test_data["publishers"][0]["id"]
    response = client.put(
        f"/api/publishers/{publisher_id}",
        json={"website": "https://www.penguin.co.uk"},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["data"]["website"] == "https://www.penguin.co.uk"
    assert response.json["data"]["name"] == "Penguin Books"


def test_delete_publisher(client, auth_header, create_test_data):
    publisher_id = create_test_data["publishers"][1]["id"]

    response = client.delete(f"/api/publishers/{publisher_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json["success"] is True

    # Verify publisher is deleted
    response = client.get(f"/api/publishers/{publisher_id}")
    assert response.status_code == 404

    # Verify any associated books now have NULL publisher_id
    from app.models.book import Book

    with client.application.app_context():
        books_count = Book.query.filter_by(publisher_id=publisher_id).count()
        assert books_count == 0


def test_search_publishers(client, create_test_data):
    response = client.get("/api/publishers/search?name=Penguin")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["name"] == "Penguin Books"
