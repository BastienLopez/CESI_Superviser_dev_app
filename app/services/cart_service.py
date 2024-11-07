from app.models import Cart, Product, CartProducts  # Assure-toi d'importer les bons modèles


class CartService:
    def get_cart(self, db, user_id):
        """Récupérer le panier d'un utilisateur"""
        cart = db.session.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            return None
        return cart

    def add_to_cart(self, db, user_id, product_id, quantity):
        """Ajouter un produit au panier"""
        cart = db.session.query(Cart).filter_by(user_id=user_id).first()
        if not cart:
            # Si aucun panier existant, en créer un
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        product = db.session.query(Product).filter_by(id=product_id).first()
        if not product:
            # Si le produit n'existe pas
            return None

        # Vérifier si le produit est déjà dans le panier
        cart_product = db.session.query(CartProducts).filter_by(cart_id=cart.id, product_id=product.id).first()
        if cart_product:
            # Si le produit existe déjà, mettre à jour la quantité
            cart_product.quantity += quantity
        else:
            # Si le produit n'est pas encore dans le panier, l'ajouter
            cart_product = CartProducts(cart_id=cart.id, product_id=product.id, quantity=quantity)
            db.session.add(cart_product)

        db.session.commit()
        return cart_product
