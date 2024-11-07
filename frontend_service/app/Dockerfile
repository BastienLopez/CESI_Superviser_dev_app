# Dockerfile pour frontend_service/app
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY . /app

# Exposer le port
EXPOSE 8000

# Lancer l'application
CMD ["python", "main.py"]
