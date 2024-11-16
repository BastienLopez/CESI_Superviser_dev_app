import os

class Config:
    """Configuration de base de l'application Flask."""

    # Clé secrète pour sécuriser les sessions et cookies
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_change_me_in_production')

    # Configuration de la base de données
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/breizhsportdb')

    # Mode de débogage
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    # Autres configurations par défaut
    JSON_SORT_KEYS = False  # Pour éviter de trier les clés JSON (si besoin)
