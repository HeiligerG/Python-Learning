# Modul ticket.py: Definition der Ticket-Klasse und TicketManager-Klasse.
import json

class Ticket:
    """
    Repräsentiert ein Ticket bzw. einen Check-in für einen Flug.
    Attribute:
        name (str): Name des Passagiers.
        flugnummer (str): Flugnummer des gebuchten Flugs.
    """
    def __init__(self, name: str, flugnummer: str):
        self.name = name
        self.flugnummer = flugnummer

    def to_dict(self) -> dict:
        """Erstellt ein Wörterbuch aus dem Ticket (für JSON-Speicherung)."""
        return {"name": self.name, "flugnummer": self.flugnummer}

    @staticmethod
    def from_dict(data: dict):
        """Erstellt ein Ticket-Objekt aus einem Wörterbuch (z.B. aus JSON geladen)."""
        return Ticket(data.get("name", ""), data.get("flugnummer", ""))


class TicketManager:
    """
    Verwalter für alle ausgestellten Tickets (verkaufte Tickets bzw. eingecheckte Passagiere).
    Bietet Methoden zum Laden/Speichern und Hinzufügen neuer Tickets.
    """
    def __init__(self):
        self.tickets = []

    def lade_daten(self, dateipfad: str):
        """
        Lädt die Ticketdaten aus einer JSON-Datei.
        Falls die Datei nicht existiert oder ungültig ist, wird mit keiner bzw. leerer Liste gestartet.
        """
        try:
            with open(dateipfad, "r", encoding="utf-8") as f:
                daten = json.load(f)
            self.tickets = [Ticket.from_dict(item) for item in daten]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tickets = []

    def speichere_daten(self, dateipfad: str):
        """Speichert alle Tickets in einer JSON-Datei."""
        with open(dateipfad, "w", encoding="utf-8") as f:
            json.dump([ticket.to_dict() for ticket in self.tickets], f, ensure_ascii=False, indent=4)

    def ticket_hinzufuegen(self, name: str, flugnummer: str):
        """
        Erstellt ein neues Ticket (bzw. Check-in) für den gegebenen Passagiernamen und die Flugnummer.
        Fügt es der Ticketliste hinzu.
        """
        neues_ticket = Ticket(name, flugnummer)
        self.tickets.append(neues_ticket)
        return True
