from unittest.mock import patch
import pytest
from flask import jsonify, Blueprint
from app import create_app  # Si vous utilisez une factory app

cart_controller = Blueprint('cart_controller', __name__)

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


# Test pour la route /api/cart/ avec méthode GET
@patch('app.services.cart_service.CartService.get_cart')
def test_get_cart(mock_get_cart, client):
    # Arrange
    user_id = 'user123'
    mock_get_cart.return_value = {"user_id": user_id, "items": [{"product_id": 1, "quantity": 2}]}

    # Act
    response = client.get(f'/api/cart/?user_id={user_id}')

    # Assert
    mock_get_cart.assert_called_once_with(user_id)
    assert response.status_code == 200
    assert b'product_id' in response.data


# Test pour la route /api/cart/add avec méthode POST
@patch('app.services.cart_service.CartService.add_to_cart')
def test_add_to_cart(mock_add_to_cart, client):
    # Arrange
    user_id = 'user123'
    product_id = 1
    quantity = 2
    data = {"user_id": user_id, "product_id": product_id, "quantity": quantity}

    # Act
    response = client.post('/api/cart/add', json=data)

    # Assert
    mock_add_to_cart.assert_called_once_with(user_id, product_id, quantity)
    assert response.status_code == 200
    assert b'Product added to cart' in response.data
