# app/models/cart.py
from app.main import db


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    products = db.relationship('Product', secondary='cart_products', back_populates='carts')

    def __init__(self, user_id):
        self.user_id = user_id


class CartProducts(db.Model):
    __tablename__ = 'cart_products'

    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
