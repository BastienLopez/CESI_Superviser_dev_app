from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt
import bcrypt
import os

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/authdb")
client = MongoClient(mongo_uri)
db = client["authdb"]
users_collection = db["users"]

SECRET_KEY = "secret_key"

@app.route("/auth/signup", methods=["POST"])
def signup():
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
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"status": "valid"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"status": "expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": "invalid"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
