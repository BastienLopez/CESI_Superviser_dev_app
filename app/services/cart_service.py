from app.extensions import mongo
from app.models.cart import Cart


class CartService:
    @staticmethod
    def create_cart(user_id, products):
        """ Crée un nouveau panier pour l'utilisateur. """
        cart = Cart(user_id=user_id, products=products)
        carts_collection = mongo["carts"]

        try:
            # Utilise to_dict() pour transformer l'objet Cart en dictionnaire
            carts_collection.insert_one(cart.to_dict())
            print("Panier créé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création du panier: {e}")

    @staticmethod
    def get_cart(user_id):
        """ Récupère le panier d'un utilisateur donné. """
        carts_collection = mongo["carts"]
        cart_data = carts_collection.find_one({"user_id": user_id})

        if cart_data is None:
            print(f"Aucun panier trouvé pour l'utilisateur {user_id}.")
            return None  # Vous pouvez retourner un message ou une structure vide si nécessaire.
        return cart_data

    @classmethod
    def add_to_cart(cls, user_id, product_id, quantity):
        """ Ajoute un produit au panier de l'utilisateur. """
        carts_collection = mongo["carts"]
        cart_data = carts_collection.find_one({"user_id": user_id})

        if cart_data is None:
            # Crée un nouveau panier si aucun n'existe
            new_cart = Cart(user_id=user_id, products=[{"product_id": product_id, "quantity": quantity}])
            try:
                carts_collection.insert_one(new_cart.to_dict())
                print(f"Produit ajouté au panier de l'utilisateur {user_id}.")
            except Exception as e:
                print(f"Erreur lors de l'ajout du produit: {e}")
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

            try:
                carts_collection.update_one(
                    {"user_id": user_id},
                    {"$set": {"products": products}}  # 'products' au lieu de 'items'
                )
                print(f"Produit ajouté ou mis à jour dans le panier de l'utilisateur {user_id}.")
            except Exception as e:
                print(f"Erreur lors de la mise à jour du panier: {e}")
