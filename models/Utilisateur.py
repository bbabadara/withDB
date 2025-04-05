from datetime import datetime
import bcrypt
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    ENSEIGNANT = "enseignant"
    ETUDIANT = "etudiant"

class Utilisateur:
    def __init__(self, email: str, nom: str, prenom: str, role: Role):
        self.id = None  
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.role = role
        self.mot_de_passe_hash = None
        self.date_creation = datetime.now()
        self.date_derniere_connexion = None
        self.actif = True

    def definir_mot_de_passe(self, mot_de_passe: str):
        sel = bcrypt.gensalt()
        self.mot_de_passe_hash = bcrypt.hashpw(mot_de_passe.encode('utf-8'), sel)

    def verifier_mot_de_passe(self, mot_de_passe: str) -> bool:
        if not self.mot_de_passe_hash:
            return False
        return bcrypt.checkpw(mot_de_passe.encode('utf-8'), self.mot_de_passe_hash)

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "nom": self.nom,
            "prenom": self.prenom,
            "role": self.role.value,
            "mot_de_passe_hash": self.mot_de_passe_hash,
            "date_creation": self.date_creation,
            "date_derniere_connexion": self.date_derniere_connexion,
            "actif": self.actif
        }

    @staticmethod
    def from_dict(data: dict) -> 'Utilisateur':
        utilisateur = Utilisateur(
            email=data["email"],
            nom=data["nom"],
            prenom=data["prenom"],
            role=Role(data["role"])
        )
        utilisateur.mot_de_passe_hash = data.get("mot_de_passe_hash")
        utilisateur.date_creation = data.get("date_creation", datetime.now())
        utilisateur.date_derniere_connexion = data.get("date_derniere_connexion")
        utilisateur.actif = data.get("actif", True)
        if "_id" in data:
            utilisateur.id = str(data["_id"])
        return utilisateur
        