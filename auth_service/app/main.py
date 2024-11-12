from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
import jwt
import bcrypt
import os

app = Flask(__name__)

# Connexion à MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo-auth:27017/authdb")
try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db = client["authdb"]
    users_collection = db["users"]
    client.admin.command('ping')
    print("Connecté à MongoDB avec succès")
except errors.ServerSelectionTimeoutError as err:
    print("Erreur de connexion à MongoDB:", err)
    db = None

SECRET_KEY = "secret_key"

@app.route("/auth/signup", methods=["POST"])
def signup():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "User created successfully"}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        token = jwt.encode({"user_id": str(user["_id"])}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/auth/validate", methods=["GET"])
def validate():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"status": "valid", "user_id": decoded["user_id"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint pour vérifier la santé du service d'authentification"""
    if db is None:
        return jsonify({"auth_service": False}), 500
    return jsonify({"auth_service": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
