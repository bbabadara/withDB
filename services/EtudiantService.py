import pymongo
import redis
from models.Etudiant import Etudiant 

class EtudiantsService:
    def __init__(self, mongo_db, redis_db):
        self.mongo_client = pymongo.MongoClient(mongo_db)
        self.redis_client = redis.StrictRedis(host=redis_db, port=6379, db=0)
        self.db = self.mongo_client['etablissement']
        self.collection_etudiants = self.db['etudiants']

    def ajouter_etudiant(self, etudiant: Etudiant):
        if not etudiant.valid_notes():
            print("Erreur: Les notes doivent être entre 0 et 20.")
            return
        # Vérification du téléphone unique dans MongoDB
        if self.collection_etudiants.find_one({"telephone": etudiant.telephone}):
            print("Erreur: Le téléphone est déjà utilisé.")
            return
        # Ajouter l'étudiant dans MongoDB
        self.collection_etudiants.insert_one(vars(etudiant))
        # Mise en cache dans Redis
        self.redis_client.set(etudiant.telephone, vars(etudiant))

    def rechercher_etudiant(self, telephone):
        etudiant_cache = self.redis_client.get(telephone)
        if etudiant_cache:
            return eval(etudiant_cache)  # Retourner les données en cache
        etudiant_db = self.collection_etudiants.find_one({"telephone": telephone})
        return etudiant_db if etudiant_db else None

    def supprimer_etudiant(self, telephone):
        self.collection_etudiants.delete_one({"telephone": telephone})
        self.redis_client.delete(telephone)

    def modifier_notes(self, telephone, nouvelles_notes):
        self.collection_etudiants.update_one(
            {"telephone": telephone},
            {"$set": {"notes": nouvelles_notes, "moyenne": sum(nouvelles_notes) / len(nouvelles_notes)}}
        )
        # Mise à jour du cache Redis
        self.redis_client.set(telephone, nouvelles_notes)
