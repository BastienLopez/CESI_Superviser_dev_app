from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client["authdb"]

@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.json
    # Inscription logique
    return jsonify({"message": "User created successfully"}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    # Authentification logique
    token = jwt.encode({"user_id": "example_id"}, "secret_key", algorithm="HS256")
    return jsonify({"token": token}), 200

@app.route("/auth/validate", methods=["GET"])
def validate():
    token = request.headers.get("Authorization")
    try:
        jwt.decode(token, "secret_key", algorithms=["HS256"])
        return jsonify({"status": "valid"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"status": "expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": "invalid"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
