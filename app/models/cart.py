class CartProducts:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    def to_dict(self):
        """Convertit l'objet CartProducts en dictionnaire pour MongoDB."""
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }


class Cart:
    def __init__(self, user_id, products):
        self.user_id = user_id
        self.products = products  # Ce devrait être un champ "products" ici

    def to_dict(self):
        """Convertit l'objet Cart en dictionnaire pour MongoDB."""
        return {
            "user_id": self.user_id,
            "products": self.products  # Conversion de products en dictionnaire
        }
