from book import Buch
from connection import makeConnection
from pymongo import mongo_client

def main():
    buecher_liste = [
    Buch("Der Herr der Ringe", "J.R.R. Tolkien", "978-3-608-93830-2", 15.99),
    Buch("Harry Potter und der Stein der Weisen", "J.K. Rowling", "978-3-551-35401-4", 12.50),
    Buch("1984", "George Orwell", "978-3-548-23410-8", 9.99),
    Buch("Python Programming", "Mark Lutz", "978-1-449-35573-9", 45.00),
    ]

if __name__ == "__main__":
    # Connection-Objekt erstellen
    conn = Connection()
    
    # Verbindung herstellen
    if conn.makeConnection():
        # Hier können Sie mit der Collection arbeiten
        # Beispiel: Anzahl Dokumente zählen
        try:
            count = conn.collection.count_documents({})
            print(f"Anzahl Restaurants in der Collection: {count}")
        except Exception as e:
            print(f"Fehler beim Zugriff auf Collection: {e}")
        
        # Verbindung schließen
        conn.closeConnection()
    else:
        print("Verbindung konnte nicht hergestellt werden.")