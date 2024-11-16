from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)  # Hachage du mot de passe

    def to_dict(self):
        """Convertit l'objet User en dictionnaire pour MongoDB."""
        return {
            "username": self.username,
            "password": self.password,
        }

    @staticmethod
    def from_dict(data):
        """Crée un objet User à partir d'un dictionnaire récupéré de MongoDB."""
        return User(username=data["username"], password=data["password"])

    def check_password(self, password):
        """Vérifie que le mot de passe correspond au hachage."""
        return check_password_hash(self.password, password)
