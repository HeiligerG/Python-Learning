from pymongo import MongoClient
from test_queries import get_top_rated_restaurants, get_unique_boroughs, find_nearest_restaurant

def main():
    client = MongoClient('mongodb://localhost:27017')
    db = client['db_restaurants']
    collection = db['restaurants']

    print("Einzigartige Boroughs:")
    get_unique_boroughs()

    print("\nTop-bewertete Restaurants:")
    get_top_rated_restaurants()

    print("\nDas naheste Restaurant zu Le Perigord")
    find_nearest_restaurant()
    
    client.close()

if __name__ == "__main__":
    main()