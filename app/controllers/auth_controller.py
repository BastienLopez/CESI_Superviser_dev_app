from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Vérifier la présence des champs 'username' et 'password'
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required"}), 400

    username = data.get('username')
    password = data.get('password')

    auth_service = AuthService()
    user = auth_service.login(username, password)
    print(f"Login result: {user}")

    if user:
        # Ne jamais retourner de mot de passe en clair ! Seulement des informations sécurisées
        user_data = {
            "username": user.username,  # Vous pouvez ajouter d'autres champs nécessaires
            "message": "Login successful"
        }
        return jsonify(user_data), 200

    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_service = AuthService()
    auth_service.logout()
    return jsonify({"message": "Logged out successfully"}), 200
