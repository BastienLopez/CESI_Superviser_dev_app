from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://mongo:27017/")  # Assurez-vous que ce port correspond à celui dans docker-compose
db = client["productdb"]

# Création des collections pour les produits et le panier et ajout de données de test
def setup_product_db():
    products_collection = db["products"]
    cart_collection = db["carts"]
    
    # Vider les collections pour éviter les doublons
    products_collection.delete_many({})
    cart_collection.delete_many({})
    
    # Insertion de produits de test
    products_collection.insert_many([
        {"product_id": "1", "name": "Chaussures de sport", "price": 49.99},
        {"product_id": "2", "name": "T-shirt", "price": 19.99},
        {"product_id": "3", "name": "Casquette", "price": 14.99}
    ])
    print("Base de données des produits initialisée avec succès.")

if __name__ == "__main__":
    setup_product_db()
