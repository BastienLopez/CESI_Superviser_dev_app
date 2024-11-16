import pytest
from flask import json
from unittest.mock import Mock, patch
from app import create_app
from app.models.user import User
from app import mongo


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    # Configurer une base de données de test si nécessaire
    app.config['MONGODB_DB'] = 'test_db'
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_auth_service():
    with patch('app.controllers.auth_controller.login') as mock:
        yield mock

class TestAuthController:

    def test_login_success(self, client, mock_auth_service):
        # Arrangement
        mock_user = Mock(spec=User)
        mock_user.username = "test_user"
        mock_user.check_password.return_value = True  # Mocking the password check
        mock_auth_service.return_value.find_user.return_value = mock_user  # Mock find_user

        # Action
        response = client.post('/api/auth/login',
                               data=json.dumps({
                                   'username': 'test_user',
                                   'password': 'test_password'
                               }),
                               content_type='application/json')

        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['username'] == 'test_user'
        assert data['message'] == 'Login successful'
        mock_auth_service.return_value.find_user.assert_called_once_with('test_user')
        mock_user.check_password.assert_called_once_with('test_password')

    def test_login_missing_credentials(self, client):
        # Test sans nom d'utilisateur
        response = client.post('/api/auth/login',  # Mise à jour du chemin avec le prefix
                               data=json.dumps({'password': 'test_password'}),
                               content_type='application/json')
        assert response.status_code == 400

        # Test sans mot de passe
        response = client.post('/api/auth/login',  # Mise à jour du chemin avec le prefix
                               data=json.dumps({'username': 'test_user'}),
                               content_type='application/json')
        assert response.status_code == 400

        # Test avec body vide
        response = client.post('/api/auth/login',  # Mise à jour du chemin avec le prefix
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code == 400

    def test_login_invalid_credentials(self, client, mock_auth_service):
        # Arrangement
        mock_auth_service.return_value.login.return_value = None

        # Action
        response = client.post('/api/auth/login',  # Mise à jour du chemin avec le prefix
                               data=json.dumps({
                                   'username': 'wrong_user',
                                   'password': 'wrong_password'
                               }),
                               content_type='application/json')

        # Assert
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['message'] == 'Invalid credentials'

    def test_logout_success(self, client, mock_auth_service):
        # Action
        response = client.post('/api/auth/logout')  # Mise à jour du chemin avec le prefix

        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Logged out successfully'
        mock_auth_service.return_value.logout.assert_called_once()

    def teardown_method(self, method):
        # Nettoyer la base de données de test après chaque test si nécessaire
        mongo.db.drop_collection('users')