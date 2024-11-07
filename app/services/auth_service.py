# app/services/auth_service.py
from app.extensions import db
from app.models.user import User


class AuthService:
    @staticmethod
    def create_user(username, password):
        user = User(username, password)
        users_collection = db["users"]
        users_collection.insert_one(user.to_dict())
        print("Utilisateur créé avec succès.")

    # Méthode pour retrouver un utilisateur
    @staticmethod
    def find_user(username):
        users_collection = db["users"]
        user_data = users_collection.find_one({"username": username})
        return user_data
