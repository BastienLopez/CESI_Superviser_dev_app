from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["breizhsportdb"]
products_collection = db["products"]

@app.route("/")
def home():
    """
    Route principale qui affiche la liste des produits sur la page d'accueil.
    """
    # Récupérer les produits depuis MongoDB
    products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))
    return render_template("index.html", products=products)

@app.route("/api/products")
def get_products():
    """
    API qui retourne la liste des produits au format JSON.
    """
    # Récupérer les produits depuis MongoDB
    products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
