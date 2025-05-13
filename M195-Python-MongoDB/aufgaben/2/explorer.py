from pymongo import MongoClient, errors
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017')

def list_databases():
    try:
        databases = client.list_database_names()
        if not databases:
            print("Keine Datenbanken gefunden.")
            return None
        
        print("Verfügbare Datenbanken:")
        for i, db in enumerate(databases, 1):
            print(f"{i}. {db}")

        while True:
            selected = input("\nWähle eine Datenbank (Name oder Nummer, 'q' zum Abbrechen): ").strip()
            if selected.lower() == 'q':
                return None
            if selected.isdigit() and 1 <= int(selected) <= len(databases):
                return databases[int(selected)-1]
            elif selected in databases:
                return selected
            else:
                print("Ungültige Auswahl. Bitte erneut versuchen.")
    except errors.PyMongoError as e:
        print(f"Fehler beim Abrufen der Datenbanken: {e}")
        return None

def list_collections(db_name):
    try:
        db = client[db_name]
        collections = db.list_collection_names()
        if not collections:
            print("Keine Collections gefunden.")
            return None
        
        print(f"Collections in '{db_name}':")
        for i, col in enumerate(collections, 1):
            print(f"{i}. {col}")

        while True:
            selected = input("\nWähle eine Collection (Name oder Nummer, 'q' zum Abbrechen): ").strip()
            if selected.lower() == 'q':
                return None
            if selected.isdigit() and 1 <= int(selected) <= len(collections):
                return collections[int(selected)-1]
            elif selected in collections:
                return selected
            else:
                print("Ungültige Auswahl. Bitte erneut versuchen.")
    except errors.PyMongoError as e:
        print(f"Fehler beim Abrufen der Collections: {e}")
        return None

def list_documents(db_name, collection_name):
    try:
        col = client[db_name][collection_name]
        docs = list(col.find({}, {"_id": 1}))
        if not docs:
            print("Keine Dokumente vorhanden.")
            return None
        
        print(f"Dokument-IDs in Collection '{collection_name}':")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. {doc['_id']}")

        while True:
            selected = input("\nWähle eine Dokument-ID (Nummer oder ObjectId, 'q' zum Abbrechen): ").strip()
            if selected.lower() == 'q':
                return None
            if selected.isdigit() and 1 <= int(selected) <= len(docs):
                return docs[int(selected)-1]['_id']
            try:
                return ObjectId(selected)
            except Exception:
                print("Ungültige ID. Bitte erneut versuchen.")
    except errors.PyMongoError as e:
        print(f"Fehler beim Abrufen der Dokumente: {e}")
        return None

def show_document(db_name, collection_name, doc_id):
    try:
        col = client[db_name][collection_name]
        document = col.find_one({"_id": doc_id})
        print("\n--- Dokument ---")
        print(document if document else "Dokument nicht gefunden.")
    except errors.PyMongoError as e:
        print(f"Fehler beim Abrufen des Dokuments: {e}")


def main():
    while True:
        db = list_databases()
        col = list_collections(db)
        doc = list_documents(db, col)
        show_document(db, col, doc)
        input("\nWeiter mit Enter...")

if __name__ == "__main__":
    main()