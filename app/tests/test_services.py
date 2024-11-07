# app/tests/test_auth_service.py
from unittest.mock import patch, MagicMock

from app.services import CartService
from app.services.auth_service import AuthService
from app.models.user import User

@patch('app.services.auth_service.db')
def test_create_user(mock_db):
    # Arrange
    username = "testuser"
    password = "testpass"

    # Act
    AuthService.create_user(username, password)

    # Assert
    mock_db["users"].insert_one.assert_called_with({
        "username": username,
        "password": password
    })

    # Vérifier que l'utilisateur a bien été créé
    user = User(username, password)
    assert user.username == username
    assert user.password == password


@patch('app.services.auth_service.db')
def test_find_user(mock_db):
    # Arrange
    username = "testuser"
    mock_db["users"].find_one.return_value = {
        "username": username,
        "password": "testpass"
    }

    # Act
    user_data = AuthService.find_user(username)

    # Assert
    mock_db["users"].find_one.assert_called_with({"username": username})
    assert user_data["username"] == username
    assert user_data["password"] == "testpass"

# Tests pour CartService
@patch('app.services.cart_service.db')
def test_create_cart(mock_db):
    # Arrange
    mock_carts_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_carts_collection
    user_id = "user123"
    products = [{"product_id": 1, "quantity": 2}]

    # Act
    CartService.create_cart(user_id, products)

    # Assert
    mock_carts_collection.insert_one.assert_called_once()
    args, kwargs = mock_carts_collection.insert_one.call_args
    assert args[0]["user_id"] == user_id
    assert args[0]["products"] == products

@patch('app.services.cart_service.db')
def test_get_cart(mock_db):
    # Arrange
    mock_carts_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_carts_collection
    user_id = "user123"
    expected_cart = {"user_id": user_id, "products": [{"product_id": 1, "quantity": 2}]}
    mock_carts_collection.find_one.return_value = expected_cart

    # Act
    cart = CartService.get_cart(user_id)

    # Assert
    mock_carts_collection.find_one.assert_called_once_with({"user_id": user_id})
    assert cart == expected_cart

@patch('app.services.cart_service.db')
def test_add_to_cart_new_cart(mock_db):
    # Arrange
    mock_carts_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_carts_collection
    user_id = "user123"
    product_id = 1
    quantity = 2
    mock_carts_collection.find_one.return_value = None

    # Act
    CartService.add_to_cart(user_id, product_id, quantity)

    # Assert
    mock_carts_collection.insert_one.assert_called_once()
    args, kwargs = mock_carts_collection.insert_one.call_args
    assert args[0]["user_id"] == user_id
    assert args[0]["products"] == [{"product_id": product_id, "quantity": quantity}]

@patch('app.services.cart_service.db')
def test_add_to_cart_existing_product(mock_db):
    # Arrange
    mock_carts_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_carts_collection
    user_id = "user123"
    product_id = 1
    quantity = 3
    existing_cart = {
        "user_id": user_id,
        "products": [{"product_id": product_id, "quantity": 2}]
    }
    mock_carts_collection.find_one.return_value = existing_cart

    # Act
    CartService.add_to_cart(user_id, product_id, quantity)

    # Assert
    updated_products = [{"product_id": product_id, "quantity": 5}]
    mock_carts_collection.update_one.assert_called_once_with(
        {"user_id": user_id},
        {"$set": {"products": updated_products}}
    )

@patch('app.services.cart_service.db')
def test_add_to_cart_new_product(mock_db):
    # Arrange
    mock_carts_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_carts_collection
    user_id = "user123"
    product_id = 2
    quantity = 1
    existing_cart = {
        "user_id": user_id,
        "products": [{"product_id": 1, "quantity": 2}]
    }
    mock_carts_collection.find_one.return_value = existing_cart

    # Act
    CartService.add_to_cart(user_id, product_id, quantity)

    # Assert
    updated_products = [
        {"product_id": 1, "quantity": 2},
        {"product_id": product_id, "quantity": quantity}
    ]
    mock_carts_collection.update_one.assert_called_once_with(
        {"user_id": user_id},
        {"$set": {"products": updated_products}}
    )
