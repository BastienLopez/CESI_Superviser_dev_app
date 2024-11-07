import unittest
from unittest.mock import patch
from main import app

class TestFrontendService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("main.requests.get")
    def test_home_with_auth_and_products(self, mock_get):
        # Mock pour le service d'authentification
        mock_get.side_effect = [
            # Premier appel pour auth_service
            unittest.mock.Mock(status_code=200, json=lambda: {"status": "valid"}),
            # Deuxième appel pour product_service
            unittest.mock.Mock(status_code=200, json=lambda: {"products": [{"name": "Chaussures", "price": 49.99}]})
        ]

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Vérifications de la réponse
        self.assertEqual(data["auth_status"], "valid")
        self.assertEqual(len(data["products"]), 1)
        self.assertEqual(data["products"][0]["name"], "Chaussures")

if __name__ == '__main__':
    unittest.main()
