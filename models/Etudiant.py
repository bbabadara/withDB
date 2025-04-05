from datetime import datetime
from typing import List, Dict
import re

class Etudiant:
    def __init__(self, nom: str, prenom: str, telephone: str, classe: str):
        self.id = None  # Sera généré par MongoDB
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.classe = classe
        self.notes: Dict[str, float] = {}  # {matiere: note}
        self.date_creation = datetime.now()
        self.date_modification = datetime.now()

    @property
    def moyenne(self) -> float:
        if not self.notes:
            return 0.0
        return sum(self.notes.values()) / len(self.notes)

    def ajouter_note(self, matiere: str, note: float) -> bool:
        if not 0 <= note <= 20:
            return False
        self.notes[matiere] = note
        self.date_modification = datetime.now()
        return True

    def to_dict(self) -> dict:
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "telephone": self.telephone,
            "classe": self.classe,
            "notes": self.notes,
            "moyenne": self.moyenne,
            "date_creation": self.date_creation,
            "date_modification": self.date_modification
        }

    @staticmethod
    def from_dict(data: dict) -> 'Etudiant':
        etudiant = Etudiant(
            nom=data["nom"],
            prenom=data["prenom"],
            telephone=data["telephone"],
            classe=data["classe"]
        )
        etudiant.notes = data.get("notes", {})
        etudiant.date_creation = data.get("date_creation", datetime.now())
        etudiant.date_modification = data.get("date_modification", datetime.now())
        if "_id" in data:
            etudiant.id = str(data["_id"])
        return etudiant

    @staticmethod
    def valider_telephone(telephone: str) -> bool:
        pattern = r"^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$"
        return bool(re.match(pattern, telephone))

    def valid_notes(self):
        return all(0 <= note <= 20 for note in self.notes.values())

    def valider_telephone(self, tel):
        return tel.startswith('77') or tel.startswith('78') or tel.startswith('76') and len(tel) == 9 and tel.isdigit()

