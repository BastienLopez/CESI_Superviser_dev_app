import unittest
from main import app

class TestFrontendService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenue sur Breizhsport', response.data)

if __name__ == '__main__':
    unittest.main()
