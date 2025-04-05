from pymongo import MongoClient

class MongoDB:
    def __init__(self, host="localhost", port=27017, db_name="ges-etudiant"):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()

# Exemple  :
# db = MongoDB()
# etudiants_collection = db.get_collection("etudiants")

# db.close()
