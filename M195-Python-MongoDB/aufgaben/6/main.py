from room import Room
from dao_room import Dao_room

dao_room = Dao_room("mongodb://localhost:27017/")

# Create
room_create = Room("Pilatus", 12, True)
dao_room.create(room_create)

# Read
room_read = dao_room.read()
print("Gelesener Raum:")
print(vars(room_read))  

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
