# Utiliser une image de base Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tout le contenu de auth_service/app
COPY ./app/ /app

# Copier le fichier requirements.txt
# COPY ./app/requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest
RUN pip install pytest pytest-cov

# Ajouter /app au PYTHONPATH
ENV PYTHONPATH=/app

# Exposer le port sur lequel l'application va fonctionner
EXPOSE 8001

RUN pwd
RUN ls -lisa /app

# Commande par défaut pour démarrer l'application
CMD ["python", "main.py","pytest", "test.py", "--cov=app", "--cov-report=xml", "--cov-report=html"]
