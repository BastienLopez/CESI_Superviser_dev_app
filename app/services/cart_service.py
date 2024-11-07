from app.extensions import db
from app.models.cart import Cart


class CartService:
    @staticmethod
    def create_cart(user_id, products):
        # Créez une instance de Cart en passant les bons arguments
        cart = Cart(user_id=user_id, products=products)
        carts_collection = db["carts"]

        # Utilisez to_dict() pour transformer l'objet Cart en dictionnaire avant de l'insérer
        carts_collection.insert_one(cart.to_dict())
        print("Panier créé avec succès.")

    @staticmethod
    def get_cart(user_id):
        carts_collection = db["carts"]
        cart_data = carts_collection.find_one({"user_id": user_id})
        return cart_data

    @classmethod
    def add_to_cart(cls, user_id, product_id, quantity):
        carts_collection = db["carts"]
        cart_data = carts_collection.find_one({"user_id": user_id})

        if cart_data is None:
            # Crée un nouveau panier si aucun n'existe
            new_cart = Cart(user_id=user_id, products=[{"product_id": product_id, "quantity": quantity}])
            carts_collection.insert_one(new_cart.to_dict())
        else:
            # Mise à jour du panier existant
            products = cart_data["products"]  # 'products' au lieu de 'items'
            found = False
            for product in products:
                if product["product_id"] == product_id:
                    product["quantity"] += quantity
                    found = True
                    break
            if not found:
                products.append({"product_id": product_id, "quantity": quantity})

            carts_collection.update_one(
                {"user_id": user_id},
                {"$set": {"products": products}}  # 'products' au lieu de 'items'
            )
