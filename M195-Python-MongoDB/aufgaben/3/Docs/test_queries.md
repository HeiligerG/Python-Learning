# Dokumentation der test_queries um alles vollumfänglich zu verstehen

## Connection und erstes Sample

### Code

```py
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

## Erste Funktion zum suchen von Stadtbezirke

### Code

```py
def get_unique_boroughs():
    """Alle einzigartigen Stadtbezirke ausgeben"""

    boroughs = collection.distinct("borough")
    
    print("Stadtbezirke:")
    for borough in boroughs:
        print(f"- {borough}")
    
    return boroughs

get_unique_boroughs()
```

### Ausgabe

```shell
Beispiel-Restaurant:

Einzigartige Boroughs:
Stadtbezirke:
- Bronx
- Brooklyn
- Manhattan
- Missing
- Queens
- Staten Island
```

## Zweite Funktion zum suchen von den 3 best bewertetenRestaurants

### Code

```py
def get_top_rated_restaurants():
    """Top 3 Restaurants mit höchstem Durchschnitts-Score"""
    pipeline = [
        {"$unwind": "$grades"},
        
        {"$group": {
            "_id": "$name",
            "avg_score": {"$avg": "$grades.score"},
            "restaurant_id": {"$first": "$_id"}
        }},
        
        {"$sort": {"avg_score": -1}},
        
        {"$limit": 3}
    ]
    
    results = list(collection.aggregate(pipeline))
    
    print("Top 3 Restaurants:")
    for i, restaurant in enumerate(results, 1):
        print(f"{i}. {restaurant['_id']} - Durchschnitt: {restaurant['avg_score']:.2f}")
    
    return results
get_top_rated_restaurants()
```

### Ausgabe

```shell
Top-bewertete Restaurants:
Top 3 Restaurants:
1. Juice It Health Bar - Durchschnitt: 75.00
2. Golden Dragon Cuisine - Durchschnitt: 73.00
3. Palombo Pastry Shop - Durchschnitt: 69.00
```

### Code

```py
def find_nearest_restaurant(restaurant_name="Le Perigord"):
    """Restaurant finden, das geografisch am nächsten liegt"""

    collection.create_index([("address.coord", "2dsphere")])
    
    reference = collection.find_one({"name": restaurant_name})
    
    if not reference:
        print(f"Restaurant '{restaurant_name}' nicht gefunden")
        return None
    
    ref_coords = reference["address"]["coord"]
    
    nearest = collection.find({
        "address.coord": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": ref_coords
                }
            }
        },
        "name": {"$ne": restaurant_name}
    }).limit(1)
    
    result = list(nearest)[0]
    print(f"- Name: {result['name']}")
    print(f"- Adresse: {result['address']['street']}")
    
    return result
find_nearest_restaurant()
```

### Ausgabe

```shell
Das naheste Restaurant zu Le Perigord
- Name: Subway
- Adresse: First Avenue
```