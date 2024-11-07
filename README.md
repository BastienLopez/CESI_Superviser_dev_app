# Projet Breizhsport

### Autre readme dans /info_projet

Ce projet consiste à développer une application de vente en ligne pour l'entreprise Breizhsport, en utilisant Flask et MongoDB. Il est conçu pour fonctionner avec Docker afin de faciliter le déploiement et l'intégration continue (CI/CD).

## Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Qualité du Code avec SonarLint et SonarCloud](#qualité-du-code-avec-sonarlint-et-sonarcloud)
- [Guide pour les contributions](#guide-pour-les-contributions)

---

### Prérequis

- **Docker** et **Docker Compose** installés sur votre machine.
- Accès à un terminal/commande pour exécuter les commandes de clonage et de lancement du projet.

### Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/BastienLopez/CESI_Superviser_dev_app.git
   cd CESI_Superviser_dev_app
   ```

2. **Construire et lancer le projet avec Docker Compose**

   ```bash
   docker-compose up --build
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
|-- docker/
|   # Ce dossier peut contenir des fichiers Docker supplémentaires, par exemple pour des configurations spécifiques
|
|-- tests/                 # Emplacement prévu pour les tests (fichiers à ajouter)
|
|-- docker-compose.yml     # Configuration Docker Compose pour orchestrer les services (app et db)
|-- Dockerfile             # Fichier Docker pour l'image de l'application Flask
|-- requirements.txt       # Fichier des dépendances Python nécessaires au projet
|-- README.md              # Documentation du projet (ce fichier)
```

---

### Qualité du Code avec SonarLint et SonarCloud

Pour garantir la qualité du code et respecter les bonnes pratiques de développement, nous utilisons **SonarLint** pour l'analyse en temps réel dans l'éditeur, et **SonarCloud** pour l'analyse continue dans les workflows CI/CD.

#### SonarLint

SonarLint est configuré pour analyser le code localement en temps réel dans **Visual Studio Code (VS Code)** :

1. **Installer l'extension SonarLint** dans VS Code (disponible dans le menu des extensions).
2. **Exécuter une analyse manuelle** en ouvrant la palette de commandes (`Ctrl+Shift+P` ou `Cmd+Shift+P` sur macOS) et en choisissant **SonarLint: Run All Analysis**.
3. SonarLint identifiera les problèmes directement dans le panneau "Problems" de VS Code.

#### SonarCloud

SonarCloud est intégré avec GitHub Actions pour une analyse continue de la qualité du code :

1. Les fichiers de configuration pour SonarCloud sont situés dans le dossier `.github/workflows`.
2. Chaque **push** ou **pull request** déclenche une analyse SonarCloud, vérifiant la qualité du code selon les règles configurées dans le projet SonarCloud.
3. Les résultats peuvent être consultés sur le tableau de bord SonarCloud pour le projet.

---

### Guide pour les contributions

Le travail est réparti entre trois personnes. Voici les différentes tâches et où concentrer les modifications :

#### 1. **Développeur 1 : Backend & API**

- Travailler principalement dans `app/main.py` pour ajouter des routes Flask supplémentaires ou des fonctionnalités backend.
- **Tests** : Préparer le fichier de tests (par exemple, `tests/test_app.py`) pour tester les routes et fonctionnalités du backend.
- Pour lancer les tests : `docker compose run test`

#### 2. **Développeur 2 : Frontend (HTML et intégration Flask)**

- Travailler sur les templates HTML dans `app/templates/`. Le fichier `index.html` peut être enrichi avec des éléments supplémentaires ou de nouveaux fichiers HTML peuvent être ajoutés pour d'autres routes.
- **Tests** : Vérifier l'affichage des pages et s'assurer que les liens et formulaires fonctionnent correctement.
- Pour lancer les tests : `docker compose run test`

#### 3. **Développeur 3 : Docker et CI/CD**

- Gérer les configurations Docker dans `Dockerfile` et `docker-compose.yml`. Optimiser les fichiers pour garantir que l’application démarre correctement et que les connexions sont fluides entre les services.
- Ajouter ou configurer les workflows CI/CD dans `.github/workflows/test.yml` pour les tests et `.github/workflows/sonarcloud.yml` pour l’analyse de la qualité du code via SonarCloud.
- **Tests** : S'assurer que les services démarrent sans erreur, et vérifier que le pipeline CI/CD s’exécute correctement sur chaque commit ou pull request.

---
