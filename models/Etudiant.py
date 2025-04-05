from Utilisateur import Utilisateur
class Etudiant (Utilisateur):
    def __init__(self, telephone, classe, notes):
        super.__init__()
        self.telephone = telephone
        self.classe = classe
        self.notes = notes
        self.moyenne = self.calculer_moyenne()

    def calculer_moyenne(self):
        if self.notes:
            return sum(self.notes) / len(self.notes)
        return 0

    def valid_notes(self):
        return all(0 <= note <= 20 for note in self.notes)
    
    def valider_telephone(self,tel):
        return tel.startswith('77') or tel.startswith('78') or tel.startswith('76') and len(tel) == 9 and tel.isdigit()
        

