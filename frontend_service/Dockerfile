# Dockerfile pour auth_service
FROM python:3.10-slim

WORKDIR /app

# Copier le fichier requirements.txt depuis le dossier app
COPY app/requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Installer pytest pour les tests
RUN pip install --no-cache-dir pytest
RUN pip install pytest pytest-cov

# Copier le reste du code source
COPY app/ .

# Exposer le port utilisé par le service
EXPOSE 8001

# Commande par défaut pour démarrer le service
CMD ["python", "main.py", "pytest", "test/test_app.py", "--cov=app", "--cov-report=xml", "--cov-report=html"]
