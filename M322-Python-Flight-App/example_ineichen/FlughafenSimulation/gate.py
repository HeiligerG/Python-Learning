# Modul gate.py: Definition der Gate-Klasse und GateManager-Klasse.
import json

class Gate:
    """
    Repräsentiert ein Gate (Flugsteig) im Flughafen.
    Attribute:
        gate_id (str): Bezeichnung des Gates (z.B. "Gate 1").
        in_wartung (bool): Ob das Gate gerade im Wartungszustand ist (True = in Wartung, False = betriebsbereit).
        besetzt_von (str or None): Flugnummer des Flugs, der dieses Gate aktuell belegt, oder None, wenn frei.
    """
    def __init__(self, gate_id: str, in_wartung: bool = False):
        self.gate_id = gate_id
        self.in_wartung = in_wartung
        self.besetzt_von = None  # None = kein Flug belegt das Gate

    def to_dict(self) -> dict:
        """Erstellt ein Wörterbuch des Gate-Zustands (für JSON-Speicherung)."""
        return {"gate_id": self.gate_id, "in_wartung": self.in_wartung}

    @staticmethod
    def from_dict(data: dict):
        """Erstellt ein Gate-Objekt aus einem Wörterbuch (z.B. aus JSON geladen)."""
        return Gate(data.get("gate_id", ""), data.get("in_wartung", False))


class GateManager:
    """
    Verwalter für mehrere Gates. Bietet Methoden zum Laden/Speichern, Suchen und Ändern des Gate-Status.
    """
    def __init__(self):
        self.gates = []

    def lade_daten(self, dateipfad: str):
        """
        Lädt die Gate-Daten aus einer JSON-Datei.
        Falls die Datei nicht existiert, wird eine Standardliste von Gates erstellt.
        """
        try:
            with open(dateipfad, "r", encoding="utf-8") as f:
                daten = json.load(f)
            self.gates = [Gate.from_dict(item) for item in daten]
        except (FileNotFoundError, json.JSONDecodeError):
            # Standardmässig einige Gates erzeugen, falls keine Daten vorhanden
            self.gates = [Gate(f"Gate {i+1}") for i in range(3)]  # z.B. 3 Gates: Gate 1, Gate 2, Gate 3

    def speichere_daten(self, dateipfad: str):
        """Speichert die Gate-Daten in einer JSON-Datei (ohne Belegungsinformationen, nur Zustand)."""
        with open(dateipfad, "w", encoding="utf-8") as f:
            json.dump([gate.to_dict() for gate in self.gates], f, ensure_ascii=False, indent=4)

    def finde_gate(self, gate_id: str):
        """Gibt das Gate-Objekt mit der gegebenen ID zurück (oder None, falls nicht gefunden)."""
        for gate in self.gates:
            if gate.gate_id == gate_id:
                return gate
        return None

    def freie_gates(self):
        """Gibt eine Liste aller Gates zurück, die aktuell nicht besetzt und nicht in Wartung sind."""
        return [gate for gate in self.gates if gate.besetzt_von is None and not gate.in_wartung]

    def gate_belegen(self, gate_id: str, flugnummer: str) -> bool:
        """
        Markiert ein Gate als besetzt durch einen Flug.
        Rückgabewert: True, wenn erfolgreich belegt, False, falls Gate nicht gefunden oder nicht verfügbar.
        """
        gate = self.finde_gate(gate_id)
        if gate and not gate.in_wartung and gate.besetzt_von is None:
            gate.besetzt_von = flugnummer
            return True
        return False

    def gate_freigeben(self, gate_id: str):
        """
        Markiert ein Gate als frei (kein Flug belegt es).
        Setzt besetzt_von auf None.
        """
        gate = self.finde_gate(gate_id)
        if gate:
            gate.besetzt_von = None

    def gate_wartung_umschalten(self, gate_id: str) -> bool:
        """
        Schaltet den Wartungszustand eines Gates um (an/aus).
        Wenn ein Gate gewartet wird, kann es nicht besetzt sein.
        Rückgabewert: True, wenn Umschalten erfolgreich, False, falls Gate belegt und nicht umschaltbar.
        """
        gate = self.finde_gate(gate_id)
        if gate:
            if gate.besetzt_von is not None:
                # Wenn Gate belegt, kann nicht in Wartung oder aus Wartung genommen werden
                return False
            # Wartungsstatus umkehren
            gate.in_wartung = not gate.in_wartung
            return True
        return False
