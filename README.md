# Breizhsport - Application Microservices

## Description

Ce projet utilise une architecture microservices pour gérer différentes fonctionnalités liées à Breizhsport. L'application est composée de trois services distincts :

1. **auth_service** : Gestion des utilisateurs (inscription, authentification, validation de jeton).
2. **product_service** : Gestion des produits et du panier.
3. **frontend_service** : Interface utilisateur pour afficher les produits.

L'ensemble du projet est conteneurisé avec Docker, ce qui facilite le déploiement et les tests en local.

## Prérequis

- Docker et Docker Compose doivent être installés sur votre machine.
- Python 3.10 ou plus récent.

## Structure du Projet

```
CESI_Superviser_dev_app/
├── auth_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── test_auth_service.py
├── product_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── test_product_service.py
├── frontend_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── templates/
│   │   └── index.html
│   ├── requirements.txt
│   └── test/test_app.py
└── docker-compose.yml
```

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/CESI_Superviser_dev_app.git
   cd CESI_Superviser_dev_app
   ```

2. Construisez les images Docker et démarrez les conteneurs :

   ```bash
   docker compose up --build
   ```

   Cette commande démarre les services `auth_service`, `product_service`, `frontend_service` ainsi que MongoDB.

## Accéder à l'application

L'interface utilisateur est accessible à l'adresse suivante :

```
http://localhost:8000
```

## Tests

Vous pouvez exécuter des tests pour chaque service individuellement en utilisant les commandes suivantes :

### Exécuter les tests pour `auth_service`

```bash
docker compose run --rm auth_service pytest
```

### Exécuter les tests pour `product_service`

```bash
docker compose run --rm product_service pytest
```

### Exécuter les tests pour `frontend_service`

```bash
docker compose run --rm frontend_service pytest
```

### Explication des tests

- **auth_service** : Vérifie l'inscription et l'authentification des utilisateurs.
- **product_service** : Vérifie la gestion des produits et du panier.
- **frontend_service** : Vérifie que la page d'accueil affiche correctement les produits.

## Nettoyer les conteneurs

Pour arrêter tous les services et nettoyer les conteneurs, utilisez la commande suivante :

```bash
docker compose down
```

## Visualisation des bases de données dans VS Code

Pour visualiser les bases de données `authdb` et `productdb` avec l'extension MongoDB de VS Code, suivez les étapes ci-dessous :

1. Ouvrez l'extension MongoDB dans VS Code.
2. Cliquez sur le bouton `+` pour ajouter une nouvelle connexion.
3. Sélectionnez "Open Form" pour entrer l'URL de connexion manuellement.
4. Utilisez les URL suivantes pour chaque base de données :
   - **authdb** : `mongodb://localhost:27017/authdb`
   - **productdb** : `mongodb://localhost:27018/productdb`
5. Cliquez sur "Connect" pour vous connecter à chaque base de données.


## Dépannage

Si vous rencontrez des problèmes avec Docker, essayez de reconstruire les conteneurs :

```bash
docker compose up --build --force-recreate
```
