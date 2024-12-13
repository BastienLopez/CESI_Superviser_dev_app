# Import sys module for modifying Python's runtime environment
import sys
# Import os module for interacting with the operating system
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import pytest for writing and running tests
import pytest

# Import the Flask app instance from the main app file
from .main import db
from .main import app

app.testing = True


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'auth_service': True}


# def test_health

# def test_signup(client):
#     response = client.post('/auth/signup', json={"username": "test", "email": "test@test.test", "password": "test"})
#     assert response.status_code == 201
#     assert response.json == {"message": "User created successfully"}
