from Utilisateur import Utilisateur
class Professeur (Utilisateur):
    def __init__(self, matiere, grade):
        super().__init__()
        self.matiere = matiere
        self.grade = grade