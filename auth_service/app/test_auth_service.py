import unittest
from main import app, users_collection

class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        # Réinitialiser la collection des utilisateurs avant chaque test
        users_collection.delete_many({})

    def test_register(self):
        response = self.client.post('/auth/signup', json={"username": "test", "password": "test123"})
        self.assertEqual(response.status_code, 201)

    def test_register_duplicate(self):
        # Enregistrer un utilisateur pour la première fois
        self.client.post('/auth/signup', json={"username": "test", "password": "test123"})
        # Essayer de l'enregistrer à nouveau
        response = self.client.post('/auth/signup', json={"username": "test", "password": "test123"})
        self.assertEqual(response.status_code, 409)

if __name__ == "__main__":
    unittest.main()
