# Dockerfile pour auth_service

# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer pytest pour les tests
RUN pip install --no-cache-dir pytest

# Copier le reste du code source
COPY . .

# Exposer le port utilisé par le service
EXPOSE 8001

# Commande par défaut pour démarrer le service
CMD ["python", "main.py"]
