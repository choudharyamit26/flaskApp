from unittest.mock import patch, MagicMock
from app.services.auth_service import AuthService
from app.models.user import User
from app import create_app

app = create_app()


class TestAuthService:
    @patch("app.repositories.user_repository.UserRepository.get_by_username")
    @patch("app.repositories.user_repository.UserRepository.get_by_email")
    @patch("app.repositories.user_repository.UserRepository.create")
    def test_register_success(
        self, mock_create, mock_get_by_email, mock_get_by_username
    ):
        username = "newuser"
        email = "newuser@example.com"
        password = "password123"

        mock_get_by_username.return_value = None
        mock_get_by_email.return_value = None

        def create_side_effect(user):
            user.id = 1
            return user

        mock_create.side_effect = create_side_effect

        with app.app_context():
            result, status_code = AuthService.register(username, email, password)

        assert status_code == 201
        assert result["success"] is True
        assert result["message"] == "User registered successfully"
        assert result["user"]["id"] == 1
        assert result["user"]["username"] == username
        assert result["user"]["email"] == email
        mock_get_by_username.assert_called_once_with(username)
        mock_get_by_email.assert_called_once_with(email)
        mock_create.assert_called_once()

    @patch("app.repositories.user_repository.UserRepository.get_by_username")
    def test_register_username_exists(self, mock_get_by_username):
        username = "existinguser"
        email = "new@example.com"
        password = "password123"

        mock_get_by_username.return_value = MagicMock(
            username=username, email="existing@example.com", password="hashed_password"
        )

        with app.app_context():
            result, status_code = AuthService.register(username, email, password)

        assert status_code == 400
        assert result["success"] is False
        assert result["message"] == "Username already exists"
        mock_get_by_username.assert_called_once_with(username)

    @patch("app.repositories.user_repository.UserRepository.get_by_username")
    @patch("app.repositories.user_repository.UserRepository.get_by_email")
    def test_register_email_exists(self, mock_get_by_email, mock_get_by_username):
        username = "newuser"
        email = "existing@example.com"
        password = "password123"

        mock_get_by_username.return_value = None
        mock_get_by_email.return_value = MagicMock(username="existinguser", email=email)

        with app.app_context():
            result, status_code = AuthService.register(username, email, password)

        assert status_code == 400
        assert result["success"] is False
        assert result["message"] == "Email already registered"
        mock_get_by_username.assert_called_once_with(username)
        mock_get_by_email.assert_called_once_with(email)

    @patch("app.services.auth_service.create_refresh_token")
    @patch("app.services.auth_service.create_access_token")
    @patch("app.repositories.user_repository.UserRepository.get_by_email")
    def test_login_success(
        self, mock_get_by_email, mock_access_token, mock_refresh_token
    ):
        email = "user@example.com"
        password = "password123"

        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = email
        mock_user.check_password.return_value = True

        mock_get_by_email.return_value = mock_user
        mock_access_token.return_value = "mock_access_token"
        mock_refresh_token.return_value = "mock_refresh_token"

        with app.app_context():
            result, status_code = AuthService.login(email, password)

        assert status_code == 200
        assert result["success"] is True
        assert result["access_token"] == "mock_access_token"
        assert result["refresh_token"] == "mock_refresh_token"
        assert result["user"]["id"] == 1
        assert result["user"]["username"] == "testuser"
        assert result["user"]["email"] == email

    @patch("app.repositories.user_repository.UserRepository.get_by_email")
    def test_login_invalid_email(self, mock_get_by_email):
        email = "nonexistent@example.com"
        password = "password123"

        mock_get_by_email.return_value = None

        with app.app_context():
            result, status_code = AuthService.login(email, password)

        assert status_code == 401
        assert result["success"] is False
        assert result["message"] == "Invalid credentials"

    @patch("app.repositories.user_repository.UserRepository.get_by_email")
    def test_login_invalid_password(self, mock_get_by_email):
        email = "user@example.com"
        password = "wrongpassword"

        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        mock_get_by_email.return_value = mock_user

        with app.app_context():
            result, status_code = AuthService.login(email, password)

        assert status_code == 401
        assert result["success"] is False
        assert result["message"] == "Invalid credentials"

    @patch("app.services.auth_service.create_access_token")
    @patch("app.repositories.user_repository.UserRepository.get_by_id")
    def test_refresh_success(self, mock_get_by_id, mock_access_token):
        user_id = 1
        mock_user = MagicMock()
        mock_user.id = user_id
        mock_user.username = "testuser"
        mock_user.email = "user@example.com"

        mock_get_by_id.return_value = mock_user
        mock_access_token.return_value = "new_access_token"

        with app.app_context():
            result, status_code = AuthService.refresh(user_id)

        assert status_code == 200
        assert result["success"] is True
        assert result["access_token"] == "new_access_token"

    @patch("app.repositories.user_repository.UserRepository.get_by_id")
    def test_refresh_user_not_found(self, mock_get_by_id):
        user_id = 999
        mock_get_by_id.return_value = None

        with app.app_context():
            result, status_code = AuthService.refresh(user_id)

        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "User not found"

    @patch("app.services.auth_service.generate_password_hash")
    @patch("app.repositories.user_repository.UserRepository.update")
    @patch("app.repositories.user_repository.UserRepository.get_by_id")
    def test_change_password_success(
        self, mock_get_by_id, mock_update, mock_generate_hash
    ):
        user_id = 1
        old_password = "oldpassword"
        new_password = "newpassword"

        mock_user = MagicMock()
        mock_user.id = user_id
        mock_user.check_password.return_value = True

        mock_get_by_id.return_value = mock_user
        mock_generate_hash.return_value = "hashed_new_password"

        with app.app_context():
            result, status_code = AuthService.change_password(
                user_id, old_password, new_password
            )

        assert status_code == 200
        assert result["success"] is True
        assert result["message"] == "Password changed successfully"
        mock_generate_hash.assert_called_once_with(new_password)
        assert mock_user.password_hash == "hashed_new_password"

    @patch("app.repositories.user_repository.UserRepository.get_by_id")
    def test_change_password_user_not_found(self, mock_get_by_id):
        user_id = 999
        old_password = "oldpassword"
        new_password = "newpassword"

        mock_get_by_id.return_value = None

        with app.app_context():
            result, status_code = AuthService.change_password(
                user_id, old_password, new_password
            )

        assert status_code == 404
        assert result["success"] is False
        assert result["message"] == "User not found"

    @patch("app.repositories.user_repository.UserRepository.get_by_id")
    def test_change_password_incorrect_old_password(self, mock_get_by_id):
        user_id = 1
        old_password = "wrongpassword"
        new_password = "newpassword"

        mock_user = MagicMock()
        mock_user.check_password.return_value = False

        mock_get_by_id.return_value = mock_user

        with app.app_context():
            result, status_code = AuthService.change_password(
                user_id, old_password, new_password
            )

        assert status_code == 401
        assert result["success"] is False
        assert result["message"] == "Incorrect password"
