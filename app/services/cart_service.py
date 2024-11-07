from app.extensions import db
from app.models.cart import Cart

class CartService:
    @staticmethod
    def create_cart(user_id, products):
        cart = Cart(user_id, products)
        carts_collection = db["carts"]
        carts_collection.insert_one(cart.to_dict())
        print("Panier créé avec succès.")

    @staticmethod
    def get_cart(user_id):
        carts_collection = db["carts"]
        cart_data = carts_collection.find_one({"user_id": user_id})
        return cart_data
