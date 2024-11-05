import unittest
from main import app
from flask import json
from pymongo import MongoClient
import os

class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"{test}: OK")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"{test}: Erreur (cf erreur)")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"{test}: Erreur (cf erreur)")

class CustomTestRunner(unittest.TextTestRunner):
    resultclass = CustomTestResult

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True

        cls.mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017"))
        cls.db = cls.mongo_client["breizhsportdb"]
        cls.products_collection = cls.db["products"]
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        cls.products_collection.delete_many({})
        cls.mongo_client.close()

    @classmethod
    def setup_test_data(cls):
        test_products = [
            {"name": "Produit Test 1", "price": 19.99, "image_url": "https://via.placeholder.com/200"},
            {"name": "Produit Test 2", "price": 29.99, "image_url": "https://via.placeholder.com/200"},
            {"name": "Produit Test 3", "price": 39.99, "image_url": "https://via.placeholder.com/200"}
        ]
        cls.products_collection.insert_many(test_products)

    def test_home_page(self):
        """Test de la route principale '/'."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bienvenue sur Breizhsport', response.data.decode('utf-8'))
        self.assertIn('Découvrez nos articles de sport de haute qualité', response.data.decode('utf-8'))

    def test_api_products(self):
        """Test de l'API '/api/products' pour vérifier le retour des produits."""
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, "La liste des produits est vide.")

    def test_product_structure(self):
        """Test pour vérifier la structure de chaque produit dans la réponse de l'API."""
        response = self.client.get('/api/products')
        data = json.loads(response.data)
        for product in data:
            self.assertIn("name", product)
            self.assertIn("price", product)
            self.assertIn("image_url", product)
            self.assertIsInstance(product["name"], str)
            self.assertIsInstance(product["price"], (int, float))
            self.assertIsInstance(product["image_url"], str)

    def test_inserted_products_in_db(self):
        """Test pour s'assurer que les produits de test sont bien insérés dans MongoDB."""
        products = list(self.products_collection.find())
        self.assertGreater(len(products), 0, "La collection 'products' dans MongoDB est vide.")
        first_product = products[0]
        self.assertIn("name", first_product)
        self.assertIn("price", first_product)
        self.assertIn("image_url", first_product)

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())
