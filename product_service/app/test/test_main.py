from unittest.mock import patch
import pytest
from ..model.cart import Cart
from ..model.product import Products


@pytest.fixture
def mock_auth_service():
    with patch("requests.get") as mock_get:
        yield mock_get  # Renvoie le mock pour les tests


def test_get_products(client, setup_data):
    """
    Teste la route GET /products
    """
    response = client.get("/products")
    assert response.status_code == 200

    data = response.get_json()
    assert "products" in data
    assert len(data["products"]) > 0
    assert data["products"][0]["name"] == "Test Product"


def test_add_to_cart(client, setup_data, mock_auth_service):
    """
    Teste la route POST /cart
    """
    user = setup_data["user"]
    product = setup_data["product"]

    # Mock de la réponse de l'auth_service
    mock_auth_service.return_value.status_code = 200
    mock_auth_service.return_value.json.return_value = {
        "id": str(user.id),
        "username": user.username,
        "email": user.email
    }

    payload = {
        "id_user": str(user.id),  # Convertir l'ID de l'utilisateur en chaîne
        "id_product": str(product.id),  # Convertir l'ID du produit en chaîne
        "quantity": 2
    }

    response = client.post("/cart", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Product added to cart"

    # Vérifie que l'élément a été ajouté au panier
    cart_items = Cart.objects()
    assert len(cart_items) == 1
    assert cart_items[0].id_user == str(user.id)  # Vérifie que l'ID utilisateur est correctement stocké
    assert cart_items[0].id_product == product
    assert cart_items[0].quantity == 2


def test_view_cart(client, setup_data):
    """
    Teste la route GET /cart
    """
    user = setup_data["user"]
    product = setup_data["product"]

    # Ajoute un élément dans le panier
    cart_item = Cart(id_user=user.id, id_product=product, quantity=2)  # Utilisez l'ID de l'utilisateur ici
    cart_item.save()

    response = client.get("/cart")
    assert response.status_code == 200

    data = response.get_json()
    assert "cart" in data
    assert len(data["cart"]) > 0
    assert data["cart"][0]["user"] == user.username  # Vérifie le nom de l'utilisateur dans le panier
    assert data["cart"][0]["product"] == product.name  # Vérifie le nom du produit dans le panier
    assert data["cart"][0]["quantity"] == 2
    assert data["cart"][0]["total_price"] == 20.0  # Vérifie le prix total
