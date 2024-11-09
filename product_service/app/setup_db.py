from pymongo import MongoClient

# Connexion à MongoDB (assurez-vous que ce port et cette URI correspondent au docker-compose)
client = MongoClient("mongodb://mongo-product:27017/")
db = client["productdb"]

# Création des collections pour les produits et le panier et ajout de données de test
def setup_product_db():
    products_collection = db["products"]
    cart_collection = db["carts"]
    
    # Vider les collections pour éviter les doublons
    products_collection.delete_many({})
    cart_collection.delete_many({})
    
    # Insertion de produits de test
    sample_products = [
        {"product_id": "1", "name": "Chaussures de sport", "price": 49.99},
        {"product_id": "2", "name": "T-shirt", "price": 19.99},
        {"product_id": "3", "name": "Casquette", "price": 14.99},
        {"product_id": "4", "name": "Sac à dos", "price": 29.99}
    ]
    products_collection.insert_many(sample_products)
    print("Base de données des produits initialisée avec succès.")

if __name__ == "__main__":
    setup_product_db()
