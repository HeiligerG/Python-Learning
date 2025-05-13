# Modul flug.py: Definition der Flug-Klasse und FlugManager-Klasse.
import json

class Flug:
    """
    Eine Klasse, die einen Flug repräsentiert.
    Attribute:
        flugnummer (str): Eindeutige Kennung des Flugs (z.B. "WK123").
        typ (str): Art des Flugs - "Landung" oder "Start".
        status (str): Aktueller Status des Flugs (z. B. "Landen", "Starten", "Wartung", "Gate belegt").
        gate (str or None): Gate-Bezeichnung, wenn das Flugzeug einem Gate zugewiesen ist, sonst None.
    """
    def __init__(self, flugnummer: str, typ: str, status: str, gate: str = None):
        self.flugnummer = flugnummer
        self.typ = typ          # "Landung" oder "Start"
        self.status = status    # z.B. "Wartet", "Landen", "Starten", "Gate belegt", "Wartung"
        self.gate = gate        # z.B. "Gate 1" oder None, falls kein Gate zugewiesen

    def to_dict(self) -> dict:
        """Erstellt ein Wörterbuch aus dem Flug-Objekt (für die JSON-Speicherung)."""
        return {"flugnummer": self.flugnummer, "typ": self.typ, "status": self.status, "gate": self.gate}

    @staticmethod
    def from_dict(data: dict):
        """Erstellt ein Flug-Objekt aus einem Wörterbuch (z.B. aus JSON geladen)."""
        return Flug(data.get("flugnummer", ""), data.get("typ", ""), data.get("status", ""), data.get("gate", None))


class FlugManager:
    """
    Diese Klasse verwaltet eine Liste von Flügen und bietet Methoden zum Hinzufügen, Entfernen
    und Speichern/Laden der Flugdaten.
    """
    def __init__(self):
        # Liste der Flugobjekte
        self.fluege = []

    def lade_daten(self, dateipfad: str):
        """
        Lädt die Flugdaten aus einer JSON-Datei.
        Existiert die Datei nicht oder ist fehlerhaft, wird mit einer leeren Liste gestartet.
        """
        try:
            with open(dateipfad, "r", encoding="utf-8") as f:
                daten = json.load(f)
            # JSON sollte eine Liste von Flug-Dictionaries enthalten
            self.fluege = [Flug.from_dict(item) for item in daten]
        except (FileNotFoundError, json.JSONDecodeError):
            # Falls Datei nicht gefunden oder JSON ungültig, beginne mit leeren Flugdaten
            self.fluege = []

    def speichere_daten(self, dateipfad: str):
        """Speichert alle Flugdaten in einer JSON-Datei."""
        with open(dateipfad, "w", encoding="utf-8") as f:
            json.dump([flug.to_dict() for flug in self.fluege], f, ensure_ascii=False, indent=4)

    def finde_flug(self, flugnummer: str):
        """Sucht einen Flug anhand der Flugnummer und gibt das Flug-Objekt zurück (oder None, falls nicht gefunden)."""
        for flug in self.fluege:
            if flug.flugnummer == flugnummer:
                return flug
        return None

    def flug_hinzufuegen(self, flugnummer: str, typ: str) -> bool:
        """
        Fügt einen neuen Flug hinzu, falls die Flugnummer noch nicht existiert.
        Der Status wird initial abhängig vom Flugtyp gesetzt.
        Rückgabewert: True, wenn erfolgreich hinzugefügt, oder False, falls die Flugnummer bereits existiert.
        """
        # Prüfen, ob Flugnummer bereits vorhanden ist
        if self.finde_flug(flugnummer) is not None:
            return False
        # Initialer Status festlegen: Alle neuen Flüge warten zunächst (bis Landung/Start ausgeführt wird)
        initial_status = "Wartet"
        # Neuen Flug erstellen
        neuer_flug = Flug(flugnummer, typ, initial_status, gate=None)
        self.fluege.append(neuer_flug)
        return True

    def flug_entfernen(self, flugnummer: str) -> bool:
        """
        Entfernt den Flug mit der angegebenen Flugnummer aus der Liste.
        Rückgabewert: True, wenn ein Flug entfernt wurde, sonst False.
        """
        flug = self.finde_flug(flugnummer)
        if flug:
            self.fluege.remove(flug)
            return True
        return False
