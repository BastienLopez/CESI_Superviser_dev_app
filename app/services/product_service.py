from app.extensions import mongo
from app.models.product import Product


class ProductService:
    @staticmethod
    def add_product(name, price, image_url):
        product = Product(name, price, image_url)
        products_collection = mongo["products"]
        products_collection.insert_one(product.to_dict())
        print("Produit ajouté avec succès.")

    @staticmethod
    def get_all_products():
        products_collection = mongo["products"]
        products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))
        return products
