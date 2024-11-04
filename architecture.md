# Architecture et Choix Technologiques du Projet Breizhsport

## 1. Technologies et Frameworks Pertinents

### Langage : Python

Python est un langage polyvalent et bien supporté dans les environnements cloud. Son écosystème riche facilite le développement rapide et son intégration avec de nombreux frameworks et bibliothèques.

### Framework Backend : Flask

Flask a été choisi pour le backend de cette application car :

- Il est léger et minimaliste, parfait pour un projet qui pourrait évoluer vers des microservices.
- Il offre une grande flexibilité dans l'ajout de nouvelles fonctionnalités.
- Il est compatible avec les déploiements Docker et peut facilement être étendu pour des besoins plus complexes.

### Conteneurisation : Docker

Docker est utilisé pour encapsuler l'application et ses dépendances dans un conteneur standardisé. Cela garantit que l'application fonctionne de manière identique dans les environnements de développement, de test, et de production, et assure ainsi une portabilité maximale.

### Orchestration : Docker Compose

Docker Compose est utilisé pour gérer plusieurs services conteneurisés dans un environnement de développement local, facilitant ainsi la gestion et la coordination de l'application (Flask) et de la base de données (PostgreSQL). Il s'agit également d'une base pour évoluer vers des orchestrateurs plus robustes comme Kubernetes.

---

## 2. Justification des Choix d'Architecture et d'Hébergement

### Objectifs d'Architecture Cloud Native

Pour concevoir une application Cloud Native, l'architecture doit répondre aux besoins de scalabilité, résilience, et déploiement flexible. L'utilisation de Docker et de Docker Compose, combinée avec une architecture de conteneurisation, est un pas vers ces objectifs, permettant une transition simple vers le cloud.

### Hébergement Cloud Public

L'application est conçue pour être facilement déployée sur des plateformes de cloud public comme **AWS**, **Azure**, ou **Google Cloud Platform (GCP)**, offrant les avantages suivants :

- **Haute disponibilité et redondance** : Ces plateformes permettent de configurer plusieurs zones de disponibilité pour garantir une disponibilité élevée et une résilience en cas de panne.
- **Scalabilité automatique** : Des solutions de scaling automatique sont proposées par ces fournisseurs pour ajuster les ressources (comme les instances ou les conteneurs) en fonction de la demande.
- **Services managés** : En utilisant des services comme des bases de données managées (par exemple, PostgreSQL managé), nous simplifions la gestion et garantissons une haute disponibilité de la base de données.

### Besoins de Scalabilité et de Résilience

- **Scalabilité** : L’architecture conteneurisée permet une scalabilité horizontale, en ajoutant ou en supprimant des conteneurs en fonction de la charge. L’orchestration avec Docker Compose peut être remplacée par Kubernetes (GKE, EKS, ou AKS selon le cloud choisi) pour une scalabilité avancée et un ajustement automatique des ressources.
- **Résilience** : Le choix de Docker garantit que l’application peut être déployée de manière répétable et fiable. En production, des options comme le stockage de base de données externe (par exemple, PostgreSQL managé) renforcent la résilience en ajoutant des sauvegardes automatiques et une récupération rapide.

---

## Diagramme d’Architecture (exemple)

![Diagramme d'architecture](diagramme_architecture.png)

Ce diagramme illustre l'architecture globale :

- L’application est conteneurisée avec Docker, assurant une isolation et une portabilité.
- Une base de données PostgreSQL est utilisée, connectée via des variables d’environnement pour la sécurité.
- Le tout est orchestré avec Docker Compose pour le développement local, avec une transition facile vers Kubernetes pour une gestion avancée des déploiements en production.

---

## Conclusion

Cette architecture, basée sur Flask et Docker, est adaptée à une application Cloud Native. En utilisant un hébergement cloud public et en tirant parti des services managés et des orchestrateurs, nous répondons aux besoins de scalabilité, résilience, et portabilité nécessaires pour une application moderne.
