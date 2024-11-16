from flask import Flask, render_template
from app import create_app
from app.extensions import mongo

# Créer l'application Flask
app = create_app()

@app.route("/")
def home():
    """Page principale affichant les produits."""
    products_collection = mongo.db["products"]
    products = list(products_collection.find({}, {"_id": 0, "name": 1, "price": 1, "image_url": 1}))
    return render_template("index.html", products=products)

if __name__ == "__main__":
    # Lancer le serveur Flask
    app.run(host="0.0.0.0", port=8000)
