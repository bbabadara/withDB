import bcrypt
from database.MongoDB import MongoDB

class UtilisateursService:
    def __init__(self):
        self.db = pymongo.MongoClient('mongodb://localhost:27017/')['etablissement']['utilisateurs']
        self.db = MongoDB.get_collection('utilisateurs')

    def ajouter_utilisateur(self, username, mot_de_passe, role):
        if self.db.find_one({"username": username}):
            print("Utilisateur déjà existant.")
            return
        hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        self.db.insert_one({"username": username, "mot_de_passe": hashed_password, "role": role})

    def authentifier(self, username, mot_de_passe):
        utilisateur = self.db.find_one({"username": username})
        if utilisateur and bcrypt.checkpw(mot_de_passe.encode('utf-8'), utilisateur["mot_de_passe"]):
            return utilisateur  
        return None
