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