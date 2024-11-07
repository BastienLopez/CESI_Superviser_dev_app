from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://mongo:27017/")
db = client["authdb"]

def setup_auth_db():
    users_collection = db["users"]
    users_collection.delete_many({})
    
    # Ajout d'utilisateurs de test avec le même hashage que dans main.py
    users_collection.insert_many([
        {"username": "user1", "password": bcrypt.hashpw("password1".encode("utf-8"), bcrypt.gensalt())},
        {"username": "user2", "password": bcrypt.hashpw("password2".encode("utf-8"), bcrypt.gensalt())}
    ])
    print("Base de données d'authentification initialisée avec succès.")

if __name__ == "__main__":
    setup_auth_db()
