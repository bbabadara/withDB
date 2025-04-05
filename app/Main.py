import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.EtudiantService import EtudiantService
from services.UtilisateursService import UtilisateursService
from models.Utilisateur import Role
from models.Etudiant import Etudiant

class Application:
    def __init__(self):
        self.etudiant_service = EtudiantService()
        self.utilisateur_service = UtilisateursService()
        self.session = None

    def afficher_menu_principal(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n=== Gestion des Étudiants ===")
            if not self.session:
                print("1. Se connecter")
                print("2. Quitter")
                choix = input("\nVotre choix : ")
                
                if choix == "1":
                    self.connexion()
                elif choix == "2":
                    print("Au revoir !")
                    sys.exit(0)
            else:
                self.afficher_menu_utilisateur()

    def connexion(self):
        print("\n=== Connexion ===")
        email = input("Email : ")
        mot_de_passe = input("Mot de passe : ")
        
        session = self.utilisateur_service.authentifier(email, mot_de_passe)
        if session:
            self.session = session
            print(f"\nBienvenue {session['prenom']} {session['nom']} !")
            input("Appuyez sur Entrée pour continuer...")
        else:
            print("\nIdentifiants incorrects !")
            input("Appuyez sur Entrée pour continuer...")

    def afficher_menu_utilisateur(self):
        role = Role(self.session["role"])
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n=== Menu {role.value.capitalize()} ===")
            print(f"Connecté en tant que : {self.session['prenom']} {self.session['nom']}")
            
            if role == Role.ADMIN:
                print("\n1. Gérer les étudiants")
                print("2. Gérer les utilisateurs")
                print("3. Voir les statistiques")
                print("4. Se déconnecter")
                
                choix = input("\nVotre choix : ")
                if choix == "1":
                    self.menu_gestion_etudiants()
                elif choix == "2":
                    self.menu_gestion_utilisateurs()
                elif choix == "3":
                    self.menu_statistiques()
                elif choix == "4":
                    self.deconnexion()
                    break
                
            elif role == Role.ENSEIGNANT:
                print("\n1. Voir la liste des étudiants")
                print("2. Modifier les notes")
                print("3. Voir les statistiques")
                print("4. Se déconnecter")
                
                choix = input("\nVotre choix : ")
                if choix == "1":
                    self.afficher_liste_etudiants()
                elif choix == "2":
                    self.modifier_notes()
                elif choix == "3":
                    self.menu_statistiques()
                elif choix == "4":
                    self.deconnexion()
                    break
                
            elif role == Role.ETUDIANT:
                print("\n1. Voir mes notes")
                print("2. Se déconnecter")
                
                choix = input("\nVotre choix : ")
                if choix == "1":
                    self.voir_mes_notes()
                elif choix == "2":
                    self.deconnexion()
                    break

    def menu_gestion_etudiants(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n=== Gestion des Étudiants ===")
            print("1. Ajouter un étudiant")
            print("2. Liste des étudiants")
            print("3. Rechercher un étudiant")
            print("4. Modifier les notes")
            print("5. Supprimer un étudiant")
            print("6. Exporter les données")
            print("7. Importer des données")
            print("8. Retour")
            
            choix = input("\nVotre choix : ")
            if choix == "1":
                self.ajouter_etudiant()
            elif choix == "2":
                self.afficher_liste_etudiants()
            elif choix == "3":
                self.rechercher_etudiant()
            elif choix == "4":
                self.modifier_notes()
            elif choix == "5":
                self.supprimer_etudiant()
            elif choix == "6":
                self.exporter_donnees()
            elif choix == "7":
                self.importer_donnees()
            elif choix == "8":
                break

    def menu_gestion_utilisateurs(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n=== Gestion des Utilisateurs ===")
            print("1. Créer un utilisateur")
            print("2. Liste des utilisateurs")
            print("3. Retour")
            
            choix = input("\nVotre choix : ")
            if choix == "1":
                self.creer_utilisateur()
            elif choix == "2":
                self.liste_utilisateurs()
            elif choix == "3":
                break

    def menu_statistiques(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n=== Statistiques ===")
            print("1. Moyenne par classe")
            print("2. Top 10 des étudiants")
            print("3. Retour")
            
            choix = input("\nVotre choix : ")
            if choix == "1":
                self.moyenne_par_classe()
            elif choix == "2":
                self.afficher_top_10()
            elif choix == "3":
                break

    def ajouter_etudiant(self):
        print("\n=== Ajout d'un Étudiant ===")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        telephone = input("Téléphone : ")
        classe = input("Classe : ")
        
        etudiant = Etudiant(nom, prenom, telephone, classe)
        if self.etudiant_service.ajouter_etudiant(etudiant):
            print("\nÉtudiant ajouté avec succès !")
        else:
            print("\nErreur lors de l'ajout de l'étudiant.")
        input("Appuyez sur Entrée pour continuer...")

    def afficher_liste_etudiants(self):
        print("\n=== Liste des Étudiants ===")
        etudiants = self.etudiant_service.liste_etudiants(tri_par_moyenne=True)
        
        if not etudiants:
            print("Aucun étudiant trouvé.")
        else:
            print(f"{'Nom':<15} {'Prénom':<15} {'Téléphone':<15} {'Classe':<10} {'Moyenne':<8}")
            print("-" * 63)
            for etudiant in etudiants:
                print(f"{etudiant.nom:<15} {etudiant.prenom:<15} {etudiant.telephone:<15} "
                      f"{etudiant.classe:<10} {etudiant.moyenne:>8.2f}")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def rechercher_etudiant(self):
        print("\n=== Recherche d'Étudiant ===")
        critere = input("Entrez le nom, prénom, téléphone ou classe : ")
        
        etudiants = self.etudiant_service.rechercher_etudiants(critere)
        if not etudiants:
            print("Aucun étudiant trouvé.")
        else:
            print(f"\n{'Nom':<15} {'Prénom':<15} {'Téléphone':<15} {'Classe':<10} {'Moyenne':<8}")
            print("-" * 63)
            for etudiant in etudiants:
                print(f"{etudiant.nom:<15} {etudiant.prenom:<15} {etudiant.telephone:<15} "
                      f"{etudiant.classe:<10} {etudiant.moyenne:>8.2f}")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def modifier_notes(self):
        print("\n=== Modification des Notes ===")
        telephone = input("Téléphone de l'étudiant : ")
        
        etudiants = self.etudiant_service.rechercher_etudiants(telephone)
        if not etudiants:
            print("Étudiant non trouvé.")
        else:
            etudiant = etudiants[0]
            matiere = input("Matière : ")
            try:
                note = float(input("Note (0-20) : "))
                if self.etudiant_service.modifier_notes(str(etudiant.id), matiere, note):
                    print("Note modifiée avec succès !")
                else:
                    print("Erreur lors de la modification de la note.")
            except ValueError:
                print("Note invalide.")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def supprimer_etudiant(self):
        print("\n=== Suppression d'Étudiant ===")
        telephone = input("Téléphone de l'étudiant : ")
        
        etudiants = self.etudiant_service.rechercher_etudiants(telephone)
        if not etudiants:
            print("Étudiant non trouvé.")
        else:
            etudiant = etudiants[0]
            confirmation = input(f"Voulez-vous vraiment supprimer l'étudiant {etudiant.prenom} {etudiant.nom} ? (o/n) : ")
            if confirmation.lower() == 'o':
                if self.etudiant_service.supprimer_etudiant(str(etudiant.id)):
                    print("Étudiant supprimé avec succès !")
                else:
                    print("Erreur lors de la suppression.")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def exporter_donnees(self):
        print("\n=== Exportation des Données ===")
        chemin = input("Chemin du fichier CSV : ")
        self.etudiant_service.exporter_vers_csv(chemin)
        print("Données exportées avec succès !")
        input("\nAppuyez sur Entrée pour continuer...")

    def importer_donnees(self):
        print("\n=== Importation des Données ===")
        chemin = input("Chemin du fichier CSV : ")
        nb_importes = self.etudiant_service.importer_depuis_csv(chemin)
        print(f"{nb_importes} étudiants importés avec succès !")
        input("\nAppuyez sur Entrée pour continuer...")

    def creer_utilisateur(self):
        print("\n=== Création d'Utilisateur ===")
        email = input("Email : ")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        mot_de_passe = input("Mot de passe : ")
        
        print("\nRôles disponibles :")
        for role in Role:
            print(f"- {role.value}")
        
        role_str = input("Rôle : ")
        try:
            role = Role(role_str.lower())
            if self.utilisateur_service.creer_utilisateur(email, nom, prenom, mot_de_passe, role):
                print("Utilisateur créé avec succès !")
            else:
                print("Erreur lors de la création de l'utilisateur.")
        except ValueError:
            print("Rôle invalide.")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def liste_utilisateurs(self):
        print("\n=== Liste des Utilisateurs ===")
        utilisateurs = self.utilisateur_service.liste_utilisateurs()
        
        if not utilisateurs:
            print("Aucun utilisateur trouvé.")
        else:
            print(f"{'Email':<30} {'Nom':<15} {'Prénom':<15} {'Rôle':<10}")
            print("-" * 70)
            for utilisateur in utilisateurs:
                print(f"{utilisateur.email:<30} {utilisateur.nom:<15} "
                      f"{utilisateur.prenom:<15} {utilisateur.role.value:<10}")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def moyenne_par_classe(self):
        print("\n=== Moyenne par Classe ===")
        classe = input("Classe : ")
        moyenne = self.etudiant_service.calculer_moyenne_classe(classe)
        print(f"\nMoyenne de la classe {classe} : {moyenne:.2f}")
        input("\nAppuyez sur Entrée pour continuer...")

    def afficher_top_10(self):
        print("\n=== Top 10 des Étudiants ===")
        top_10 = self.etudiant_service.top_10_etudiants()
        
        if not top_10:
            print("Aucun étudiant trouvé.")
        else:
            print(f"{'Rang':<5} {'Nom':<15} {'Prénom':<15} {'Classe':<10} {'Moyenne':<8}")
            print("-" * 53)
            for i, etudiant in enumerate(top_10, 1):
                print(f"{i:<5} {etudiant.nom:<15} {etudiant.prenom:<15} "
                      f"{etudiant.classe:<10} {etudiant.moyenne:>8.2f}")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def voir_mes_notes(self):
        etudiant = self.etudiant_service.obtenir_etudiant(self.session["user_id"])
        if not etudiant:
            print("Erreur lors de la récupération des notes.")
        else:
            print("\n=== Mes Notes ===")
            print(f"Étudiant : {etudiant.prenom} {etudiant.nom}")
            print(f"Classe : {etudiant.classe}")
            print("\nNotes :")
            for matiere, note in etudiant.notes.items():
                print(f"{matiere:<20} : {note:>5.2f}")
            print(f"\nMoyenne générale : {etudiant.moyenne:.2f}")
        
        input("\nAppuyez sur Entrée pour continuer...")

    def deconnexion(self):
        if self.session:
            self.utilisateur_service.deconnecter(self.session["session_id"])
            self.session = None
            print("\nVous êtes déconnecté.")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    app = Application()
    app.afficher_menu_principal()
