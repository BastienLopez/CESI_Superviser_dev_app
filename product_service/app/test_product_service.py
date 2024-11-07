import unittest
from main import app

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.json)

    def test_add_to_cart(self):
        response = self.client.post('/cart', json={"product_id": "12345", "name": "T-shirt", "price": 19.99})
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Product added to cart")

if __name__ == '__main__':
    unittest.main()
