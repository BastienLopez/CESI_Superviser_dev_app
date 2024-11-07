# controllers/product_controller.py

from flask import Blueprint, request, jsonify
from services.product_service import ProductService

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = ProductService.get_all_products()
    return jsonify(products), 200

@product_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"message": "Product not found"}), 404
