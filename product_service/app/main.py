import base64
import logging

import jwt
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import requests  # Importation de requests pour effectuer les appels HTTP
from mongoengine import DoesNotExist, StringField, ValidationError  # Importation de l'exception DoesNotExist
from mongoengine import Document, SequenceField, IntField, ReferenceField
import mongoengine as db

SECRET_KEY = "secret_key"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    id_user = StringField(required=True)  # ID de l'utilisateur (pas une référence Mongo)
    id_product = ReferenceField(Products, required=True)  # Référence vers le modèle Product
    quantity = IntField(required=True, min_value=1)

    def __repr__(self):
        return f'<Cart User ID: {self.id_user}, Product: {self.id_product.name}, Quantity: {self.quantity}>'


def get_app(config, auth_service_url=None):
    app = Flask(__name__)

    # Configuration de MongoDB
    app.config['MONGODB_SETTINGS'] = config

    # Initialisation de MongoEngine
    db = MongoEngine(app)

    # Ajout de l'URL du service d'authentification à la configuration de l'application
    if auth_service_url:
        app.config['AUTH_SERVICE_URL'] = auth_service_url

    # Retourne l'instance de l'application Flask




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

    @app.route("/products/<product_id>", methods=["GET"])
    def get_product_by_id(product_id):
        try:
            # Recherche du produit par son ID
            product = Products.objects.get(id=product_id)
        except DoesNotExist:
            # Gestion du cas où le produit n'est pas trouvé
            return jsonify({"error": "Product not found"}), 404
        except ValidationError:
            # Gestion des erreurs liées à un format d'ID non valide
            return jsonify({"error": "Invalid product ID format"}), 400

        # Construction de la réponse
        response = {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image": f"/products/{product.id}/image" if product.image else None,
            "storage_quantity": product.storage_quantity,
        }

        return jsonify({"product": response}), 200


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

        if not data or not all(key in data for key in ["id_product", "quantity"]):
            return jsonify({"error": "Invalid data"}), 400

        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 400

        # Appel à l'endpoint /auth/validate pour valider le token
        validate_response = requests.get(
            f"{app.config['AUTH_SERVICE_URL']}/auth/validate",
            headers={"Authorization": token}
        )

        if validate_response.status_code != 200:
            return jsonify({"error": "Invalid or expired token"}), validate_response.status_code

        validation_data = validate_response.json()
        user_id = validation_data.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID not found"}), 400

        # Recherche du produit
        try:
            product = Products.objects.get(id=data["id_product"])
        except DoesNotExist:
            return jsonify({"error": "Product not found"}), 404

        if product.storage_quantity < data["quantity"]:
            return jsonify({"error": "Not enough stock available"}), 400

        # Crée un élément de panier avec l'ID utilisateur validé
        cart_item = Cart(
            id_user=user_id,
            id_product=product,
            quantity=data["quantity"]
        )
        cart_item.save()

        return jsonify({"message": "Product added to cart"}), 201


    @app.route("/cart", methods=["GET"])
    def view_cart():
        # Récupérer le token Authorization
        token = request.headers.get("Authorization")
        product = None
        if not token:
            return jsonify({"error": "Token is missing"}), 400

        try:
            # Vérifier et décoder le token pour obtenir l'user_id
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        # Récupérer les éléments du panier pour cet utilisateur
        cart_items = Cart.objects(id_user=user_id)
        if not cart_items:
            return jsonify({"cart": []}), 200  # Renvoie un panier vide si aucun article trouvé

        # Construire la réponse avec les détails du produit
        response = []
        for item in cart_items:
            # Appeler get_product_by_id pour obtenir les détails du produit
            try:
                product = Products.objects.get(id=item.id_product.id)
                product_details = {
                    "id": str(product.id),
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "image": f"/products/{product.id}/image" if product.image else None,
                }
            except DoesNotExist:
                product_details = {"error": "Product not found"}

            # Ajouter l'article du panier à la réponse
            response.append({
                "product": product_details,
                "quantity": item.quantity,
                "total_price": item.quantity * product.price if "price" in product_details else 0,
            })

        return jsonify({"cart": response}), 200

    @app.route("/health", methods=["GET"])
    def health_check():
        if db is None:
            return jsonify({"product_service": False}), 500
        return jsonify({"product_service": True}), 200

    return app


if __name__ == "__main__":
    config = {
        'db': 'productdb',
        'host': 'mongo-product',  # Nom du service MongoDB dans Docker
        'port': 27017,  # Port de MongoDB
        'username': 'root',  # Nom d'utilisateur MongoDB
        'password': 'example',  # Mot de passe MongoDB
        'authentication_source': 'admin'  # Base de données où les infos d'authentification sont stockées
    }

    # Initialisation de l'application avec l'URL du service d'authentification
    auth_service_url = "http://auth_service:8001"

    app = get_app(config, auth_service_url=auth_service_url)
    app.run(host="0.0.0.0", port=8002)
