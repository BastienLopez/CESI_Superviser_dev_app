from mongoengine import Document, SequenceField, IntField, ReferenceField
from .product import Product  # Assurez-vous que le modèle Product est importé

class Cart(Document):
    id = SequenceField(primary_key=True)
    id_user = IntField(required=True)  # ID de l'utilisateur (pas une référence Mongo)
    id_product = ReferenceField(Product, required=True)  # Référence vers le modèle Product
    quantity = IntField(required=True, min_value=1)

    def __repr__(self):
        return f'<Cart User ID: {self.id_user}, Product: {self.id_product.name}, Quantity: {self.quantity}>'
