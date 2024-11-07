# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialiser l'application Flask et la base de données
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configuration de la base de données
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # Exemple avec SQLite, ajustez pour MongoDB si nécessaire
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisation de la base de données avec l'application Flask
    db.init_app(app)

    # Importer et enregistrer les modèles (c'est important d'importer après l'initialisation de la base de données)
    from .models import User, Product  # Assurez-vous que les modèles sont bien importés ici

    # Autres initialisations ou configurations (par exemple les blueprints, etc.)

    return app
