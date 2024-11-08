from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8002")


# Page d'accueil - maintenant rendue avec "template.html"
@app.route("/")
def home():
    return render_template("index.html")


# Page des produits
@app.route("/products")
def products():
    try:
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
        product_response.raise_for_status()
        products = product_response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des produits: {e}")
        products = []

    return render_template("products.html", products=products)


# Page d'inscription
@app.route("/register")
def register():
    return render_template("register.html")


# Page de connexion
@app.route("/login")
def login():
    return render_template("login.html")


# Page de contact
@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
