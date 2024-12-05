import mongoengine as db
import bcrypt

class User(db.Document):
    username = db.StringField(required=True, unique=True, max_length=80)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    # Méthode pour hacher le mot de passe avant de l'enregistrer
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Méthode pour vérifier le mot de passe
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'
