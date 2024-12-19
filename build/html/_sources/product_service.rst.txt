Produit et Panier Service
=========================
Ce service est responsable de la gestion des produits et des paniers d'achat. Il permet aux utilisateurs de consulter les produits, d'ajouter des produits au panier et de visualiser leur panier.

Configuration de la Base de Données
-----------------------------------
Le service utilise MongoDB pour stocker les informations relatives aux produits et aux paniers d'achat. La configuration MongoDB est définie comme suit :

- **db** : Base de données MongoDB (productdb)
- **host** : Nom du service MongoDB dans Docker (mongo-product)
- **port** : 27017
- **username** : root
- **password** : example
- **authentication_source** : admin

API Endpoints
-------------
### `/products/<product_id>` [GET]
- **Description** : Permet de récupérer un produit par son ID.
- **Réponse** :
    - **200 OK** : Retourne les détails du produit.
    - **404 Not Found** : Produit non trouvé.
    - **400 Bad Request** : ID de produit invalide.

### `/products/<product_id>/image` [GET]
- **Description** : Permet de récupérer l'image d'un produit sous forme de données binaires.
- **Réponse** :
    - **200 OK** : Retourne l'image en format PNG.
    - **404 Not Found** : Produit non trouvé ou aucune image disponible.

### `/products` [GET]
- **Description** : Permet de récupérer tous les produits disponibles dans le service.
- **Réponse** :
    - **200 OK** : Retourne la liste des produits.

### `/cart` [POST]
- **Description** : Permet d'ajouter un produit au panier d'achat.
- **Paramètres attendus** :
    - **id_product** : ID du produit à ajouter.
    - **quantity** : Quantité du produit à ajouter.
    - **Authorization** : Token JWT valide dans les en-têtes.
- **Réponse** :
    - **201 Created** : Produit ajouté avec succès au panier.
    - **400 Bad Request** : Données invalides ou produit non trouvé.
    - **401 Unauthorized** : Token JWT invalide ou expiré.

### `/cart` [GET]
- **Description** : Permet de récupérer le contenu du panier de l'utilisateur.
- **Réponse** :
    - **200 OK** : Retourne les articles présents dans le panier de l'utilisateur.
    - **400 Bad Request** : Token JWT manquant ou invalide.
    - **401 Unauthorized** : Token JWT expiré ou invalide.

### `/health` [GET]
- **Description** : Permet de vérifier la santé du service de produits.
- **Réponse** :
    - **200 OK** : Service fonctionnel.
    - **500 Internal Server Error** : Problème avec la base de données.

Authentification
----------------
Le service de produits interagit avec un service d'authentification externe pour valider les utilisateurs via des tokens JWT. Les tokens sont envoyés dans les en-têtes des requêtes et validés par le service d'authentification via l'endpoint `/auth/validate`.

### Flux d'authentification
1. L'utilisateur s'authentifie via le service d'authentification, obtenant un token JWT.
2. Ce token est utilisé pour interagir avec les services de produits (ajouter au panier, consulter les produits, etc.).
3. Le service valide le token avec le service d'authentification avant de permettre l'accès aux fonctionnalités.

Gestion des Produits
--------------------
Les produits sont représentés par le modèle `Products`, qui inclut les champs suivants :
- **id** : Identifiant unique du produit.
- **name** : Nom du produit.
- **description** : Description du produit.
- **price** : Prix du produit.
- **image** : Image du produit encodée en Base64.
- **storage_quantity** : Quantité en stock.

Le modèle `Cart` représente un panier d'achat. Il contient les champs suivants :
- **id_user** : ID de l'utilisateur auquel le panier appartient.
- **id_product** : Référence au produit ajouté au panier.
- **quantity** : Quantité de ce produit dans le panier.

Logging
-------
Le service utilise le module `logging` pour enregistrer les événements importants, ce qui permet un suivi facile des actions effectuées.

Dépendances
-----------
Le service utilise les bibliothèques suivantes :
- **Flask** : Framework web léger pour Python.
- **Flask-MongoEngine** : Extension pour Flask qui permet d'intégrer MongoDB.
- **Requests** : Bibliothèque pour effectuer des appels HTTP (utilisée pour valider les tokens avec le service d'authentification).
- **PyJWT** : Bibliothèque pour travailler avec les tokens JWT.
