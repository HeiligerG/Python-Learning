from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['restaurants']
collection = db['restaurants']

sample = collection.find_one()
print("Beispiel-Restaurant:")
print(sample)

print("\nVerfügbare Felder:")
for key in sample.keys():
    print(f"- {key}: {type(sample[key])}")