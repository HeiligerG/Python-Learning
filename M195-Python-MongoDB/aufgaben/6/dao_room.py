from pymongo import MongoClient
from room import Room
from bson.objectid import ObjectId

class Dao_room:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        self.col.insert_one(room.__dict__)

    def read(self):
        room_data = self.col.find_one()
        if room_data:
            return Room(**room_data)
        return None

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
