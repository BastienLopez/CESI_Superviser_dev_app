import unittest
from main import app

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

if __name__ == "__main__":
    unittest.main()
