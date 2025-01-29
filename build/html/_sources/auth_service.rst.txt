Authentification Service
========================

Le service d'authentification permet aux utilisateurs de s'inscrire, de se connecter et de valider leur token JWT.

Le service utilise **MongoDB** pour stocker les informations des utilisateurs et utilise **JWT** (JSON Web Tokens) pour l'authentification et la validation des utilisateurs.

**Endpoints :**
----------------

1. **POST /auth/signup**
   - Description : Inscription d'un utilisateur dans le système.
   - Paramètres attendus (dans le corps de la requête) :
     - `username` (str) : Le nom d'utilisateur.
     - `email` (str) : L'adresse email.
     - `password` (str) : Le mot de passe de l'utilisateur.
   - Réponse en cas de succès :
     - `201 Created` avec un message `"User created successfully"`.
   - Réponse en cas d'erreur :
     - `400 Bad Request` si des informations obligatoires manquent.
     - `409 Conflict` si l'utilisateur existe déjà.

2. **POST /auth/login**
   - Description : Connexion d'un utilisateur existant et génération d'un token JWT.
   - Paramètres attendus (dans le corps de la requête) :
     - `username` (str) : Le nom d'utilisateur.
     - `password` (str) : Le mot de passe de l'utilisateur.
   - Réponse en cas de succès :
     - `200 OK` avec le token JWT dans le corps de la réponse.
   - Réponse en cas d'erreur :
     - `400 Bad Request` si les paramètres requis sont manquants.
     - `401 Unauthorized` si les informations d'identification sont invalides.

3. **GET /auth/validate**
   - Description : Validation d'un token JWT.
   - Paramètres attendus (dans les en-têtes de la requête) :
     - `Authorization` : Le token JWT à valider.
   - Réponse en cas de succès :
     - `200 OK` avec un message `"valid"` et l'ID utilisateur.
   - Réponse en cas d'erreur :
     - `400 Bad Request` si le token est manquant.
     - `401 Unauthorized` si le token est expiré ou invalide.

4. **GET /health**
   - Description : Vérification de la santé du service d'authentification.
   - Réponse en cas de succès :
     - `200 OK` avec un état `"auth_service": True` si le service est opérationnel.
   - Réponse en cas d'erreur :
     - `500 Internal Server Error` si le service de base de données est inaccessible.

**Modèle d'utilisateur :**
---------------------------

La base de données utilise un modèle MongoDB pour stocker les informations des utilisateurs. Le modèle `Users` contient les champs suivants :
- `username` (str) : Le nom d'utilisateur (unique).
- `email` (str) : L'adresse email de l'utilisateur (unique).
- `password` (str) : Le mot de passe de l'utilisateur (haché avant l'enregistrement).

**Sécurité :**
--------------
- Le mot de passe de l'utilisateur est haché à l'aide de **bcrypt** avant d'être stocké dans la base de données.
- Le service utilise **JWT** pour gérer l'authentification et l'autorisation des utilisateurs. Les tokens sont signés avec une clé secrète et ont une durée de vie limitée.

**Exemple d'utilisation :**
---------------------------

1. **Inscription d'un utilisateur** :
   - Requête POST vers `/auth/signup` avec les données suivantes :
     ```json
     {
       "username": "john_doe",
       "email": "john@example.com",
       "password": "password123"
     }
     ```
   - Réponse :
     ```json
     {
       "message": "User created successfully"
     }
     ```

2. **Connexion d'un utilisateur** :
   - Requête POST vers `/auth/login` avec les données suivantes :
     ```json
     {
       "username": "john_doe",
       "password": "password123"
     }
     ```
   - Réponse :
     ```json
     {
       "token": "jwt_token_here"
     }
     ```

3. **Validation d'un token JWT** :
   - Requête GET vers `/auth/validate` avec l'en-tête `Authorization: jwt_token_here`.
   - Réponse :
     ```json
     {
       "status": "valid",
       "user_id": "user_id_here"
     }
     ```

**Configuration de la base de données :**
-----------------------------------------

Le service d'authentification utilise MongoDB pour stocker les informations des utilisateurs. La configuration MongoDB pour l'application est la suivante :

- Base de données : `authdb`
- Hôte MongoDB : `mongo-auth`
- Port MongoDB : `27017`
- Nom d'utilisateur MongoDB : `root`
- Mot de passe MongoDB : `example`
- Base d'authentification : `admin`

