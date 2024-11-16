from flask import Flask
from app.extensions import mongo  # L'instance de mongo initialisée dans extensions.py

def create_app():
    app = Flask(__name__)

    # Charger la configuration de l'application
    app.config.from_object('app.config.Config')  # Assurez-vous d'avoir un fichier config.py avec la classe Config

    # Initialiser mongo avec la configuration
    mongo.init_app(app)

    # Enregistrement des blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.cart_controller import cart_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')

    return app
