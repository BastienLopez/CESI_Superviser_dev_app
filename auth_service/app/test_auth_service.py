import unittest
from main import app
import requests
import os

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        # Réinitialiser la collection des utilisateurs avant chaque test
        users_collection.delete_many({})

    def test_register(self):
        response = self.client.post('/auth/signup', json={"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 201)

    def test_register_duplicate(self):
        self.client.post('/auth/signup', json={"username": "testuser", "password": "testpass"})
        response = self.client.post('/auth/signup', json={"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 409)

    def test_login(self):
        self.client.post('/auth/signup', json={"username": "testuser", "password": "testpass"})
        response = self.client.post('/auth/login', json={"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_validate_token(self):
        signup_response = self.client.post('/auth/signup', json={"username": "testuser", "password": "testpass"})
        login_response = self.client.post('/auth/login', json={"username": "testuser", "password": "testpass"})
        token = login_response.json["token"]
        
        headers = {"Authorization": token}
        validate_response = self.client.get('/auth/validate', headers=headers)
        self.assertEqual(validate_response.status_code, 200)
        self.assertEqual(validate_response.json["status"], "valid")

    def test_auth_service_communication(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn("auth_service", response.json)
        self.assertTrue(response.json["auth_service"])


if __name__ == "__main__":
    unittest.main()
