from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://mongo:27017")
db = client["breizhsportdb"]
products_collection = db["products"]

# Supprimer tous les documents existants pour éviter les doublons
products_collection.delete_many({})

# Insérer des produits par défaut
products = [
    {"name": "Produit 1", "price": 29.99, "image_url": "https://via.placeholder.com/200"},
    {"name": "Produit 2", "price": 39.99, "image_url": "https://via.placeholder.com/200"},
    {"name": "Produit 3", "price": 49.99, "image_url": "https://via.placeholder.com/200"}
]

result = products_collection.insert_many(products)
print(f"{len(result.inserted_ids)} produits insérés dans MongoDB")
