from app.extensions import mongo
from app.models.user import User


class AuthService:
    @staticmethod
    def create_user(username, password):
        """Crée un utilisateur et l'insère dans la base de données."""
        user = User(username, password)  # Créer un utilisateur
        users_collection = mongo.db["users"]  # Assurez-vous d'utiliser mongo.db pour accéder à la collection
        # Insérer l'utilisateur dans la collection
        users_collection.insert_one(user.to_dict())
        print("Utilisateur créé avec succès.")

    @staticmethod
    def find_user(username):
        """Trouve un utilisateur par son nom d'utilisateur."""
        users_collection = mongo.db["users"]  # Accès à la collection "users"
        user_data = users_collection.find_one({"username": username})

        if user_data:
            return User.from_dict(user_data)  # Retourne un objet User si trouvé
        return None  # Retourne None si l'utilisateur n'est pas trouvé

    def login(self, username, password):
        """Tentative de connexion avec le nom d'utilisateur et le mot de passe."""
        user = self.find_user(username)
        if user and user.check_password(password):  # Vérifier le mot de passe
            print("Connexion réussie.")
            return user  # Retourne l'utilisateur connecté
        print("Échec de la connexion.")
        return None

    def logout(self):
        """Déconnecte l'utilisateur (pour l'instant, il peut être géré via une session ou un token)."""
        print("Déconnexion réussie.")
        # Code pour gérer la déconnexion (par exemple, supprimer la session ou le token)
        pass
