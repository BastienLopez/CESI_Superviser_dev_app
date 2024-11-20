### Documentation : Mise en place d’un serveur cloud avec Ubuntu et MongoDB

Cette documentation décrit les étapes nécessaires pour configurer une VM Ubuntu comme serveur pour votre projet, y compris MongoDB et la connectivité réseau.

---

## **1. Pré-requis**

1. **Accès à la VM** :
   - Ayez les identifiants pour vous connecter à votre VM via SSH.
   - Exemple :
     ```bash
     ssh user@<IP_VM>
     ```
2. **VM Ubuntu installée** :
   - Version Ubuntu Server (20.04 ou plus récent recommandé).
3. **Un utilisateur avec des droits sudo**.

---

## **2. Mise à jour et préparation de la VM**

### a. Mettre à jour le système

```bash
sudo apt update && sudo apt upgrade -y
```

### b. Installer les outils essentiels

```bash
sudo apt install -y curl wget git ufw
```

---

## **3. Installation de Docker et Docker Compose**

### a. Installer Docker

1. Supprimez les versions Docker précédentes (si existantes) :

   ```bash
   sudo apt remove -y docker docker-engine docker.io containerd runc
   ```

2. Installez Docker depuis le dépôt officiel :

   ```bash
   sudo apt update
   sudo apt install -y ca-certificates curl gnupg
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io
   ```

3. Vérifiez l’installation :
   ```bash
   docker --version
   ```

### b. Installer Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### c. Autoriser l’utilisateur courant à utiliser Docker

```bash
sudo usermod -aG docker $USER
```

**Note :** Déconnectez-vous puis reconnectez-vous pour appliquer les changements.

---

## **4. Installation et configuration de MongoDB**

### a. Installer MongoDB

1. Importer la clé GPG et le dépôt MongoDB :

   ```bash
   curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg
   echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   sudo apt update
   ```

2. Installer MongoDB :

   ```bash
   sudo apt install -y mongodb-org
   ```

3. Démarrer MongoDB et l’activer au démarrage :

   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```

4. Vérifiez que MongoDB fonctionne :
   ```bash
   sudo systemctl status mongod
   ```

### b. Configurer MongoDB pour les connexions externes

1. Éditez le fichier de configuration de MongoDB :

   ```bash
   sudo nano /etc/mongod.conf
   ```

2. Modifiez `bindIp` pour accepter les connexions externes :

   ```yaml
   net:
     bindIp: 0.0.0.0
     port: 27017
   ```

3. Redémarrez MongoDB :
   ```bash
   sudo systemctl restart mongod
   ```

### c. Sécuriser MongoDB

1. Activer l’authentification MongoDB :

   - Éditez `/etc/mongod.conf` et ajoutez sous `security` :

     ```yaml
     security:
       authorization: enabled
     ```

   - Redémarrez MongoDB :
     ```bash
     sudo systemctl restart mongod
     ```

2. Ajouter un utilisateur administrateur dans MongoDB :

   ```bash
   mongo
   use admin
   db.createUser({
     user: "admin",
     pwd: "secure_password",
     roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
   })
   exit
   ```

3. Connectez-vous avec l’utilisateur :
   ```bash
   mongo -u admin -p secure_password --authenticationDatabase admin
   ```

---

## **5. Configurer le pare-feu**

1. Activer le pare-feu UFW et autoriser SSH :

   ```bash
   sudo ufw allow OpenSSH
   sudo ufw enable
   ```

2. Autoriser les ports nécessaires :

   ```bash
   sudo ufw allow 27017
   sudo ufw allow 8001
   sudo ufw allow 8002
   sudo ufw allow 8000
   ```

3. Vérifiez le statut :
   ```bash
   sudo ufw status
   ```

---

## **6. Déployer votre projet avec Docker Compose**

1. Clonez votre dépôt dans la VM :

   ```bash
   git clone <url_du_repo>
   cd <nom_du_repo>
   ```

2. Modifiez les `MONGO_URI` dans `docker-compose.yml` :

   - Auth service :
     ```yaml
     MONGO_URI: mongodb://admin:secure_password@<IP_VM>:27017/authdb?authSource=admin
     ```
   - Product service :
     ```yaml
     MONGO_URI: mongodb://admin:secure_password@<IP_VM>:27017/productdb?authSource=admin
     ```

3. Lancez Docker Compose :
   ```bash
   docker compose up --build
   ```

---

## **7. Tester le projet**

1. Ouvrez vos services dans un navigateur :

   - **Frontend** : `http://<IP_VM>:8000`
   - **Auth Service** : `http://<IP_VM>:8001/health`
   - **Product Service** : `http://<IP_VM>:8002/health`

2. Vérifiez les logs Docker pour détecter d’éventuelles erreurs :

   ```bash
   docker compose logs
   ```

3. Exécutez vos tests unitaires pour valider la configuration :
   ```bash
   docker compose run --rm auth_service pytest
   docker compose run --rm product_service pytest
   docker compose run --rm frontend_service pytest
   ```

---

## **8. Accès MongoDB graphique avec VSCode**

1. Installez l’extension **MongoDB** pour VSCode.
2. Ajoutez une connexion :
   - Auth Service : `mongodb://<IP_VM>:27017/authdb`
   - Product Service : `mongodb://<IP_VM>:27017/productdb`

---
