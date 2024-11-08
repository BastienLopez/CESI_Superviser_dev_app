from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

# Variables d'environnement pour les services
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8002")

@app.route("/")
def home():
    """
    Cette route renvoie la page HTML principale.
    """
    return render_template("index.html")

@app.route("/api/data")
def get_data():
    """
    Cette route récupère l'état d'authentification et les produits depuis les services externes
    et renvoie un JSON avec les informations.
    """
    headers = request.headers.copy()

    # Vérifier si un token est présent dans les headers
    token = headers.get("Authorization")
    if not token:
        headers["Authorization"] = "Bearer <TOKEN_DE_TEST>"  # Token par défaut pour les tests

    # Appel au service d'authentification
    try:
        auth_response = requests.get(f"{AUTH_SERVICE_URL}/auth/validate", headers=headers)
        auth_status = auth_response.json().get("status", "unknown")
    except requests.RequestException as e:
        print(f"Erreur lors de l'appel à auth_service: {e}")
        auth_status = "unknown"

    # Appel au service des produits
    try:
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
        product_response.raise_for_status()
        products = product_response.json().get("products", [])
    except requests.RequestException as e:
        print(f"Erreur lors de l'appel à product_service: {e}")
        products = []

    # Retourne le JSON avec l'état d'authentification et les produits
    return jsonify({
        "auth_status": auth_status,
        "products": products
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
