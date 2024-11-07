# app/tests/test_controllers.py
import json
from unittest.mock import patch
from flask import Flask
from app.services.auth_service import AuthService
from app.controllers.auth_controller import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@patch('app.services.auth_service.AuthService')
def test_login_success(mock_auth_service):
    mock_auth_service.return_value.login.return_value = {'username': 'testuser'}
    # Reste du test
    pass

@patch('app.services.auth_service.AuthService')
def test_login_failure(mock_auth_service):
    mock_auth_service.return_value.login.return_value = None
    # Reste du test
    pass

@patch('app.services.auth_service.AuthService')
def test_logout(mock_auth_service):
    mock_auth_service.return_value.logout.return_value = None
    # Test de la déconnexion
    pass

# ---------------------------CartController---------------------------------------------

@patch('app.services.cart_service.CartService.get_cart')
def test_get_cart(mock_get_cart):
    # Arrange
    mock_get_cart.return_value = {
        'items': [
            {'product_id': 1, 'quantity': 2},
            {'product_id': 2, 'quantity': 1}
        ]
    }

    # Act
    response = app.test_client().get('/api/cart/')

    # Assert
    mock_get_cart.assert_called_once()
    assert response.status_code == 200
    assert json.loads(response.data) == {
        'items': [
            {'product_id': 1, 'quantity': 2},
            {'product_id': 2, 'quantity': 1}
        ]
    }

@patch('app.services.cart_service.CartService.add_to_cart')
def test_add_to_cart(mock_add_to_cart):
    # Arrange
    data = {'product_id': 3, 'quantity': 1}

    # Act
    response = app.test_client().post('/api/cart/add', data=json.dumps(data), content_type='application/json')

    # Assert
    mock_add_to_cart.assert_called_once_with(3, 1)
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Product added to cart'}