from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

def list_databases():
    databases = client.list_database_names()
    print("Verfügbare Datenbanken:")
    for db in databases:
        print(f" - {db}")
    
    selected = input("\nWähle eine Datenbank: ")
    return selected

def list_collections(db_name):
    db = client[db_name]
    collections = db.list_collection_names()
    print(f"Verfügbare Collections in '{db_name}':")
    for col in collections:
        print(f" - {col}")
    
    selected = input("\nWähle eine Collection: ")
    return selected

def list_documents(db_name, collection_name):
    col = client[db_name][collection_name]
    docs = list(col.find({}, {"_id": 1}))
    print(f"Dokument-IDs in Collection '{collection_name}':")
    for doc in docs:
        print(f" - {doc['_id']}")
    
    selected = input("\nWähle eine Dokument-ID: ")
    return selected

def show_document(db_name, collection_name, doc_id):
    from bson import ObjectId
    col = client[db_name][collection_name]
    document = col.find_one({"_id": ObjectId(doc_id)})
    
    print("\n--- Dokument ---")
    print(document)

def main():
    while True:
        db = list_databases()
        col = list_collections(db)
        doc = list_documents(db, col)
        show_document(db, col, doc)
        input("\nWeiter mit Enter...")

if __name__ == "__main__":
    main()