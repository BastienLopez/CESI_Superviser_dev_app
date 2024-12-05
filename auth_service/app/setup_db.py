from pymongo import MongoClient
import bcrypt
import os

# Connexion à la base de données MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo-auth:27017/authdb")

client = MongoClient(mongo_uri)
db = client["authdb"]

def setup_auth_db():
    users_collection = db["users"]
    
    # Supprimer les utilisateurs existants pour éviter les doublons lors de chaque exécution
    users_collection.delete_many({})
    
    # Ajouter des utilisateurs de test
    sample_users = [
        {"username": "user1", "password": bcrypt.hashpw("password1".encode("utf-8"), bcrypt.gensalt())},
        {"username": "user2", "password": bcrypt.hashpw("password2".encode("utf-8"), bcrypt.gensalt())},
        {"username": "admin", "password": bcrypt.hashpw("adminpass".encode("utf-8"), bcrypt.gensalt())}
    ]
    
    users_collection.insert_many(sample_users)
    print("Base de données d'authentification initialisée avec succès.")

if __name__ == "__main__":
    setup_auth_db()
