import pytest
from app.repositories.user_repository import UserRepository
from app.models.user import User


class TestUserRepository:
    def test_create(self, db_session):
        new_user = User(
            username="newuser", email="newuser@example.com", password="password123"
        )

        created = UserRepository.create(new_user)
        assert created is not None
        assert created.id is not None
        assert created.username == "newuser"
        assert created.email == "newuser@example.com"
        assert created.check_password("password123") is True

        # Verify in database
        db_user = db_session.get(User, created.id)
        assert db_user is not None
        assert db_user.username == "newuser"

    def test_get_by_id(self, db_session, sample_user):
        user = UserRepository.get_by_id(sample_user.id)
        assert user is not None
        assert user.id == sample_user.id
        assert user.username == "testuser"
        assert user.email == "test@example.com"

        # Test with non-existent ID
        non_existent = UserRepository.get_by_id(9999)
        assert non_existent is None

    def test_get_by_username(self, db_session, sample_user):
        user = UserRepository.get_by_username("testuser")
        assert user is not None
        assert user.id == sample_user.id
        assert user.username == "testuser"

        # Test with non-existent username
        non_existent = UserRepository.get_by_username("nonexistent")
        assert non_existent is None

    def test_get_by_email(self, db_session, sample_user):
        user = UserRepository.get_by_email("test@example.com")
        assert user is not None
        assert user.id == sample_user.id
        assert user.email == "test@example.com"

        # Test with non-existent email
        non_existent = UserRepository.get_by_email("nonexistent@example.com")
        assert non_existent is None

    def test_update(self, db_session, sample_user):
        sample_user.username = "updateduser"
        sample_user.email = "updated@example.com"

        updated = UserRepository.update(sample_user)
        assert updated is not None
        assert updated.username == "updateduser"
        assert updated.email == "updated@example.com"

        # Verify in database
        db_session.expire_all()
        db_user = db_session.get(User, sample_user.id)
        assert db_user.username == "updateduser"
        assert db_user.email == "updated@example.com"

    def test_delete(self, db_session, sample_user):
        UserRepository.delete(sample_user)

        # Verify deletion
        db_session.expire_all()
        db_user = db_session.get(User, sample_user.id)
        assert db_user is None
