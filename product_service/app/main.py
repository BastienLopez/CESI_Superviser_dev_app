from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/productdb")
client = MongoClient(mongo_uri)
db = client["productdb"]

@app.route("/products", methods=["GET"])
def get_products():
    products = list(db["products"].find({}, {"_id": 0}))
    return jsonify({"products": products}), 200

@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.json
    db["carts"].insert_one(data)
    return jsonify({"message": "Product added to cart"}), 201

@app.route("/cart", methods=["GET"])
def view_cart():
    cart_items = list(db["carts"].find({}, {"_id": 0}))
    return jsonify({"cart": cart_items}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
