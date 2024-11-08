import unittest
from main import app

class TestFrontendService(unittest.TestCase):
    def setUp(self):
        # Configuration du client de test Flask
        self.client = app.test_client()

    def test_homepage_contains_breizhsport(self):
        """
        Test pour vérifier si la page d'accueil contient le mot "Breizhsport"
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        # Vérifiez si le mot "Breizhsport" est présent dans la page HTML
        self.assertIn("Breizhsport", response.data.decode('utf-8'))

if __name__ == "__main__":
    unittest.main()
