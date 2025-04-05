import os
from app.Config import Config
from app.Utils import Utils
from database.MongoDB import MongoDB
from database.redis import RedisCache
from services.EtudiantService import EtudiantService
from services.UtilisateursService import UtilisateursService

class Main:
    def __init__(self):
        self.db = MongoDB()
        self.cache = RedisCache()
        self.etudiant_service = EtudiantService(self.db, self.cache)
        self.utilisateur_service = UtilisateursService(self.db)

    def run(self):
        while True:
            print("\n1. Gérer les étudiants")
            print("2. Gérer les utilisateurs")
            print("3. Quitter")
            choix = input("Choisissez une option: ")
            if choix == "1":
                self.gestion_etudiants()
            elif choix == "2":
                self.gestion_utilisateurs()
            elif choix == "3":
                print("Fermeture de l'application...")
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def gestion_etudiants(self):
        print("\n1. Ajouter un étudiant")
        print("2. Lister les étudiants")
        choix = input("Choisissez une option: ")
        if choix == "1":
            nom = input("Nom: ")
            prenom = input("Prénom: ")
            telephone = input("Téléphone: ")
            classe = input("Classe: ")
            self.etudiant_service.ajouter_etudiant(nom, prenom, telephone, classe)
        elif choix == "2":
            self.etudiant_service.lister_etudiants()
        else:
            print("Option invalide.")

    def gestion_utilisateurs(self):
        print("\n1. Ajouter un utilisateur")
        print("2. Lister les utilisateurs")
        choix = input("Choisissez une option: ")
        if choix == "1":
            nom = input("Nom: ")
            email = input("Email: ")
            password = input("Mot de passe: ")
            self.utilisateur_service.ajouter_utilisateur(nom, email, password)
        elif choix == "2":
            self.utilisateur_service.lister_utilisateurs()
        else:
            print("Option invalide.")

if __name__ == "__main__":
    main_app = Main()
    main_app.run()
