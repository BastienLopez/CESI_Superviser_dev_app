from flask import Flask

def create_app():
    app = Flask(__name__)

    # Charger la configuration de l'app
    app.config.from_object('config.Config')

    # Initialiser les extensions ici (par exemple, db, migrations, etc.)
    from app.extensions import db
    db.init_app(app)

    # Enregistrer les blueprints
    from app.controllers.cart_controller import cart_controller
    app.register_blueprint(cart_controller)

    return app