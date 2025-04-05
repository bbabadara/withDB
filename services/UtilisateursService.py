from typing import Optional, Dict
import uuid
from datetime import datetime
from models.Utilisateur import Utilisateur, Role
from database.MongoDB import MongoDB
from database.redis import RedisCache

class UtilisateursService:
    def __init__(self):
        self.db = MongoDB()
        self.cache = RedisCache()
        self.collection = self.db.get_collection("utilisateurs")

    def creer_utilisateur(self, email: str, nom: str, prenom: str, mot_de_passe: str, role: Role) -> Optional[str]:
        """
        Crée un nouvel utilisateur
        :return: ID de l'utilisateur créé ou None si erreur
        """
        # Vérification de l'unicité de l'email
        if self.collection.find_one({"email": email}):
            return None

        utilisateur = Utilisateur(email, nom, prenom, role)
        utilisateur.definir_mot_de_passe(mot_de_passe)

        result = self.collection.insert_one(utilisateur.to_dict())
        return str(result.inserted_id) if result.inserted_id else None

    def authentifier(self, email: str, mot_de_passe: str) -> Optional[Dict]:
        """
        Authentifie un utilisateur et crée une session
        :return: Données de session ou None si échec
        """
        user_data = self.collection.find_one({"email": email})
        if not user_data:
            return None

        utilisateur = Utilisateur.from_dict(user_data)
        if not utilisateur.verifier_mot_de_passe(mot_de_passe):
            return None

        # Création de la session
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": str(user_data["_id"]),
            "email": email,
            "role": utilisateur.role.value,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom
        }

        # Stockage de la session dans Redis
        self.cache.set_session(session_id, session_data)

        # Mise à jour de la dernière connexion
        self.collection.update_one(
            {"_id": user_data["_id"]},
            {"$set": {"date_derniere_connexion": datetime.now()}}
        )

        return {"session_id": session_id, **session_data}

    def verifier_session(self, session_id: str) -> Optional[Dict]:
        """
        Vérifie si une session est valide
        :return: Données de session ou None si invalide
        """
        return self.cache.get_session(session_id)

    def deconnecter(self, session_id: str) -> bool:
        """
        Déconnecte un utilisateur en supprimant sa session
        :return: True si succès, False sinon
        """
        return self.cache.delete(f"session:{session_id}")

    def verifier_autorisation(self, session_id: str, roles_requis: list[Role]) -> bool:
        """
        Vérifie si l'utilisateur a les droits requis
        :return: True si autorisé, False sinon
        """
        session = self.verifier_session(session_id)
        if not session:
            return False
        return Role(session["role"]) in roles_requis

    def modifier_mot_de_passe(self, user_id: str, ancien_mot_de_passe: str, nouveau_mot_de_passe: str) -> bool:
        """
        Modifie le mot de passe d'un utilisateur
        :return: True si succès, False sinon
        """
        user_data = self.collection.find_one({"_id": user_id})
        if not user_data:
            return False

        utilisateur = Utilisateur.from_dict(user_data)
        if not utilisateur.verifier_mot_de_passe(ancien_mot_de_passe):
            return False

        utilisateur.definir_mot_de_passe(nouveau_mot_de_passe)
        result = self.collection.update_one(
            {"_id": user_id},
            {"$set": {"mot_de_passe_hash": utilisateur.mot_de_passe_hash}}
        )
        return result.modified_count > 0

    def liste_utilisateurs(self) -> list[Utilisateur]:
        """
        Liste tous les utilisateurs (admin uniquement)
        :return: Liste des utilisateurs
        """
        cursor = self.collection.find()
        return [Utilisateur.from_dict(doc) for doc in cursor]
