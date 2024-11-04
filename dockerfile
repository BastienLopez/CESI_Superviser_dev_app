# Dockerfile
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le code de l'application
COPY app/ /app

# Exposer le port utilisé par Flask
EXPOSE 8000

# Définir la variable d'environnement FLASK_APP
ENV FLASK_APP=main.py

# Commande pour démarrer l'application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
