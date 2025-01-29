# Dockerfile pour product_service
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt depuis le dossier app
COPY ./app/requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Installer pytest pour les tests
RUN pip install pytest
RUN pip install pytest pytest-cov

# Copier le reste du code source
ENV PYTHONPATH=/app

# Exposer le port utilisé par le service
EXPOSE 8002

RUN pwd
RUN ls -R /app

# Commande par défaut pour démarrer le service
CMD ["python", "main.py","pytest", "test_product_service.py", "--cov=app", "--cov-report=xml", "--cov-report=html"]
