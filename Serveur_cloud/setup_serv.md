## **1. Pré-requis**

1. **Système d'exploitation** : Ubuntu (déjà installé).
2. **Accès root** ou **sudo** configuré.
3. **Connexion SSH** à la VM depuis votre machine locale.

---

## **2. Installation des outils nécessaires**

### 2.1. Mise à jour du système

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2. Installer Docker et Docker Compose

```bash
# Installer Docker
sudo apt install -y docker.io

# Activer Docker au démarrage
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter l'utilisateur courant au groupe Docker
sudo usermod -aG docker $USER
newgrp docker

# Installer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Vérification
docker --version
docker-compose --version
```

### 2.3. Installer Git

```bash
sudo apt install -y git
```

### 2.4. (Optionnel) Installer Node.js pour des outils supplémentaires

```bash
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## **3. Configuration du projet**

### 3.1. Cloner le projet

```bash
git clone <votre-repo.git> /path/to/your/project
cd /path/to/your/project
```

### 3.2. Configurer les variables d'environnement

Créez un fichier `.env` pour centraliser vos variables d'environnement. Exemple :

```bash
# .env
MONGO_AUTH_URI=mongodb://mongo-auth:27017/authdb
MONGO_PRODUCT_URI=mongodb://mongo-product:27017/productdb
FRONTEND_PORT=8000
AUTH_SERVICE_PORT=8001
PRODUCT_SERVICE_PORT=8002
```

Ajoutez le chemin dans vos services `auth_service`, `product_service`, et `frontend_service` :

```yaml
# Exemple dans docker-compose.yml
auth_service:
  environment:
    - MONGO_URI=${MONGO_AUTH_URI}
```

---

## **4. Configurer MongoDB pour le cloud**

1. Utiliser **MongoDB Atlas** (recommandé) :
   - Créez un compte [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Configurez un cluster.
   - Remplacez vos URI dans `.env` :
     ```bash
     MONGO_AUTH_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/authdb
     MONGO_PRODUCT_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/productdb
     ```
2. **Local MongoDB** :
   - Continuez à utiliser `mongo-auth` et `mongo-product` comme configurés dans Docker.

---

## **5. Configurer le déploiement automatique (CI/CD)**

Utilisez votre fichier **deploiement.yml** pour automatiser le déploiement en production via GitHub Actions :

1. Ajoutez des **secrets** GitHub pour votre serveur :

   - **SERVER_HOST** : L'adresse IP ou le domaine de votre serveur.
   - **SERVER_USER** : L'utilisateur SSH (ex. `ubuntu`).
   - **SERVER_PATH** : Chemin où déployer les fichiers.

2. Modifiez votre pipeline pour utiliser Docker Compose :

```yaml
- name: Déployer le projet avec Docker Compose
  run: |
    ssh $SERVER_USER@$SERVER_HOST "cd $SERVER_PATH && docker-compose pull && docker-compose up -d --build"
```

---

## **6. Configurer HTTPS avec Nginx et un certificat SSL**

### 6.1. Installer Nginx

```bash
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 6.2. Installer Certbot pour SSL

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 6.3. Configurer Nginx

Créez un fichier de configuration pour votre projet :

```bash
sudo nano /etc/nginx/sites-available/projet
```

Contenu :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://localhost:8000; # Remplacez par votre frontend
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Activez et redémarrez Nginx :

```bash
sudo ln -s /etc/nginx/sites-available/projet /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Générez un certificat SSL :

```bash
sudo certbot --nginx -d votre-domaine.com
```

---

## **7. Superviser les logs**

### 7.1. Installer un outil de supervision

- **ELK Stack** (ElasticSearch, Logstash, Kibana) :
  - Suivez [cette documentation](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-elastic-stack.html).

### 7.2. Configurer les logs Docker

Ajoutez dans `docker-compose.yml` :

```yaml
services:
  auth_service:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

---

## **8. Test final**

1. **Lancer votre projet :**
   ```bash
   docker-compose up -d --build
   ```
2. **Vérifiez les services :**
   - MongoDB : Connectez-vous via l'extension MongoDB de VSCode.
   - Frontend : Accédez à `http://<votre-ip>:8000`.
   - Auth Service : Testez à `http://<votre-ip>:8001`.
   - Product Service : Testez à `http://<votre-ip>:8002`.

---

## **9. Maintenance**

1. **Mettre à jour le code :**
   ```bash
   git pull origin main
   docker-compose up -d --build
   ```
2. **Vérifier les logs :**
   ```bash
   docker logs <nom-du-service>
   ```
3. **Redémarrer les services :**
   ```bash
   docker-compose restart
   ```
