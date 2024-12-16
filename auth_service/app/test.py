# Import sys module for modifying Python's runtime environment
import json
import sys
# Import os module for interacting with the operating system
import os

import jwt
import mongomock


# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import pytest for writing and running tests
import pytest
import logging


from mongoengine import connect, disconnect
connection = connect('mongoenginetest', host='mongodb://localhost', alias='testdb', mongo_client_class=mongomock.MongoClient)

from main import get_app, Users, SECRET_KEY

app = get_app({
    'db': 'testdb',
    'host': 'mongo-auth',  # Nom du service MongoDB dans Docker
    'port': 27017,  # Port de MongoDB
    'username': 'root',  # Nom d'utilisateur MongoDB
    'password': 'example',  # Mot de passe MongoDB
    'authentication_source': 'admin'  # Base de données où les infos d'authentification sont stockées
})

app.testing = True
logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def create_user():
    """Fixture pour créer un utilisateur de test."""
    user = Users(username="testuser", email="testuser@example.com")
    user.set_password("password123")
    user.save()
    yield user
    user.delete()
    disconnect('mongoenginetest')


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'auth_service': True}


def test_signup_201(client):
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post('/auth/signup', data=json.dumps(data), content_type='application/json')
    try:
        assert response.status_code == 201
    finally:
        Users.objects(username="newuser").first().delete()
        disconnect('mongoenginetest')


def test_signup_409(client):
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }

    user = Users(username=data["username"], email=data["email"], password=data["password"])
    user.save()

    response = client.post('/auth/signup', data=json.dumps(data), content_type='application/json')
    try:
        assert response.status_code == 409
    finally:
        Users.objects(username="newuser").first().delete()
        disconnect('mongoenginetest')


def test_login_200(client, create_user):
    data = {
        "username": "testuser",
        "password": "password123"
    }
    try:
        response_login = client.post('/auth/login', data=json.dumps(data), content_type='application/json')

        # Vérifications
        assert response_login.status_code == 200
        assert "token" in response_login.json

        # Décodage du token
        decoded = jwt.decode(response_login.json["token"], SECRET_KEY, algorithms=["HS256"])
        assert decoded["user_id"] == str(create_user.id)
    finally:
        # Nettoyage
        disconnect('mongoenginetest')


def test_login_invalid_credentials(client):
    data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }

    response = client.post('/auth/login', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}


def test_login_missing_fields(client):
    data = {"username": "testuser"}  # Missing password

    response = client.post('/auth/login', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.json == {"error": "Username and password are required"}


def test_validate_success(client, create_user):
    # Générer un token valide
    token = jwt.encode({"user_id": str(create_user.id)}, SECRET_KEY, algorithm="HS256")

    response = client.get('/auth/validate', headers={"Authorization": token})

    assert response.status_code == 200
    assert response.json == {"status": "valid", "user_id": str(create_user.id)}

def test_validate_missing_token(client):
    response = client.get('/auth/validate')

    assert response.status_code == 400
    assert response.json == {"error": "Token is missing"}

def test_validate_invalid_token(client):
    token = "invalid.token.here"

    response = client.get('/auth/validate', headers={"Authorization": token})

    assert response.status_code == 401
    assert response.json == {"error": "Invalid token"}


def test_validate_expired_token(client, create_user):
    # Générer un token expiré (utilisation de jwt pour configurer l'expiration)
    expired_token = jwt.encode(
        {"user_id": str(create_user.id), "exp": 0}, SECRET_KEY, algorithm="HS256"
    )

    response = client.get('/auth/validate', headers={"Authorization": expired_token})

    assert response.status_code == 401
    assert response.json == {"error": "Token has expired"}


def test_signup_missing_fields(client):
    data = {
        "username": "",  # Username manquant
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post('/auth/signup', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.json == {"error": "Username, email, and password are required"}
