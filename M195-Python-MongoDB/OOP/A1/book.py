class Buch:
    def __init__(self, titel, author, isbn, preis):
        self.titel = titel
        self.author = author
        self.isbn = isbn
        self.preis = preis
    
    def __str__(self):
        return f"Titel: {self.titel}, Author: {self.author}, ISBN: {self.isbn}, Preis: {self.preis}€"