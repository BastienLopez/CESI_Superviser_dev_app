from flask import Blueprint, request, jsonify
from app.services.cart_service import CartService

cart_bp = Blueprint('cart', __name__)

# Route pour récupérer le panier d'un utilisateur
@cart_bp.route('/api/cart/', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')  # Récupérer le user_id à partir des paramètres de la requête
    cart = CartService.get_cart(user_id)
    return jsonify(cart)

# Route pour ajouter un produit au panier
@cart_bp.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()  # Récupérer les données JSON de la requête
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    CartService.add_to_cart(user_id, product_id, quantity)
    return jsonify({"message": "Product added to cart"}), 200
