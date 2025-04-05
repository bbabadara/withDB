from typing import List, Optional
from bson import ObjectId
from models.Etudiant import Etudiant
from database.MongoDB import MongoDB
from database.redis import RedisCache
import pandas as pd
from datetime import datetime

class EtudiantService:
    def __init__(self):
        self.db = MongoDB()
        self.cache = RedisCache()
        self.collection = self.db.get_collection("etudiants")

    def ajouter_etudiant(self, etudiant: Etudiant) -> Optional[str]:
        """
        Ajoute un nouvel étudiant
        :param etudiant: Instance d'Etudiant à ajouter
        :return: ID de l'étudiant créé ou None si erreur
        """
        # Vérification du numéro de téléphone unique
        if self.collection.find_one({"telephone": etudiant.telephone}):
            return None

        # Insertion dans MongoDB
        result = self.collection.insert_one(etudiant.to_dict())
        if not result.inserted_id:
            return None

        etudiant_id = str(result.inserted_id)
        # Mise en cache
        self.cache.cache_etudiant(etudiant_id, etudiant.to_dict())
        return etudiant_id

    def obtenir_etudiant(self, etudiant_id: str) -> Optional[Etudiant]:
        """
        Récupère un étudiant par son ID
        :param etudiant_id: ID de l'étudiant
        :return: Instance d'Etudiant ou None
        """
        # Tentative de récupération depuis le cache
        cached_data = self.cache.get_etudiant_cache(etudiant_id)
        if cached_data:
            return Etudiant.from_dict(cached_data)

        # Récupération depuis MongoDB
        data = self.collection.find_one({"_id": ObjectId(etudiant_id)})
        if not data:
            return None

        # Mise en cache et retour
        etudiant = Etudiant.from_dict(data)
        self.cache.cache_etudiant(etudiant_id, etudiant.to_dict())
        return etudiant

    def liste_etudiants(self, tri_par_moyenne: bool = False) -> List[Etudiant]:
        """
        Liste tous les étudiants
        :param tri_par_moyenne: Si True, trie par moyenne décroissante
        :return: Liste d'étudiants
        """
        cursor = self.collection.find()
        etudiants = [Etudiant.from_dict(doc) for doc in cursor]
        
        if tri_par_moyenne:
            etudiants.sort(key=lambda e: e.moyenne, reverse=True)
        
        return etudiants

    def rechercher_etudiants(self, critere: str) -> List[Etudiant]:
        """
        Recherche des étudiants selon différents critères
        :param critere: Texte à rechercher
        :return: Liste d'étudiants correspondants
        """
        query = {
            "$or": [
                {"nom": {"$regex": critere, "$options": "i"}},
                {"prenom": {"$regex": critere, "$options": "i"}},
                {"telephone": {"$regex": critere, "$options": "i"}},
                {"classe": {"$regex": critere, "$options": "i"}}
            ]
        }
        cursor = self.collection.find(query)
        return [Etudiant.from_dict(doc) for doc in cursor]

    def modifier_notes(self, etudiant_id: str, matiere: str, note: float) -> bool:
        """
        Modifie la note d'un étudiant
        :param etudiant_id: ID de l'étudiant
        :param matiere: Nom de la matière
        :param note: Nouvelle note
        :return: True si succès, False sinon
        """
        if not 0 <= note <= 20:
            return False

        etudiant = self.obtenir_etudiant(etudiant_id)
        if not etudiant:
            return False

        # Mise à jour dans MongoDB
        result = self.collection.update_one(
            {"_id": ObjectId(etudiant_id)},
            {
                "$set": {
                    f"notes.{matiere}": note,
                    "date_modification": datetime.now()
                }
            }
        )

        if result.modified_count > 0:
            # Invalider le cache
            self.cache.invalider_cache_etudiant(etudiant_id)
            return True
        return False

    def supprimer_etudiant(self, etudiant_id: str) -> bool:
        """
        Supprime un étudiant
        :param etudiant_id: ID de l'étudiant
        :return: True si succès, False sinon
        """
        result = self.collection.delete_one({"_id": ObjectId(etudiant_id)})
        if result.deleted_count > 0:
            self.cache.invalider_cache_etudiant(etudiant_id)
            return True
        return False

    def exporter_vers_csv(self, chemin_fichier: str):
        """
        Exporte les données des étudiants vers un fichier CSV
        :param chemin_fichier: Chemin du fichier de sortie
        """
        etudiants = self.liste_etudiants()
        data = [e.to_dict() for e in etudiants]
        df = pd.DataFrame(data)
        df.to_csv(chemin_fichier, index=False)

    def importer_depuis_csv(self, chemin_fichier: str) -> int:
        """
        Importe des étudiants depuis un fichier CSV
        :param chemin_fichier: Chemin du fichier source
        :return: Nombre d'étudiants importés
        """
        df = pd.read_csv(chemin_fichier)
        count = 0
        for _, row in df.iterrows():
            etudiant = Etudiant(
                nom=row["nom"],
                prenom=row["prenom"],
                telephone=row["telephone"],
                classe=row["classe"]
            )
            if self.ajouter_etudiant(etudiant):
                count += 1
        return count

    def calculer_moyenne_classe(self, classe: str) -> float:
        """
        Calcule la moyenne générale d'une classe
        :param classe: Nom de la classe
        :return: Moyenne de la classe
        """
        etudiants = self.collection.find({"classe": classe})
        moyennes = [Etudiant.from_dict(e).moyenne for e in etudiants]
        if not moyennes:
            return 0.0
        return sum(moyennes) / len(moyennes)

    def top_10_etudiants(self) -> List[Etudiant]:
        """
        Retourne les 10 meilleurs étudiants
        :return: Liste des 10 meilleurs étudiants
        """
        return self.liste_etudiants(tri_par_moyenne=True)[:10]
