# Documentation du Système de Gestion des Étudiants

## 1. Introduction

Ce projet est une application Python de gestion des étudiants utilisant une architecture orientée objet et des bases de données NoSQL. L'application permet de gérer les étudiants, les notes, les utilisateurs et offre différentes fonctionnalités selon le rôle de l'utilisateur connecté.

## 2. Architecture du Projet

### 2.1 Structure des répertoires

```
/
├── app/             # Contient l'application principale
├── models/          # Définition des modèles de données
├── services/        # Services métier
├── database/        # Couche d'accès aux données
├── exports/         # Dossier pour l'exportation des données
├── imports/         # Dossier pour l'importation des données
├── test/            # Tests unitaires
└── venv/            # Environnement virtuel Python
```

### 2.2 Technologies utilisées

- **Langage** : Python
- **Bases de données NoSQL** :
  - MongoDB : Stockage principal des données
  - Redis : Cache pour améliorer les performances
- **Dépendances** :
  - pymongo : Interface Python pour MongoDB
  - redis : Interface Python pour Redis
  - bcrypt : Hachage sécurisé des mots de passe
  - pandas : Manipulation et analyse de données pour l'import/export

## 3. Modèles de Données

### 3.1 Etudiant

Le modèle `Etudiant` représente un étudiant dans le système.

**Attributs** :
- `id` : Identifiant unique (généré par MongoDB)
- `nom` : Nom de l'étudiant
- `prenom` : Prénom de l'étudiant
- `telephone` : Numéro de téléphone (doit être unique)
- `classe` : Classe de l'étudiant
- `notes` : Dictionnaire des notes par matière `{matiere: note}`
- `date_creation` : Date de création de l'enregistrement
- `date_modification` : Date de dernière modification

**Méthodes principales** :
- `moyenne()` : Calcule et retourne la moyenne des notes
- `ajouter_note(matiere, note)` : Ajoute ou modifie une note
- `to_dict()` : Convertit l'objet en dictionnaire pour la persistance
- `from_dict(data)` : Crée un objet Etudiant à partir d'un dictionnaire

### 3.2 Utilisateur

Le modèle `Utilisateur` représente un utilisateur du système.

**Attributs** :
- `id` : Identifiant unique
- `email` : Email de l'utilisateur (doit être unique)
- `nom` : Nom de l'utilisateur
- `prenom` : Prénom de l'utilisateur
- `role` : Rôle (Admin, Enseignant, Etudiant)
- `mot_de_passe_hash` : Mot de passe haché
- `date_creation` : Date de création du compte
- `date_derniere_connexion` : Date de dernière connexion
- `actif` : État du compte

**Méthodes principales** :
- `definir_mot_de_passe(mot_de_passe)` : Hache et stocke le mot de passe
- `verifier_mot_de_passe(mot_de_passe)` : Vérifie si le mot de passe est correct
- `to_dict()` : Convertit l'objet en dictionnaire
- `from_dict(data)` : Crée un objet Utilisateur à partir d'un dictionnaire

### 3.3 Role

Énumération qui définit les rôles possibles dans le système :
- `ADMIN` : Administrateur du système
- `ENSEIGNANT` : Enseignant avec accès à la modification des notes
- `ETUDIANT` : Étudiant avec accès limité à ses propres notes

## 4. Services

### 4.1 EtudiantService

Service qui gère toutes les opérations liées aux étudiants.

**Fonctionnalités** :
- Ajouter un étudiant
- Obtenir un étudiant par ID
- Lister tous les étudiants
- Rechercher des étudiants par critères
- Modifier les notes d'un étudiant
- Supprimer un étudiant
- Exporter les données vers CSV
- Importer les données depuis CSV
- Calculer la moyenne d'une classe
- Obtenir le top 10 des étudiants

### 4.2 UtilisateursService

Service qui gère toutes les opérations liées aux utilisateurs.

**Fonctionnalités** :
- Créer un utilisateur
- Authentifier un utilisateur (connexion)
- Vérifier une session
- Déconnecter un utilisateur
- Vérifier les autorisations
- Modifier le mot de passe
- Lister tous les utilisateurs

## 5. Couche d'Accès aux Données

### 5.1 MongoDB

Classe `MongoDB` qui encapsule les opérations avec la base de données MongoDB.

**Méthodes** :
- `get_collection(collection_name)` : Obtient une collection
- `close()` : Ferme la connexion

### 5.2 RedisCache

Classe `RedisCache` qui gère le cache avec Redis pour améliorer les performances.

**Méthodes** :
- `set(key, value, expiration)` : Stocke une valeur dans le cache
- `get(key)` : Récupère une valeur du cache
- `delete(key)` : Supprime une clé du cache
- `set_session(session_id, user_data)` : Stocke une session utilisateur
- `get_session(session_id)` : Récupère une session utilisateur
- `cache_etudiant(etudiant_id, data)` : Met en cache les données d'un étudiant
- `get_etudiant_cache(etudiant_id)` : Récupère les données d'un étudiant du cache
- `invalider_cache_etudiant(etudiant_id)` : Invalide le cache d'un étudiant

## 6. Interface Utilisateur

L'application est une interface en ligne de commande (CLI) qui offre différentes fonctionnalités selon le rôle de l'utilisateur.

### 6.1 Menu Principal

- Se connecter
- Quitter

### 6.2 Menu Administrateur

- Gérer les étudiants
- Gérer les utilisateurs
- Voir les statistiques
- Se déconnecter

### 6.3 Menu Enseignant

- Voir la liste des étudiants
- Modifier les notes
- Voir les statistiques
- Se déconnecter

### 6.4 Menu Étudiant

- Voir mes notes
- Se déconnecter

### 6.5 Gestion des Étudiants (Admin)

- Ajouter un étudiant
- Liste des étudiants
- Rechercher un étudiant
- Modifier les notes
- Supprimer un étudiant
- Exporter les données
- Importer des données

### 6.6 Gestion des Utilisateurs (Admin)

- Créer un utilisateur
- Liste des utilisateurs

### 6.7 Statistiques

- Moyenne par classe
- Top 10 des étudiants

## 7. Sécurité

- Les mots de passe sont hachés avec bcrypt avant stockage
- Système de sessions pour l'authentification
- Vérification des rôles pour l'accès aux fonctionnalités
- Validation des données entrées par l'utilisateur

## 8. Améliorations Récentes

- Correction d'un bug dans la méthode `moyenne()` de la classe `Etudiant` pour éviter une erreur quand `notes` est une liste
- Renforcement de la méthode `from_dict()` pour convertir les notes en dictionnaire si elles sont fournies sous forme de liste
- Ajout de protections supplémentaires contre les erreurs dans les méthodes `moyenne()` et `valid_notes()`

## 9. Installation et Démarrage

1. Cloner le dépôt
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer l'environnement virtuel :
   - Windows : `venv\Scripts\activate`
   - Unix/MacOS : `source venv/bin/activate`
4. Installer les dépendances : `pip install -r requirements.txt`
5. S'assurer que MongoDB et Redis sont installés et en cours d'exécution
6. Lancer l'application : `python app/Main.py`

## 10. Prérequis

- Python 3.8 ou supérieur
- MongoDB
- Redis
- Dépendances Python listées dans requirements.txt 