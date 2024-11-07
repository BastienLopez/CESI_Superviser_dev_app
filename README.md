# Projet Breizhsport

### Autre readme dans /info_projet

Ce projet consiste à développer une application de vente en ligne pour l'entreprise Breizhsport, en utilisant Flask et MongoDB. Il est conçu pour fonctionner avec Docker afin de faciliter le déploiement et l'intégration continue (CI/CD).

## Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Guide pour les contributions](#guide-pour-les-contributions)

---

### Prérequis

- **Docker** et **Docker Compose** installés sur votre machine.
- Accès à un terminal pour exécuter les commandes de clonage et de lancement du projet.

### Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/BastienLopez/CESI_Superviser_dev_app.git
   cd CESI_Superviser_dev_app
   ```

2. **Construire et lancer le projet avec Docker Compose**

   ```bash
   docker-compose up --build
   docker-compose up --build -d
   ```
```bash
docker exec -it <container_id> /bin/bash
docker exec -it a11a087341aa /bin/bash

```


3. **Accéder à l'application**
   Ouvrez votre navigateur et rendez-vous sur [http://localhost:8000](http://localhost:8000).

---

### Structure du projet

Voici la structure des dossiers et fichiers principaux du projet, avec une explication de leur rôle.

```plaintext
/project-root
|-- app/
|   |-- main.py            # Fichier principal Python qui lance l'application Flask
|   |-- templates/
|       |-- index.html     # Page HTML affichée à l'accueil de l'application
|
|-- .github/
|   |-- workflows/
|       |-- test.yml       # Workflow CI/CD pour exécuter les tests avec GitHub Actions
|
|-- tests/                 # Emplacement des tests (fichiers à ajouter)
|
|-- docker-compose.yml     # Configuration Docker Compose pour orchestrer les services (app et MongoDB)
|-- Dockerfile             # Fichier Docker pour l'image de l'application Flask
|-- requirements.txt       # Fichier des dépendances Python nécessaires au projet
|-- README.md              # Documentation du projet (ce fichier)
```

- **`app/main.py`** : Fichier principal de l’application, avec le code Flask pour démarrer le serveur et servir les pages HTML.
- **`app/templates/index.html`** : Page HTML affichée à l’utilisateur. Peut être enrichie pour inclure d’autres sections.
- **`.github/workflows/test.yml`** : Fichier de configuration CI/CD pour GitHub Actions, qui exécute les tests à chaque pull request.
- **`docker-compose.yml`** : Configuration pour lancer les conteneurs Docker (application Flask et base de données MongoDB).
- **`Dockerfile`** : Configuration Docker pour construire l'image de l'application Flask.
- **`requirements.txt`** : Liste des dépendances Python pour le projet.

---

### Guide pour les contributions

Le travail est réparti entre trois personnes. Voici les différentes tâches et où concentrer les modifications :

#### 1. **Développeur 1 : Backend & API**

- Travailler principalement dans `app/main.py` pour ajouter des routes Flask supplémentaires ou des fonctionnalités backend.
- Ajouter les configurations nécessaires pour la base de données MongoDB.
- **Tests** : Préparer le fichier de tests (par exemple, `tests/test_app.py`) pour tester les routes et fonctionnalités du backend.
- Pour lancer les tests : `docker compose run test`

#### 2. **Développeur 2 : Frontend (HTML et intégration Flask)**

- Travailler sur les templates HTML dans `app/templates/`. Le fichier `index.html` peut être enrichi avec des éléments supplémentaires ou de nouveaux fichiers HTML peuvent être ajoutés pour d'autres routes.
- Utiliser `render_template` dans `main.py` pour connecter les nouvelles pages HTML aux routes Flask.
- **Tests** : Vérifier l'affichage des pages et s'assurer que les liens et formulaires fonctionnent correctement.
- Pour lancer les tests : `docker compose run test`

#### 3. **Développeur 3 : Docker et CI/CD**

- Gérer les configurations Docker dans `Dockerfile` et `docker-compose.yml`. Optimiser les fichiers pour garantir que l’application démarre correctement et que les connexions sont fluides entre les services.
- Configurer le workflow CI/CD dans `.github/workflows/test.yml` pour l’intégration continue et les tests automatisés.
- **Tests** : S'assurer que les services démarrent sans erreur, et vérifier que le pipeline CI/CD s’exécute correctement sur chaque commit ou pull request.

---

### Bonnes pratiques pour les contributions

1. **Branching** : Utilisez des branches distinctes pour chaque fonctionnalité ou correctif, par exemple, `feature/backend-routes`, `feature/frontend-html`, `feature/docker-setup`.
2. **Pull Requests** : Créez une pull request pour chaque modification. Évitez les commits directs sur la branche `main` afin de maintenir l'intégrité du code.
3. **Documentation** : Ajoutez des commentaires dans le code pour expliquer les parties complexes ou importantes, surtout dans `main.py` et `docker-compose.yml`.
