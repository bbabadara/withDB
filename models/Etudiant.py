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
        try:
            if not self.notes or not isinstance(self.notes, dict):
                return 0.0
            return sum(self.notes.values()) / len(self.notes) if len(self.notes) > 0 else 0.0
        except (AttributeError, TypeError):
            # En cas d'erreur inattendue, retourner 0
            return 0.0

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
        # Assurer que notes est toujours un dictionnaire
        notes_data = data.get("notes", {})
        if isinstance(notes_data, list):
            # Si les notes sont sous forme de liste, créer un dictionnaire avec des indices numériques comme clés
            etudiant.notes = {f"Matière {i+1}": note for i, note in enumerate(notes_data) if isinstance(note, (int, float))}
        else:
            etudiant.notes = notes_data
        etudiant.date_creation = data.get("date_creation", datetime.now())
        etudiant.date_modification = data.get("date_modification", datetime.now())
        if "_id" in data:
            etudiant.id = str(data["_id"])
        return etudiant

  

    def valid_notes(self):
        try:
            if not isinstance(self.notes, dict):
                return False
            return all(0 <= note <= 20 for note in self.notes.values())
        except (AttributeError, TypeError):
            return False


    @staticmethod
    def valider_telephone(self, tel):
        return tel.startswith('77') or tel.startswith('78') or tel.startswith('76') and len(tel) == 9 and tel.isdigit()

