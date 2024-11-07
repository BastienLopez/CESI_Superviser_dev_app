import time
from flask import Flask, jsonify, render_template
from app.extensions import db
import os
from pymongo.errors import ConnectionFailure


def wait_for_mongo():
    while True:
        try:
            # Vérifiez la connexion à MongoDB en utilisant db
            db.client.admin.command('ping')
            print("MongoDB est prêt à accepter des connexions.")
            break
        except ConnectionFailure:
            print("MongoDB n'est pas encore disponible, nouvelle tentative dans 5 secondes...")
            time.sleep(5)

def create_app():
    app = Flask(__name__)

    # Attachez db à l'application Flask
    app.db = db

    # Attendre que MongoDB soit prêt
    wait_for_mongo()

    # Importation des blueprints après la création de l'app pour éviter l'import circulaire
    from .controllers.auth_controller import auth_bp
    from .controllers.product_controller import product_bp
    from .controllers.cart_controller import cart_bp

    # Enregistrer les blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')

    # Définir les routes de l'application
    @app.route("/")
    def home():
        products_collection = db["products"]
        print("Tentative de récupération des produits depuis MongoDB...")
        products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))

        if products:
            print(f"Produits récupérés : {products}")
        else:
            print("Aucun produit trouvé dans la collection 'products'.")

        return render_template("index.html", products=products)

    @app.route("/api/products")
    def get_products():
        products_collection = db["products"]
        print("API - Tentative de récupération des produits depuis MongoDB...")
        products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))

        if products:
            print(f"Produits récupérés via l'API : {products}")
        else:
            print("API - Aucun produit trouvé dans la collection 'products'.")

        return jsonify(products)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
