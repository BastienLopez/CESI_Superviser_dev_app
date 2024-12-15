# Import sys module for modifying Python's runtime environment
import json
import sys
# Import os module for interacting with the operating system
import os
from unittest.mock import MagicMock, patch

import mongomock

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import pytest for writing and running tests
import pytest
import logging

# Import the Flask app instance from the main app file
from .main import Users
from .main import get_app

from mongoengine import connect, disconnect
connection = connect('mongoenginetest', host='mongodb://localhost', alias='testdb', mongo_client_class=mongomock.MongoClient)

app = get_app({
    'db': 'testdb',
    'host': 'localhost',  # Nom du service MongoDB dans Docker
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

# @pytest.fixture
# def mock_database():
#     """Mock database to simulate the Users collection."""
#     mock_users = MagicMock()
#     mock_users.objects = MagicMock()
#     # Simuler un comportement où `filter()` ne renvoie rien, et donc `first()` renverra None
#     mock_users.objects.filter.return_value.first.return_value = None  # Aucun utilisateur existant
#     return mock_users
#
# @pytest.fixture
# def setup_database(mock_database):
#     """Fixture to set up and tear down the mock database."""
#     Users.objects = mock_database.objects
#     yield
#     Users.objects.delete = MagicMock()

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


def test_signup(client, setup_database, mock_database, capsys):
    # Test d'inscription avec un utilisateur qui n'existe pas
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    logger.debug("client: %s", client)
    print("Testing signup")
    # Effectuer la requête POST pour l'inscription
    response = client.post('/auth/signup', data=json.dumps(data), content_type='application/json')

    captured = capsys.readouterr()
    assert "Testing signup" in captured.out

    # Afficher la réponse pour déboguer
    print("Response data:", response.data)

    # Vérification que la réponse est celle attendue pour un utilisateur créé
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully"}

    # Vérification que la méthode save() a été appelée pour enregistrer l'utilisateur
    mock_database.objects.save.assert_called_once()  # Vérifier que save() a bien été appelée

    # Simuler l'ajout de l'utilisateur et la recherche
    mock_database.objects.filter.return_value.first.return_value = data  # L'utilisateur existe désormais
    user = Users.objects(username="newuser").first()

    assert user is not None
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"



def test_signup_user_exists(client, setup_database, mock_database):
    # Test d'inscription avec un utilisateur qui existe déjà
    existing_user = {
        "username": "existinguser",
        "email": "existinguser@example.com",
        "password": "password123"
    }

    # Simuler qu'un utilisateur existe déjà avec le même nom d'utilisateur
    mock_database.objects.filter.return_value.first.return_value = existing_user  # Utilisateur existant

    # Données pour l'inscription
    data = {
        "username": "existinguser",
        "email": "existinguser@example.com",
        "password": "password123"
    }

    # Effectuer la requête POST pour l'inscription
    response = client.post('/auth/signup', data=json.dumps(data), content_type='application/json')

    # Vérification que la réponse est celle attendue pour un utilisateur déjà existant
    assert response.status_code == 409
    assert response.json == {"error": "User already exists"}