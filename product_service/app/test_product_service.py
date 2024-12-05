import unittest
from main import app, db
from pymongo import MongoClient
import os


class TestProductService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo-product:27017/productdb")

        cls.client_db = MongoClient(mongo_uri)
        cls.db = cls.client_db["productdb"]

    @classmethod
    def tearDownClass(cls):
        cls.client_db.close()

    def setUp(self):
        self.client = app.test_client()
        self.db["products"].delete_many({})
        self.db["carts"].delete_many({})
        self.db["products"].insert_many([
            {"product_id": "1", "name": "Chaussures de sport", "price": 49.99},
            {"product_id": "2", "name": "Collation", "price": 19.99}  # Modification ici
        ])

    def tearDown(self):
        self.db["products"].delete_many({})
        self.db["carts"].delete_many({})

    def test_get_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.json)
        self.assertEqual(len(response.json["products"]), 2)

    def test_add_to_cart(self):
        response = self.client.post('/cart',
                                    json={"product_id": "1", "name": "Collation", "price": 19.99})  # Modification ici
        self.assertEqual(201, response.status_code)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Product added to cart")

        cart_response = self.client.get('/cart')
        self.assertEqual(cart_response.status_code, 200)
        self.assertEqual(len(cart_response.json["cart"]), 1)
        self.assertEqual(cart_response.json["cart"][0]["name"], "Collation")  # Modification ici

    def test_product_service_communication(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.json)


if __name__ == "__main__":
    unittest.main()
