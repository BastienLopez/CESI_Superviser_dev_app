from .main import get_app
from product_service.app.main import SECRET_KEY


app = get_app({
    'db': 'testdbproduct',
    'host': 'localhost',  # Nom du service MongoDB dans Docker
    'port': 27017,  # Port de MongoDB
    'username': 'root',  # Nom d'utilisateur MongoDB
    'password': 'example',  # Mot de passe MongoDB
    'authentication_source': 'admin'  # Base de données où les infos d'authentification sont stockées
})

app.testing = True

# Ajout de l'URL du service d'authentification pour les tests
auth_service_url = "http://test_auth_service:8001"
app.config['AUTH_SERVICE_URL'] = auth_service_url

