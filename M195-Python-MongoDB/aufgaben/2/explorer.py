from pymongo import MongoClient

def list_databases():
    client = MongoClient('mongodb://localhost:27017')
    databases = client.list_database_names()
    
    print("Databases")
    for db in databases:
        print(f" - {db}")
    
    print("\nSelect Database: ", end="")
    selected = input()
    return selected

db_name = list_databases()
print(f"Gewählt: {db_name}")