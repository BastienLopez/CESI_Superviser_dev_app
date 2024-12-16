from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import jwt
import mongoengine as me
import bcrypt


class Users(me.Document):
    username = me.StringField(required=True, unique=True, max_length=80)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True, min_length=6)

    # Méthode pour hacher le mot de passe avant de l'enregistrer
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Méthode pour vérifier le mot de passe
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'

SECRET_KEY = "secret_key"

def get_app(config):

    app = Flask(__name__)

    # Configuration de MongoDB
    app.config['MONGODB_SETTINGS'] = config


    # Initialisation de MongoEngine
    db = MongoEngine(app)




    @app.route("/auth/signup", methods=["POST"])
    def signup():
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400

        # Vérifier si l'utilisateur existe déjà
        if Users.objects(username=username):
            return jsonify({"error": "User already exists"}), 409

        user = Users(username=username, email=email)
        user.set_password(password)  # Hachage du mot de passe
        user.save()

        return jsonify({"message": "User created successfully"}), 201


    @app.route("/auth/login", methods=["POST"])
    def login():
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = Users.objects(username=username).first()
        if user and user.check_password(password):  # Vérification du mot de passe
            token = jwt.encode({"user_id": str(user.id)}, SECRET_KEY, algorithm="HS256")
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401


    @app.route("/auth/validate", methods=["GET"])
    def validate():
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 400

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return jsonify({"status": "valid", "user_id": decoded["user_id"]}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401


    @app.route("/health", methods=["GET"])
    def health_check():
        if db is None:
            return jsonify({"auth_service": False}), 500
        return jsonify({"auth_service": True}), 200

    return app


if __name__ == "__main__":
    get_app({
        'db': 'authdb',
        'host': 'mongo-auth',  # Nom du service MongoDB dans Docker
        'port': 27017,  # Port de MongoDB
        'username': 'root',  # Nom d'utilisateur MongoDB
        'password': 'example',  # Mot de passe MongoDB
        'authentication_source': 'admin'  # Base de données où les infos d'authentification sont stockées
    }).run(host="0.0.0.0", port=8001)
