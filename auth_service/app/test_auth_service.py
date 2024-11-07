import unittest
from main import app

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_register(self):
        response = self.client.post('/auth/signup', json={"username": "test", "password": "test123"})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        # S'assurer que l'utilisateur est enregistré avant de tester la connexion
        self.client.post('/auth/signup', json={"username": "test", "password": "test123"})
        response = self.client.post('/auth/login', json={"username": "test", "password": "test123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

if __name__ == '__main__':
    unittest.main()
