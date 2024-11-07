class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        """Convertit l'objet User en dictionnaire pour MongoDB."""
        return {
            "username": self.username,
            "password": self.password,
        }