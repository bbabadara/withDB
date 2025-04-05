import pandas as pd
from fpdf import FPDF

from database.MongoDB import MongoDB as mdb;

def exporter_etudiants(format="csv"):
   
    collection = mdb.get_collection("etudiants")

    etudiants = list(collection.find({}, {"_id": 0}))  # Récupérer les étudiants (sans l'ID MongoDB)
    
    if not etudiants:
        print("Aucun étudiant trouvé.")
        return
    
    df = pd.DataFrame(etudiants)  # Convertir en DataFrame

    if format == "csv":
        df.to_csv("export_etudiants.csv", index=False)
        print("Exportation en CSV réussie ! ✅")
    elif format == "excel":
        df.to_excel("export_etudiants.xlsx", index=False)
        print("Exportation en Excel réussie ! ✅")
    elif format == "json":
        df.to_json("export_etudiants.json", orient="records", indent=4)
        print("Exportation en JSON réussie ! ✅")
    else:
        print("Format non pris en charge ❌")


def exporter_en_pdf():
    collection = mdb.get_collection("etudiants")
    etudiants = list(collection.find({}, {"_id": 0}))

    if not etudiants:
        print("Aucun étudiant trouvé.")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Liste des étudiants", ln=True, align="C")
    pdf.ln(10)

    for etudiant in etudiants:
        ligne = f"{etudiant['Nom']} {etudiant['Prenom']} - {etudiant['Classe']} - {etudiant['Telephone']}"
        pdf.cell(200, 10, ligne, ln=True)
    
    pdf.output("export_etudiants.pdf")
    print("Exportation en PDF réussie ! ✅")
