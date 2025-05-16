from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['restaurants']
collection = db['restaurants']

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

def get_unique_boroughs():
    """Alle einzigartigen Stadtbezirke ausgeben"""

    boroughs = collection.distinct("borough")
    
    print("Stadtbezirke:")
    for borough in boroughs:
        print(f"- {borough}")
    
    return boroughs