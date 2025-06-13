# Dokumentation zu Aufgabe 6.1
## Vorgegebe Files

### Filestruktur

├── dao_room.py  
├── main.py  
└── room.py

### main.py

```py
from room import Room
from dao_room import Dao_room

dao_room = Dao_room("mongodb://localhost:27017/")

# Create
room_create = Room("Pilatus", 12, True)
dao_room.create(room_create)

# Read
room_read = dao_room.read()
```

### dao_room.py

```py
from pymongo import MongoClient
from room import Room

class Dao_room:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        self.col.insert_one(room.__dict__)

    def read(self):
        room = Room(**self.col.find_one())
        return room

```


### room.py

```py
class Room:
    def __init__(self, name, seats, is_reservable, _id = None):
        if(_id is not None):
            self._id = _id
        self.name = name
        self.seats = seats
        self.is_reservable = is_reservable
```

## unsere Änderungen

### Hinzufügen der Methoden in dao_room.py

```py

def update(self, room_id, updated_room):
        self.col.update_one(
            {"_id": ObjectId(room_id)},
            {"$set": {
                "name": updated_room.name,
                "seats": updated_room.seats,
                "is_reservable": updated_room.is_reservable
            }}
        )

    def delete(self, room_id):
        self.col.delete_one({"_id": ObjectId(room_id)})

```

### Aufrufen der Methoden in main.py

```py

# Update
if hasattr(room_read, "_id"):
    updated_room = Room("Titlis", 20, False)
    dao_room.update(room_read._id, updated_room)
    print("Raum aktualisiert.")

# Read nach Update
room_updated = dao_room.read()
print("Aktualisierter Raum:")
print(vars(room_updated))

# Delete
if hasattr(room_updated, "_id"):
    dao_room.delete(room_updated._id)
    print("Raum gelöscht.")
```
