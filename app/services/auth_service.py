from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User

class AuthService:
    def register_user(self, db, username, password):
        """Inscrire un nouvel utilisateur"""
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def authenticate_user(self, db, username, password):
        """Authentifier un utilisateur"""
        user = db.session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        return None
