from pymongo import MongoClient

class Connection:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
    
    def makeConnection(self):
        """Stellt eine Verbindung zur MongoDB her"""
        try:
            self.client = MongoClient('mongodb://localhost:27017')
            
            self.db = self.client['restaurants']
            
            self.collection = self.db['restaurants']
            
            print("Verbindung zur MongoDB erfolgreich hergestellt!")
            return True
            
        except Exception as e:
            print(f"Fehler bei der Verbindung: {e}")
            return False
    
    def closeConnection(self):
        """Schließt die Verbindung zur MongoDB"""
        if self.client:
            self.client.close()
            print("Verbindung geschlossen.")