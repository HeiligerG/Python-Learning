## Verbindung und Grundstruktur

```py
### Imports für MongoDB
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import pprint

# Verbindung zur lokalen MongoDB-Instanz herstellen
client = MongoClient('mongodb://localhost:27017')
# Datenbank "db_restaurants" auswählen
db = client['db_restaurants']
# Collection "restaurants" auswählen
collection = db['restaurants']

# Pretty Printer für bessere Ausgabe
pp = pprint.PrettyPrinter(indent=2)

### Datenbankstruktur überprüfen
sample = collection.find_one()

if sample is None:
    print("Kein Dokument in der Collection 'restaurants' gefunden.")
else:
    print("Beispiel-Restaurant:")
    pp.pprint(sample)

    print("\nVerfügbare Felder:")
    for key in sample.keys():
        print(f"- {key}: {type(sample[key])}")

### Einfache Abfragen
print("\n=== EINFACHE ABFRAGEN ===")

# Anzahl der Dokumente in der Collection
count = collection.count_documents({})
print(f"\nAnzahl der Restaurants: {count}")

# Ein bestimmtes Restaurant nach Namen finden
restaurant_name = "Riviera Caterer"
result = collection.find_one({"name": restaurant_name})
print(f"\nSuche nach '{restaurant_name}':")
pp.pprint(result)

# Alle Restaurants in Brooklyn finden
print("\nAnzahl der Restaurants in Brooklyn:")
brooklyn_count = collection.count_documents({"borough": "Brooklyn"})
print(brooklyn_count)

### Komplexere Abfragen
print("\n=== KOMPLEXERE ABFRAGEN ===")

# Restaurants mit einer bestimmten Küche finden (z.B. Italienisch)
print("\nTop 3 italienische Restaurants:")
italian_restaurants = collection.find({"cuisine": "Italian"}).limit(3)
for restaurant in italian_restaurants:
    print(f"- {restaurant['name']} ({restaurant['borough']})")

# Finde Restaurants mit einer Bewertung von 'A' und einem Score unter 10
print("\nRestaurants mit 'A' Bewertung und Score unter 10:")
query = {
    "grades.grade": "A",
    "grades.score": {"$lt": 10}
}
top_rated = collection.find(query).limit(5)
for restaurant in top_rated:
    print(f"- {restaurant['name']} ({restaurant['borough']})")
    # Zeige die relevanten Bewertungen an
    for grade in restaurant['grades']:
        if grade['grade'] == 'A' and grade['score'] < 10:
            print(f"  Score: {grade['score']} am {grade['date'].strftime('%d.%m.%Y')}")

### Aggregation Pipeline
print("\n=== AGGREGATION PIPELINE ===")

# Anzahl der Restaurants pro Stadtteil
print("\nAnzahl der Restaurants pro Stadtteil:")
borough_pipeline = [
    {"$group": {"_id": "$borough", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
borough_counts = collection.aggregate(borough_pipeline)
for result in borough_counts:
    print(f"- {result['_id']}: {result['count']}")

# Durchschnittliche Bewertung pro Küche
print("\nDurchschnittliche Bewertungspunkte nach Küche (Top 5):")
cuisine_pipeline = [
    {"$unwind": "$grades"},  # Entfaltet das grades-Array
    {"$group": {
        "_id": "$cuisine",
        "avg_score": {"$avg": "$grades.score"},
        "count": {"$sum": 1}
    }},
    {"$match": {"count": {"$gt": 50}}},  # Nur Küchen mit mehr als 50 Bewertungen
    {"$sort": {"avg_score": 1}},  # Aufsteigend sortieren (niedrigere Scores sind besser)
    {"$limit": 5}
]
cuisine_scores = collection.aggregate(cuisine_pipeline)
for result in cuisine_scores:
    print(f"- {result['_id']}: {result['avg_score']:.2f} (aus {result['count']} Bewertungen)")

### Suche mit Geodaten
print("\n=== GEOSPATIALE ABFRAGEN ===")

# Restaurants in der Nähe eines Standorts finden (z.B. Times Square)
times_square = [-73.9855, 40.7580]  # Ungefähre Koordinaten des Times Square
distance = 1000  # Suchradius in Metern

print(f"\nRestaurants im Umkreis von 1km um den Times Square:")
geo_query = {
    "address.coord": {
        "$nearSphere": {
            "$geometry": {
                "type": "Point",
                "coordinates": times_square
            },
            "$maxDistance": distance
        }
    }
}

# Hinweis: Diese Abfrage funktioniert nur, wenn ein Geo-Index auf address.coord existiert
# collection.create_index([("address.coord", "2dsphere")])
try:
    nearby_restaurants = collection.find(geo_query).limit(5)
    for restaurant in nearby_restaurants:
        coords = restaurant['address']['coord']
        print(f"- {restaurant['name']} ({restaurant['cuisine']})")
        print(f"  Adresse: {restaurant['address']['building']} {restaurant['address']['street']}")
except Exception as e:
    print(f"Fehler bei der Geo-Abfrage: {e}")
    print("Hinweis: Möglicherweise fehlt ein Geo-Index. Führen Sie folgendes aus:")
    print("collection.create_index([('address.coord', '2dsphere')])")

### Update-Operationen
print("\n=== UPDATE-BEISPIELE (NICHT AUSGEFÜHRT) ===")

# Beispiel: Ein neues Restaurant hinzufügen
new_restaurant = {
    "name": "Mein Testrestaurant",
    "borough": "Manhattan",
    "cuisine": "German",
    "address": {
        "building": "123",
        "street": "Test Street",
        "zipcode": "10001",
        "coord": [-73.9764, 40.7489]
    },
    "grades": [
        {
            "date": datetime.datetime.now(),
            "grade": "A",
            "score": 8
        }
    ],
    "restaurant_id": "99999999"
}

print("\nBeispiel für das Hinzufügen eines neuen Restaurants:")
pp.pprint(new_restaurant)
print("\n# Um das Restaurant tatsächlich hinzuzufügen, führen Sie aus:")
print("# result = collection.insert_one(new_restaurant)")
print("# print(f'Eingefügt mit ID: {result.inserted_id}')")

# Beispiel: Ein bestehendes Restaurant aktualisieren
print("\nBeispiel für das Aktualisieren eines Restaurants:")
update_query = {"name": "Riviera Caterer"}
update_data = {
    "$push": {
        "grades": {
            "date": datetime.datetime.now(),
            "grade": "A",
            "score": 9
        }
    }
}

print(f"Update-Query: {update_query}")
pp.pprint(update_data)
print("\n# Um das Update tatsächlich durchzuführen, führen Sie aus:")
print("# result = collection.update_one(update_query, update_data)")
print("# print(f'Aktualisierte Dokumente: {result.modified_count}')")
```