import base64

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import requests  # Importation de requests pour effectuer les appels HTTP
from mongoengine import DoesNotExist  # Importation de l'exception DoesNotExist
from mongoengine import Document, SequenceField, IntField, ReferenceField
import mongoengine as db


class Products(db.Document):
    id = db.ObjectIdField(primary_key=True)
    name = db.StringField(required=True, max_length=100)
    description = db.StringField()
    price = db.FloatField(required=True)
    image = db.BinaryField()
    storage_quantity = db.IntField(required=True)

    def __repr__(self):
        return f'<Product {self.name}>'


class Cart(Document):
    id = SequenceField(primary_key=True)
    id_user = IntField(required=True)  # ID de l'utilisateur (pas une référence Mongo)
    id_product = ReferenceField(Products, required=True)  # Référence vers le modèle Product
    quantity = IntField(required=True, min_value=1)

    def __repr__(self):
        return f'<Cart User ID: {self.id_user}, Product: {self.id_product.name}, Quantity: {self.quantity}>'


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'productdb',
    'host': 'mongo-product',  # Nom du service MongoDB dans Docker
    'port': 27017,  # Port de MongoDB
    'username': 'root',  # Nom d'utilisateur MongoDB
    'password': 'example',  # Mot de passe MongoDB
    'authentication_source': 'admin'  # Base de données où les infos d'authentification sont stockées
}
db = MongoEngine(app)

# URL de l'API de auth_service (mettre l'URL correcte)
AUTH_SERVICE_URL = "http://auth_service:8001"


# @app.route("/products/<string:product_id>/image", methods=["POST"])
# def upload_product_image(product_id):
#     file = request.files.get('image')
#     if not file:
#         return jsonify({"error": "No image file provided"}), 400
#
#     try:
#         product = Products.objects.get(id=product_id)
#         product.image = file.read()  # Lire les données binaires du fichier
#         product.save()
#         return jsonify({"message": "Image uploaded successfully"}), 200
#     except DoesNotExist:
#         return jsonify({"error": "Product not found"}), 404

@app.route("/products/<product_id>/image", methods=["GET"])
def get_product_image(product_id):
    try:
        product = Products.objects.get(id=product_id)
        if not product.image:
            return jsonify({"error": "No image available for this product"}), 404

        # Si l'image est en Base64, nous devons la décoder en binaire
        image_data = base64.b64decode(product.image)

        # Retourne l'image sous forme de réponse HTTP avec le type MIME approprié
        return app.response_class(image_data, content_type="image/png"), 200
    except DoesNotExist:
        return jsonify({"error": "Product not found"}), 404


@app.route("/products", methods=["GET"])
def get_products():
    products = Products.objects()
    response = [
        {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image": f"/products/{product.id}/image" if product.image else None,
            "storage_quantity": product.storage_quantity,
        }
        for product in products
    ]
    return jsonify({"products": response}), 200


@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.json

    if not data or not all(key in data for key in ["id_user", "id_product", "quantity"]):
        return jsonify({"error": "Invalid data"}), 400

    try:
        # Appel à l'API auth_service pour obtenir les informations de l'utilisateur
        user_response = requests.get(f"{AUTH_SERVICE_URL}/users/{data['id_user']}")

        if user_response.status_code != 200:
            return jsonify({"error": "User not found in auth_service"}), 404

        user_data = user_response.json()  # Utilisation des données utilisateur récupérées

        # Recherche du produit
        try:
            product = Products.objects.get(id=data["id_product"])
        except DoesNotExist:
            return jsonify({"error": "Product not found"}), 404

        if product.storage_quantity < data["quantity"]:
            return jsonify({"error": "Not enough stock available"}), 400

        # Crée un élément de panier avec juste l'ID de l'utilisateur
        cart_item = Cart(
            id_user=data["id_user"],  # Juste l'ID de l'utilisateur
            id_product=product,
            quantity=data["quantity"]
        )
        cart_item.save()
        return jsonify({"message": "Product added to cart"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cart", methods=["GET"])
def view_cart():
    cart_items = Cart.objects()
    response = [
        {
            "user": str(item.id_user.username) if item.id_user else "Unknown",  # Correction de l'accès à 'username'
            "product": str(item.id_product.name),
            "quantity": item.quantity,
            "total_price": item.quantity * item.id_product.price
        }
        for item in cart_items
    ]
    return jsonify({"cart": response}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
