import json
import pytest
import mongomock
import jwt
from bson import ObjectId  # Pour générer un ID unique
from mongoengine import connect, disconnect
from product_service.app.main import get_app, Products, Cart
from product_service.app.main import SECRET_KEY

# Configuration de la base de test avec MongoMock
connection = connect('mongoenginetest', host='mongodb://localhost', alias='testdbproduct', mongo_client_class=mongomock.MongoClient)

app = get_app({
    'db': 'testdbproduct',
    'host': 'localhost',
    'port': 27017,
    'username': 'root',
    'password': 'example',
    'authentication_source': 'admin'
})
app.testing = True

@pytest.fixture
def client():
    """Client Flask pour les tests."""
    app.config['AUTH_SERVICE_URL'] = 'http://localhost'
    with app.test_client() as client:
        yield client

def cleanup():
    """Nettoyage de la base de test."""
    Products.drop_collection()
    Cart.drop_collection()
    disconnect(alias='testdbproduct')  # Déconnexion propre

@pytest.fixture
def create_product():
    """Fixture pour créer un produit de test."""
    product = Products(
        id=ObjectId(),  # Génération explicite de l'ID
        name="Test Product",
        description="A test product",
        price=10.0,
        storage_quantity=5
    ).save()
    yield product
    product.delete()

# Tests

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"product_service": True}

def test_get_products_empty(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert "products" in response.json
    assert len(response.json["products"]) == 0

def test_get_products_with_data(client, create_product):
    response = client.get('/products')
    assert response.status_code == 200
    products = response.json["products"]
    assert len(products) == 1
    assert products[0]["name"] == "Test Product"

def test_get_product_by_id(client, create_product):
    response = client.get(f'/products/{str(create_product.id)}')  # Conversion explicite
    assert response.status_code == 200
    product = response.json["product"]
    assert product["name"] == "Test Product"

def test_get_product_by_id_not_found(client):
    # Test avec un ID invalide (devrait renvoyer 404 pour ID invalide)
    response = client.get('/products/invalid_id')
    assert response.status_code == 404
    assert response.json == {"error": "Invalid product ID format"}

    # Test avec un ID valide mais produit introuvable (devrait renvoyer 404 pour produit non trouvé)
    invalid_product_id = '507f1f77bcf86cd799439011'  # ID valide mais pas dans la DB
    response = client.get(f'/products/{invalid_product_id}')
    assert response.status_code == 404
    assert response.json == {"error": "Product not found"}

def test_add_to_cart(client, create_product, mocker):
    # Mock validation du token
    mocker.patch('requests.get', return_value=mocker.Mock(
        status_code=200,
        json=lambda: {"user_id": "test_user"}
    ))

    token = "Bearer valid_token"
    data = {"id_product": str(create_product.id), "quantity": 2}
    response = client.post('/cart', headers={"Authorization": token}, json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Product added to cart"}

def test_add_to_cart_invalid_token(client, create_product, mocker):
    # Mock échec de validation du token
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=401))

    token = "Bearer invalid_token"
    data = {"id_product": str(create_product.id), "quantity": 2}
    response = client.post('/cart', headers={"Authorization": token}, json=data)
    assert response.status_code == 401
    assert response.json == {"error": "Invalid or expired token"}

def test_view_cart_empty(client, mocker):
    mocker.patch('jwt.decode', return_value={"user_id": "test_user"})

    token = "Bearer valid_token"
    response = client.get('/cart', headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json == {"cart": []}

def test_view_cart_with_items(client, create_product, mocker):
    Cart(id_user="test_user", id_product=create_product, quantity=2).save()

    mocker.patch('jwt.decode', return_value={"user_id": "test_user"})

    token = "Bearer valid_token"
    response = client.get('/cart', headers={"Authorization": token})
    assert response.status_code == 200
    cart = response.json["cart"]
    assert len(cart) == 1
    assert cart[0]["product"]["name"] == "Test Product"
    assert cart[0]["quantity"] == 2

def test_add_to_cart_insufficient_stock(client, create_product, mocker):
    # Mock validation du token
    mocker.patch('requests.get', return_value=mocker.Mock(
        status_code=200,
        json=lambda: {"user_id": "test_user"}
    ))

    token = "Bearer valid_token"
    data = {"id_product": str(create_product.id), "quantity": 10}  # Quantité > stock
    response = client.post('/cart', headers={"Authorization": token}, json=data)
    assert response.status_code == 400
    assert response.json == {"error": "Not enough stock available"}

# Cleanup après chaque test
@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    cleanup()


