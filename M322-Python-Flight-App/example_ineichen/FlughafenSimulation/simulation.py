# Modul simulation.py: Koordiniert Flüge, Gates und Tickets.
from flug import FlugManager
from gate import GateManager
from ticket import TicketManager

class FlughafenSimulation:
    """
    Die Haupt-Klasse der Simulation, die Flüge, Gates und Tickets koordiniert.
    Sie hält je einen Manager für Flüge, Gates und Tickets.
    Bietet Methoden, um typische Vorgänge im Flughafen zu steuern (z.B. Flüge landen/starten, Gates zuweisen).
    """
    def __init__(self, flug_datei="fluege.json", gate_datei="gates.json", ticket_datei="tickets.json"):
        # Manager für verschiedene Bereiche der Simulation erstellen
        self.flug_manager = FlugManager()
        self.gate_manager = GateManager()
        self.ticket_manager = TicketManager()
        # Daten aus Dateien laden
        self.flug_manager.lade_daten(flug_datei)
        self.gate_manager.lade_daten(gate_datei)
        self.ticket_manager.lade_daten(ticket_datei)
        # Nach dem Laden: Gate-Belegungen anhand der Flugdaten herstellen
        self.sync_gate_belegung()

        # Dateipfade speichern, um beim Beenden alle Daten sichern zu können
        self.flug_datei = flug_datei
        self.gate_datei = gate_datei
        self.ticket_datei = ticket_datei

    def sync_gate_belegung(self):
        """
        Synchronisiert die Gate-Belegungen basierend auf den geladenen Flugdaten.
        D.h. falls Flüge gespeichert waren, die einem Gate zugewiesen sind, markiere diese Gates als besetzt.
        """
        for gate in self.gate_manager.gates:
            gate.besetzt_von = None  # Alle Belegungen zurücksetzen
        for flug in self.flug_manager.fluege:
            if flug.gate:
                # Flug hat ein Gate, dieses Gate entsprechend markieren
                gate = self.gate_manager.finde_gate(flug.gate)
                if gate:
                    gate.besetzt_von = flug.flugnummer

    def speichere_alles(self):
        """Speichert alle Bereiche (Flüge, Gates, Tickets) in ihren JSON-Dateien."""
        self.flug_manager.speichere_daten(self.flug_datei)
        self.gate_manager.speichere_daten(self.gate_datei)
        self.ticket_manager.speichere_daten(self.ticket_datei)

    def flug_hinzufuegen(self, flugnummer: str, typ: str) -> bool:
        """
        Fügt einen neuen Flug hinzu. Falls es ein Start-Flug ist und ein Gate frei ist, wird er direkt einem Gate zugewiesen.
        """
        erfolgreich = self.flug_manager.flug_hinzufuegen(flugnummer, typ)
        if not erfolgreich:
            return False
        # Wurde hinzugefügt, zusätzliche Logik für Start-Flüge:
        if typ == "Start":
            # Neu hinzugefügten Flug finden
            flug = self.flug_manager.finde_flug(flugnummer)
            # Falls ein freies Gate vorhanden ist, weise es sofort zu
            freie = self.gate_manager.freie_gates()
            if flug and freie:
                gate_obj = freie[0]
                flug.gate = gate_obj.gate_id
                flug.status = "Gate belegt"  # Status anpassen, da Flugzeug nun am Gate steht
                gate_obj.besetzt_von = flug.flugnummer
        return True

    def flug_entfernen(self, flugnummer: str) -> bool:
        """
        Entfernt einen Flug (z.B. wenn ein Start erfolgt oder der Flug gestrichen wurde).
        Gibt True zurück, wenn entfernt.
        Dabei wird auch das zugehörige Gate wieder freigegeben (falls der Flug an einem Gate stand).
        """
        # Vor dem Entfernen prüfen, ob Flug ein Gate belegt hatte, um das Gate frei zu machen.
        flug = self.flug_manager.finde_flug(flugnummer)
        if flug and flug.gate:
            # Gate freigeben
            self.gate_manager.gate_freigeben(flug.gate)
        # Flug entfernen
        return self.flug_manager.flug_entfernen(flugnummer)

    def landung_durchfuehren(self, flugnummer: str) -> bool:
        """
        Simuliert die Landung eines wartenden Flugs.
        Findet ein freies Gate und weist es dem Flug zu. Der Flugstatus wird auf "Gate belegt" gesetzt.
        Gibt True zurück, wenn erfolgreich zugewiesen, False falls kein Gate frei.
        """
        flug = self.flug_manager.finde_flug(flugnummer)
        if not flug or flug.typ != "Landung":
            return False
        # Prüfen, ob bereits an einem Gate (dann ist Landung schon erfolgt)
        if flug.gate is not None:
            return False
        # Freies Gate suchen
        freie = self.gate_manager.freie_gates()
        if not freie:
            return False
        # Nimm das erste freie Gate und weise es zu
        gate_obj = freie[0]
        flug.gate = gate_obj.gate_id
        flug.status = "Gate belegt"
        gate_obj.besetzt_von = flug.flugnummer
        return True

    def start_durchfuehren(self, flugnummer: str) -> bool:
        """
        Simuliert den Start eines Flugs.
        Entfernt den Flug aus der Liste und gibt sein Gate frei.
        Gibt True zurück, wenn Start (Entfernung) erfolgreich war.
        """
        return self.flug_entfernen(flugnummer)

    def flug_in_wartung(self, flugnummer: str) -> bool:
        """
        Versetzt einen Flug in den Wartungszustand.
        D.h. der Flug muss sein Gate verlassen (Gate wird frei) und der Flugstatus wird auf "Wartung" gesetzt.
        Rückgabewert: True, wenn erfolgreich in Wartung versetzt, False sonst.
        """
        flug = self.flug_manager.finde_flug(flugnummer)
        if not flug:
            return False
        if flug.gate:
            # Gate freimachen
            self.gate_manager.gate_freigeben(flug.gate)
            flug.gate = None
        # Status auf Wartung setzen
        flug.status = "Wartung"
        return True

    def gate_wartung_umschalten(self, gate_id: str) -> bool:
        """
        Schaltet den Wartungsstatus eines Gates um.
        Gibt False zurück, wenn das Gate nicht umgeschaltet werden konnte (z.B. weil es belegt ist).
        """
        return self.gate_manager.gate_wartung_umschalten(gate_id)

    def ticket_kaufen(self, name: str, flugnummer: str) -> bool:
        """
        Erstellt ein Ticket (Check-in) für einen Passagier mit dem angegebenen Namen
        für den Flug mit der gegebenen Flugnummer.
        Gibt True zurück, wenn erfolgreich (Flug muss existieren), sonst False.
        """
        # Prüfen, ob Flug existiert
        flug = self.flug_manager.finde_flug(flugnummer)
        if not flug:
            return False
        # Ticket hinzufügen
        self.ticket_manager.ticket_hinzufuegen(name, flugnummer)
        return True
