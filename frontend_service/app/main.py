from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__, template_folder='templates')

# URLs des services d'authentification et de produits
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8002")


# Page d'accueil
@app.route("/")
def home():
    return render_template("index.html")


# Page des produits
@app.route("/products")
def products():
    try:
        # Récupérer les produits depuis le service product_service
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
        product_response.raise_for_status()
        products = product_response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des produits: {e}")
        products = []

    return render_template("products.html", products=products)


# Page d'inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            try:
                response = requests.post(f"{AUTH_SERVICE_URL}/auth/signup", json={"username": username, "password": password})
                if response.status_code == 201:
                    return render_template("login.html", message="Inscription réussie. Veuillez vous connecter.")
                else:
                    return render_template("register.html", error="Erreur lors de l'inscription.")
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de l'inscription: {e}")
                return render_template("register.html", error="Service d'authentification indisponible.")
    return render_template("register.html")


# Page de connexion
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            try:
                response = requests.post(f"{AUTH_SERVICE_URL}/auth/login", json={"username": username, "password": password})
                if response.status_code == 200:
                    token = response.json().get("token")
                    return render_template("index.html", message="Connexion réussie.", token=token)
                else:
                    return render_template("login.html", error="Identifiants incorrects.")
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la connexion: {e}")
                return render_template("login.html", error="Service d'authentification indisponible.")
    return render_template("login.html")


# Page de contact
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Vérification des services
@app.route("/health")
def health_check():
    try:
        auth_response = requests.get(f"{AUTH_SERVICE_URL}/auth/validate")
        auth_status = auth_response.status_code == 200
    except requests.exceptions.RequestException:
        auth_status = False

    try:
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
        product_status = product_response.status_code == 200
    except requests.exceptions.RequestException:
        product_status = False

    return {
        "auth_service": auth_status,
        "product_service": product_status
    }, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
