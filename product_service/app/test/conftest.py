from datetime import datetime

import mongomock
import pytest
from mongoengine import connect, disconnect
from product_service.app.main import app as flask_app


@pytest.fixture
def app():
    """
    Configure l'application Flask pour utiliser MongoMock
    """
    flask_app.config["TESTING"] = True
    flask_app.config["MONGODB_SETTINGS"] = {
        "db": "mongoenginetest",  # Nom de la base de données
        "host": "localhost",      # Hôte MongoMock
        # Pas besoin d'ajouter "client_class" ici
    }

    # Déconnexion de toute connexion MongoDB existante avant de se reconnecter
    disconnect()

    # Connexion à la base MongoDB (utilise MongoMock si nécessaire)
    connect(**flask_app.config["MONGODB_SETTINGS"])

    # Configurer mongomock dans le contexte des tests
    with mongomock.patch(servers=[("localhost", 27017)]):
        yield flask_app  # Rendre l'application pour le test

    disconnect()  # Déconnexion après le test


@pytest.fixture
def client(app):
    """
    Client Flask pour les tests
    """
    return app.test_client()


@pytest.fixture
def setup_data():
    """
    Adds data to the MongoMock database for testing
    """
    from product_service.app.model.product import Products
    from product_service.app.model.cart import Cart
    from auth_service.app.model.user import Users

    # Ensure the database is clean before adding new test data
    Users.objects(username="testuser").delete()

    # Add the test user
    user = Users(username="testuser", email="testuser@example.com", password="password123")
    user.save()

    # Add other necessary setup data
    product = Products(name="Test Product", price=10, storage_quantity=100)
    product.save()

    cart = Cart(user=user, products=[product], created_at=datetime.now())
    cart.save()

    return {"user": user, "product": product, "cart": cart}
