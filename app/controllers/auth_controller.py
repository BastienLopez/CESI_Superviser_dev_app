# controllers/auth_controller.py

from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = AuthService.login(username, password)
    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    AuthService.logout()
    return jsonify({"message": "Logged out successfully"}), 200
