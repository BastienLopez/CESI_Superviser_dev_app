# API Documentation

## Table of Contents
1. [Health Check](#health-check-get)
2. [Products](#products)
    - [Product Details](#product-details-get)
    - [Product Image](#product-image-get)
    - [List All Products](#list-all-products-get)
3. [Authentication](#authentication)
    - [Sign Up](#sign-up-post)
    - [Log In](#log-in-post)
    - [Validate Token](#validate-token-get)
4. [Cart](#cart)
    - [Add Product to Cart](#add-product-to-cart-post)
    - [View Cart](#view-cart-get)

---

## Health Check [GET]

**Endpoint**  
```bash
http://localhost:8001/health
```

**Response Example**  
```json
{
    "auth_service": true
}
```

---

## Products

### Product Details [GET]

**Endpoint**  
```bash
http://localhost:8002/products/{id}
```

- `{id}`: Product ID (e.g., `"675f0aeb846059bec45617dc"`)

**Response Example**  
```json
{
    "product": {
        "description": "Comfortable running sneakers for everyday use.",
        "id": "675f0aeb846059bec45617dc",
        "image": "/products/675f0aeb846059bec45617dc/image",
        "name": "Running Sneakers",
        "price": 79.99,
        "storage_quantity": 120
    }
}
```

---

### Product Image [GET]

**Endpoint**  
```bash
http://localhost:8002/products/{id}/image
```

- `{id}`: Product ID (e.g., `"675c5d38e4de3534ea4800dc"`)

**Response**  
Directly displays the product image.

---

### List All Products [GET]

**Endpoint**  
```bash
http://localhost:8002/products
```

**Response Example**  
```json
{
    "products": [
        {
            "description": "Comfortable running sneakers for everyday use.",
            "id": "675f0aeb846059bec45617dc",
            "image": "/products/675f0aeb846059bec45617dc/image",
            "name": "Running Sneakers",
            "price": 79.99,
            "storage_quantity": 120
        },
        {
            "description": "Comfortable Jogging for everyday use.",
            "id": "675f0aeb846059bec45617dd",
            "image": "/products/675f0aeb846059bec45617dd/image",
            "name": "Jogging",
            "price": 79.99,
            "storage_quantity": 120
        }
    ]
}
```

---

## Authentication

### Sign Up [POST]

**Endpoint**  
```bash
http://localhost:8001/auth/signup
```

**Body**  
```json
{
    "username": "user",
    "email": "user@example.com",
    "password": "password"
}
```

**Response Example**  
```json
{
    "message": "User created successfully"
}
```

---

### Log In [POST]

**Endpoint**  
```bash
http://localhost:8001/auth/login
```

**Body**  
```json
{
    "username": "user",
    "password": "password"
}
```

**Response Example**  
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjc1YzVkNjY1NzgzYWEwODZhYTA5MTg5In0.eCXmxQ5S2cv0h2Of1l6x5MBWZwxwZ41MaHAxsGonJZI"
}
```

---

### Validate Token [GET]

**Endpoint**  
```bash
http://localhost:8001/auth/validate
```

**Headers**  
- `Authorization: Bearer {token}`

**Response Example**  
```json
{
    "status": "valid",
    "user_id": "675c5d665783aa086aa09189"
}
```

---

## Cart

### Add Product to Cart [POST]

**Endpoint**  
```bash
http://localhost:8002/cart
```

**Headers**  
- `Authorization: Bearer {token}`

**Body**  
```json
{
    "id_product": "675f0aeb846059bec45617dc",
    "quantity": 1
}
```

**Response Example**  
```json
{
    "message": "Product added to cart"
}
```

---

### View Cart [GET]

**Endpoint**  
```bash
http://localhost:8002/cart
```

**Headers**  
- `Authorization: Bearer {token}`

**Response Example**  
```json
{
    "cart": [
        {
            "product": {
                "description": "Comfortable running sneakers for everyday use.",
                "id": "675f0aeb846059bec45617dc",
                "image": "/products/675f0aeb846059bec45617dc/image",
                "name": "Running Sneakers",
                "price": 79.99
            },
            "quantity": 2,
            "total_price": 159.98
        }
    ]
}