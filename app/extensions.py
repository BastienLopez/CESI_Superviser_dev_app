from pymongo import MongoClient
import os

# Initialiser l'instance MongoDB ici
mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://27017:27017"))
db = mongo_client["mongo-1"]