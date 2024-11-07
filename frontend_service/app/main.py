from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8002")

# Route pour afficher le contenu HTML
@app.route("/")
def home():
    return render_template("index.html")

# Route pour obtenir l'état de l'authentification et les produits
@app.route("/api/data")
def get_data():
    headers = request.headers.copy()
    
    # Vérifier si un token est présent
    token = headers.get("Authorization")
    if not token:
        headers["Authorization"] = "Bearer <TOKEN_DE_TEST>"  # Remplacez <TOKEN_DE_TEST> par un token valide si nécessaire.

    # Appel à `auth_service` pour vérifier l'authentification
    auth_response = requests.get(f"{AUTH_SERVICE_URL}/auth/validate", headers=headers)
    auth_status = auth_response.json().get("status", "unknown")

    # Appel à `product_service`
    try:
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
        product_response.raise_for_status()
        products = product_response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion au service produit : {e}")
        products = []

    return jsonify({"auth_status": auth_status, "products": products}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
