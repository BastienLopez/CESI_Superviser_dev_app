import unittest
from main import app

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        response = self.client.post('/cart', json={"product_id": "12345"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
