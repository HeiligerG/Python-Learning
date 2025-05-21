import re
from datetime import datetime
from pymongo import MongoClient

class RestaurantSearch:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['restaurants']
        self.collection = self.db['restaurants']
    
    def search_restaurants(self, name="", cuisine=""):
        """Suche nach Name und/oder Küche"""
        query = {}
        
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        
        if cuisine:
            query["cuisine"] = {"$regex": cuisine, "$options": "i"}
        
        results = list(self.collection.find(query))
        
        return results
    
    def display_results(self, results):
        """Suchergebnisse anzeigen"""
        if not results:
            print("Keine Restaurants gefunden.")
            return None
        
        print(f"\n{len(results)} Restaurant(s) gefunden:")
        for i, restaurant in enumerate(results):
            print(f"{i+1}. {restaurant['name']} - {restaurant['cuisine']}")
            print(f"   ID: {restaurant['_id']}")
        
        if len(results) > 1:
            print("\nWähle ein Restaurant (Nummer): ", end="")
            choice = int(input()) - 1
            return results[choice]['_id']
        else:
            return results[0]['_id']
    
    def run_search(self):
        """Interaktive Suche"""
        print("Restaurant-Suche")
        print("-" * 20)
        
        name = input("Name (oder Enter für alle): ").strip()
        cuisine = input("Küche (oder Enter für alle): ").strip()
        
        results = self.search_restaurants(name, cuisine)
        selected_id = self.display_results(results)
        
        return selected_id
    
if __name__ == "__main__":
    rs = RestaurantSearch()
    selected = rs.run_search()
    print(f"Ausgewählte Restaurant-ID: {selected}")