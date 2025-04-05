from Utilisateur import Utilisateur
class Admin(Utilisateur):
    def __init__(self, ref):
        super().__init__(ref)
        self.ref = ref