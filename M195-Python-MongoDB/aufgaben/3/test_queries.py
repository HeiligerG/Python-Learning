from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['db_restaurants']
collection = db['restaurants']

sample = collection.find_one()

if sample is None:
    print("Kein Dokument in der Collection 'restaurants' gefunden.")
else:
    print("Beispiel-Restaurant:")
    print(sample)

    print("\nVerfügbare Felder:")
    for key in sample.keys():
        print(f"- {key}: {type(sample[key])}")