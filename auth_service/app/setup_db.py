from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Connexion à MongoDB
client = MongoClient("mongodb://mongo_auth:27017/")
db = client["authdb"]

# Création de la collection des utilisateurs et ajout de données de test
def setup_auth_db():
    users_collection = db["users"]
    
    # Vider la collection pour éviter les doublons lors de chaque exécution
    users_collection.delete_many({})
    
    # Insertion de quelques utilisateurs de test
    users_collection.insert_many([
        {"username": "user1", "password": generate_password_hash("password1")},
        {"username": "user2", "password": generate_password_hash("password2")}
    ])
    print("Base de données d'authentification initialisée avec succès.")

if __name__ == "__main__":
    setup_auth_db()
