from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    auth_service = AuthService()
    user = auth_service.login(username, password)
    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_service = AuthService()
    auth_service.logout()
    return jsonify({"message": "Logged out successfully"}), 200