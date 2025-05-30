# Dokumentation der test_queries um alles vollumfänglich zu verstehen

## Connection und erstes Sample

### Code

```py
from pymongo import MongoClient

# Establish a connection to the MongoDB server running on localhost at port 27017.
client = MongoClient('mongodb://localhost:27017')

# Access the database named 'db_restaurants'. If it doesn't exist, MongoDB will create it
# upon the first data insertion.
db = client['db_restaurants']

# Access the collection named 'restaurants' within the 'db_restaurants' database.
# If the collection doesn't exist, MongoDB will create it upon the first data insertion.
collection = db['restaurants']

# Retrieve a single document from the 'restaurants' collection.
# If the collection is empty, 'find_one()' will return None.
sample = collection.find_one()

# Check if a document was found.
if sample is None:
    # If no document is found, print an informative message.
    print("Kein Dokument in der Collection 'restaurants' gefunden.")
else:
    # If a document is found, print a header and then the document itself.
    print("Beispiel-Restaurant:")
    print(sample)

    # Print a header for the list of available fields.
    print("\nVerfügbare Felder:")
    # Iterate through the keys (field names) of the sample document.
    for key in sample.keys():
        # For each key, print the key name and its corresponding data type in the document.
        print(f"- {key}: {type(sample[key])}")
```

### Ausgabe

```shell
(.venv)  python test_queries.py
Beispiel-Restaurant:
```

```json
{'_id': ObjectId('5eb3d668b31de5d588f4292a'), 'address': {'building': '2780', 'coord': [-73.98241999999999, 40.579505], 'street': 'Stillwell Avenue', 'zipcode': '11224'}, 'borough': 'Brooklyn', 'cuisine': 'American', 'grades': [{'date': datetime.datetime(2014, 6, 10, 0, 0), 'grade': 'A', 'score': 5}, {'date': datetime.datetime(2013, 6, 5, 0, 0), 'grade': 'A', 'score': 7}, {'date': datetime.datetime(2012, 4, 13, 0, 0), 'grade': 'A', 'score': 12}, {'date': datetime.datetime(2011, 10, 12, 0, 0), 'grade': 'A', 'score': 12}], 'name': 'Riviera Caterer', 'restaurant_id': '40356018'}
```

```shell
Verfügbare Felder:
- _id: <class 'bson.objectid.ObjectId'>
- address: <class 'dict'>
- borough: <class 'str'>
- cuisine: <class 'str'>
- grades: <class 'list'>
- name: <class 'str'>
- restaurant_id: <class 'str'>
```

## 3.1 Einmalige Bezirke ausgeben

### Code

```py
def get_unique_boroughs():
    """
    Diese Funktion ruft alle einzigartigen Stadtbezirke (boroughs) aus der
    'restaurants' Collection ab und gibt sie auf der Konsole aus.

    Rückgabe:
        list: Eine Liste der einzigartigen Stadtbezirke.
    """

    # Verwendet die 'distinct' Methode, um alle einzigartigen Werte für das Feld "borough"
    # aus der 'collection' (die 'restaurants' Collection) abzurufen.
    boroughs = collection.distinct("borough")

    # Gibt eine Überschrift aus.
    print("Stadtbezirke:")
    # Iteriert über die Liste der abgerufenen Stadtbezirke.
    for borough in boroughs:
        # Gibt jeden Stadtbezirk in einem formatierten String aus.
        print(f"- {borough}")

    # Gibt die Liste der einzigartigen Stadtbezirke zurück.
    return boroughs
```

### Ausgabe

```shell
(.venv)  python test_queries.py
Stadtbezirke:
- Bronx
- Brooklyn
- Manhattan
- Missing
- Queens
- Staten Island
```

## 3.2 Top 3 Restaurants nach Rating ausgeben

### Code

