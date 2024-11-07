from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

from controllers.auth_controller import auth_bp
from controllers.product_controller import product_bp
from controllers.cart_controller import cart_bp


app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017"))
db = client["breizhsportdb"]
products_collection = db["products"]

@app.route("/")
def home():
    # Récupérer les produits depuis MongoDB
    print("Tentative de récupération des produits depuis MongoDB...")
    products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))

    # Log du contenu de la liste products pour vérifier
    if products:
        print(f"Produits récupérés : {products}")
    else:
        print("Aucun produit trouvé dans la collection 'products'.")

    return render_template("index.html", products=products)

@app.route("/api/products")
def get_products():
    # Récupérer les produits depuis MongoDB
    print("API - Tentative de récupération des produits depuis MongoDB...")
    products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))

    # Log du contenu de la liste products pour l'API
    if products:
        print(f"Produits récupérés via l'API : {products}")
    else:
        print("API - Aucun produit trouvé dans la collection 'products'.")

    return jsonify(products)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(cart_bp, url_prefix='/api/cart')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
