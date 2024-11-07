# controllers/cart_controller.py

from flask import Blueprint, request, jsonify
from services.cart_service import CartService

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/', methods=['GET'])
def get_cart():
    cart = CartService.get_cart()
    return jsonify(cart), 200


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    CartService.add_to_cart(product_id, quantity)
    return jsonify({"message": "Product added to cart"}), 200
