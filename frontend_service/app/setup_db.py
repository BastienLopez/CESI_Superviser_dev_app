from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://mongo:27017")
db = client["breizhsportdb"]
products_collection = db["products"]

# Supprime tous les documents pour éviter les doublons
products_collection.delete_many({})

# Insère des produits d'exemple
products = [
    {"name": "Produit 1", "price": 29.99, "image_url": "https://via.placeholder.com/200"},
    {"name": "Produit 2", "price": 39.99, "image_url": "https://via.placeholder.com/200"},
    {"name": "Produit 3", "price": 49.99, "image_url": "https://via.placeholder.com/200"}
]

products_collection.insert_many(products)
print("Les produits ont été insérés dans MongoDB")
