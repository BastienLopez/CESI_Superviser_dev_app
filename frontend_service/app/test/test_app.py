import unittest
from main import app
from unittest.mock import patch
import requests

class TestFrontendService(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Breizhsport", response.get_data(as_text=True))

    def test_products_page(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nos produits", response.get_data(as_text=True))

    def test_register_page(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Créer un compte", response.get_data(as_text=True))

    def test_login_page(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Se connecter à votre compte", response.get_data(as_text=True))

    def test_contact_page(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nous contacter", response.get_data(as_text=True))

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("auth_service", response.get_data(as_text=True))
        self.assertIn("product_service", response.get_data(as_text=True))

    # Test supplémentaire pour vérifier la communication avec auth_service et product_service
    @patch("main.requests.get")
    def test_health_check_with_services(self, mock_get):
        # Simuler les réponses des services
        mock_get.side_effect = [
            unittest.mock.Mock(status_code=200, json=lambda: {"status": "valid"}),  # auth_service
            unittest.mock.Mock(status_code=200, json=lambda: {"products": [{"name": "Chaussures", "price": 49.99}]})  # product_service
        ]
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["auth_service"])
        self.assertTrue(data["product_service"])

    @patch("main.requests.get")
    def test_products_api(self, mock_get):
        # Simuler la réponse de l'API product_service
        mock_get.return_value = unittest.mock.Mock(status_code=200, json=lambda: {"products": [{"name": "T-shirt", "price": 19.99}]})
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Collation", response.get_data(as_text=True))

    @patch("main.requests.get")
    def test_login_page_with_auth(self, mock_get):
        # Simuler la réponse de l'API auth_service
        mock_get.return_value = unittest.mock.Mock(status_code=200, json=lambda: {"status": "valid"})
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Se connecter à votre compte", response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
