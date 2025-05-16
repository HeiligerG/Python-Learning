import bson.json_util
from pymongo import MongoClient
import bson

client = MongoClient('mongodb://localhost:27017')
db = client['restaurants']
collection = db['restaurants']
restaurant = 'Le Perigord'

def get_nearest_restaurant_to_LePerigord():
    baseRestaurant = collection.find_one({'name': '{restaurant}'})

    if baseRestaurant:

        json_output = bson.json_util.dumps(baseRestaurant)
        print(json_output)

    else:
        print(bson.json_util.dumps({"error": "Restaurant '{restaurant}' nicht gefunden."}, indent=4))
