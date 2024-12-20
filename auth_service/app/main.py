from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import jwt
import mongoengine as me
import bcrypt


class Users(me.Document):
    """
    Représente un utilisateur dans la base de données MongoDB.

    Attributes:
        username (str): Le nom d'utilisateur de l'utilisateur.
        email (str): L'adresse email de l'utilisateur.
        password (str): Le mot de passe de l'utilisateur.
    """
    username = me.StringField(required=True, unique=True, max_length=80)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True, min_length=6)

    # Méthode pour hacher le mot de passe avant de l'enregistrer
    def set_password(self, password):
        """
        Hache le mot de passe avant de l'enregistrer.

        Args:
            password (str): Le mot de passe en clair à hacher.
        """
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Méthode pour vérifier le mot de passe
    def check_password(self, password):
        """
        Vérifie si le mot de passe correspond à celui stocké.

        Args:
            password (str): Le mot de passe à vérifier.

        Returns:
            bool: True si les mots de passe correspondent, False sinon.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        """
        Représentation de l'utilisateur sous forme de chaîne.

        Returns:
            str: Représentation sous forme de chaîne du nom d'utilisateur.
        """
        return f'<User {self.username}>'

SECRET_KEY = "secret_key"

def get_app(config):
    """
    Crée une application Flask pour le service d'authentification.

    Args:
        config (dict): Configuration de la base de données MongoDB.

    Returns:
        Flask: L'application Flask configurée.
    """

    app = Flask(__name__)

    # Configuration de MongoDB
    app.config['MONGODB_SETTINGS'] = config


    # Initialisation de MongoEngine
    db = MongoEngine(app)




    @app.route("/auth/signup", methods=["POST"])
    def signup():
        """
        Endpoint pour l'inscription d'un utilisateur.

        Attendu : une requête POST avec les données JSON contenant un nom d'utilisateur, un email et un mot de passe.
        Retourne un message de succès ou une erreur.

        Returns:
            Response: La réponse de l'API.
        """
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
        """
        Endpoint pour la connexion d'un utilisateur.

        Attendu : une requête POST avec les données JSON contenant un nom d'utilisateur et un mot de passe.
        Retourne un token JWT si les informations sont correctes, ou une erreur.

        Returns:
            Response: La réponse de l'API.
        """
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
        """
        Endpoint pour valider un token JWT.

        Attendu : une requête GET avec un en-tête Authorization contenant un token JWT.
        Retourne l'état du token (valide ou expiré).

        Returns:
            Response: La réponse de l'API.
        """
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
        """
        Endpoint pour vérifier la santé du service d'authentification.

        Returns:
            Response: La réponse de l'API avec l'état de la base de données.
        """
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