```py
def get_top_rated_restaurants():
    """
    Diese Funktion findet die Top 3 Restaurants mit dem höchsten durchschnittlichen Score.
    Dazu wird eine Aggregations-Pipeline verwendet, um die Bewertungen zu verarbeiten
    und die Durchschnittswerte zu berechnen.

    Rückgabe:
        list: Eine Liste der Top 3 Restaurants, sortiert nach ihrem durchschnittlichen Score.
    """
    # Definiert die Aggregations-Pipeline. Eine Pipeline besteht aus mehreren Stufen,
    # die nacheinander auf die Dokumente angewendet werden.
    pipeline = [
        # Stufe 1: "$unwind"
        # Trennt das "grades"-Array in einzelne Dokumente auf. Für jedes Element im
        # "grades"-Array wird ein separates Dokument erstellt, das alle anderen Felder
        # des ursprünglichen Dokuments dupliziert. Dies ermöglicht es, individuelle
        # Bewertungen zu verarbeiten.
        {"$unwind": "$grades"},

        # Stufe 2: "$group"
        # Gruppiert die Dokumente nach dem Feld "name" (dem Namen des Restaurants).
        # Für jede Gruppe (jedes Restaurant) werden Aggregationsoperationen durchgeführt:
        # "_id": "$name" setzt den Gruppierungsschlüssel auf den Restaurantnamen.
        # "avg_score": {"$avg": "$grades.score"} berechnet den Durchschnitt der "score"-Werte
        #              aus dem "grades"-Feld für jedes Restaurant.
        # "restaurant_id": {"$first": "$_id"} speichert die ursprüngliche "_id" des
        #                  ersten Dokuments in der Gruppe.
        {"$group": {
            "_id": "$name",
            "avg_score": {"$avg": "$grades.score"},
            "restaurant_id": {"$first": "$_id"}
        }},

        # Stufe 3: "$sort"
        # Sortiert die Dokumente basierend auf dem berechneten "avg_score" in absteigender
        # Reihenfolge (-1), sodass die Restaurants mit dem höchsten Durchschnitts-Score
        # zuerst kommen.
        {"$sort": {"avg_score": -1}},

        # Stufe 4: "$limit"
        # Begrenzt die Anzahl der Ergebnisse auf die ersten 3 Dokumente nach der Sortierung.
        # Dies gibt uns die Top 3 Restaurants.
        {"$limit": 3}
    ]

    # Führt die Aggregations-Pipeline auf der 'collection' (der 'restaurants' Collection) aus.
    # Das Ergebnis der Aggregation ist ein Cursor, der in eine Liste umgewandelt wird.
    results = list(collection.aggregate(pipeline))

    # Gibt eine Überschrift für die Ergebnisse aus.
    print("Top 3 Restaurants:")
    # Iteriert über die Liste der Top 3 Restaurants. 'enumerate' wird verwendet,
    # um einen Index (i) für die Nummerierung hinzuzufügen.
    for i, restaurant in enumerate(results, 1):
        # Gibt jedes Restaurant mit seiner Nummer, seinem Namen und seinem
        # durchschnittlichen Score (formatiert auf zwei Dezimalstellen) aus.
        print(f"{i}. {restaurant['_id']} - Durchschnitt: {restaurant['avg_score']:.2f}")

    # Gibt die Liste der Top 3 Restaurants zurück.
    return results
```

### Ausgabe

```shell
(.venv)  python test_queries.py
Top 3 Restaurants:
1. Juice It Health Bar - Durchschnitt: 75.00
2. Golden Dragon Cuisine - Durchschnitt: 73.00
3. Chelsea'S Juice Factory - Durchschnitt: 69.00
```

## 3.3 Restaurant finden, das geografisch am nächsten bei „Le Perigord“ liegt

### Code

```py
def find_nearest_restaurant(restaurant_name="Le Perigord"):
    """
    Diese Funktion findet das Restaurant, das einem gegebenen Referenzrestaurant
    (standardmäßig "Le Perigord") geografisch am nächsten liegt.
    Dafür wird ein 2dsphere-Index auf den Geokoordinaten verwendet, um eine
    effiziente Abfrage nach räumlicher Nähe durchzuführen.

    Args:
        restaurant_name (str): Der Name des Restaurants, das als Referenzpunkt dient.
                               Standardmäßig ist dies "Le Perigord".

    Rückgabe:
        dict: Das Dokument des nächstgelegenen Restaurants oder None, falls das
              Referenzrestaurant nicht gefunden wird.
    """

    # Erstellt einen 2dsphere-Index auf dem Feld "address.coord".
    # Dieser Index ist entscheidend für effiziente geografische Abfragen wie "$near".
    # Wenn der Index bereits existiert, hat dieser Aufruf keine Auswirkung.
    collection.create_index([("address.coord", "2dsphere")])

    # Sucht das Referenzrestaurant anhand seines Namens.
    reference = collection.find_one({"name": restaurant_name})

    # Überprüft, ob das Referenzrestaurant gefunden wurde.
    if not reference:
        # Wenn das Referenzrestaurant nicht gefunden wird, wird eine Nachricht ausgegeben
        # und die Funktion beendet.
        print(f"Restaurant '{restaurant_name}' nicht gefunden")
        return None

    # Extrahiert die Koordinaten des Referenzrestaurants.
    # Die Koordinaten werden im Format [Längengrad, Breitengrad] erwartet.
    ref_coords = reference["address"]["coord"]

    # Führt eine Abfrage durch, um das nächstgelegene Restaurant zu finden.
    # "$near" ist ein räumlicher Operator, der Dokumente nach ihrer Nähe zu einem Punkt sortiert.
    # "$geometry" definiert den Referenzpunkt für die Suche.
    # "type": "Point" gibt an, dass es sich um einen Punkt handelt.
    # "coordinates": ref_coords sind die Längen- und Breitengrade des Referenzrestaurants.
    # "name": {"$ne": restaurant_name} stellt sicher, dass das Referenzrestaurant selbst
    #         nicht als das nächstgelegene Restaurant zurückgegeben wird.
    # .limit(1) begrenzt die Ergebnisse auf das nächstgelegene Restaurant.
    nearest = collection.find({
        "address.coord": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": ref_coords
                }
            }
        },
        "name": {"$ne": restaurant_name}  # Schließt das Referenzrestaurant aus
    }).limit(1)

    # Konvertiert den Cursor in eine Liste und holt das erste (und einzige) Ergebnis.
    result = list(nearest)[0]

    # Gibt den Namen und die Straße des nächstgelegenen Restaurants aus.
    print(f"- Name: {result['name']}")
    print(f"- Adresse: {result['address']['street']}")

    # Gibt das Dokument des nächstgelegenen Restaurants zurück.
    return result
```

### Ausgabe

```shell
(.venv)  python test_queries.py
Das naheste Restaurant zu Le Perigord
- Name: Subway
- Adresse: First Avenue
```