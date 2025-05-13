# Modul main.py: GUI-Anwendung (Tkinter) der Flughafen-Simulation.
import tkinter as tk
from tkinter import ttk, messagebox
from simulation import FlughafenSimulation

# Hauptfenster erstellen
root = tk.Tk()
root.title("Flughafen-Simulation")

# Simulation-Objekt erstellen (lädt Daten aus JSON-Dateien)
sim = FlughafenSimulation()

# Funktion zum Aktualisieren der Flugliste (Treeview)
def aktualisiere_flugliste():
    """Lädt alle Flüge aus dem FlugManager ins Treeview."""
    flug_tree.delete(*flug_tree.get_children())  # Alle Einträge entfernen
    for flug in sim.flug_manager.fluege:
        flugnummer = flug.flugnummer
        typ = flug.typ
        status = flug.status
        gate = flug.gate if flug.gate is not None else ""
        flug_tree.insert("", "end", iid=flugnummer, values=(flugnummer, typ, status, gate))

# Funktion zum Aktualisieren der Gate-Liste (Treeview)
def aktualisiere_gateliste():
    """Lädt alle Gates aus dem GateManager ins Treeview."""
    gate_tree.delete(*gate_tree.get_children())
    for gate in sim.gate_manager.gates:
        gate_id = gate.gate_id
        if gate.in_wartung:
            status = "Wartung"
        elif gate.besetzt_von:
            status = "Belegt"
        else:
            status = "Frei"
        flug_bezeichnung = gate.besetzt_von if gate.besetzt_von is not None else ""
        gate_tree.insert("", "end", iid=gate_id, values=(gate_id, status, flug_bezeichnung))

# Funktion zum Aktualisieren der Flugauswahl im Ticketverkaufs-Combobox (nur Start-Flüge)
def aktualisiere_flug_options():
    """Aktualisiert die Liste der Flugnummern (nur Start-Flüge) für den Ticketverkauf."""
    flug_optionen = [flug.flugnummer for flug in sim.flug_manager.fluege if flug.typ == "Start"]
    flug_optionen.sort()
    flug_combobox['values'] = flug_optionen
    # Falls aktuelle Auswahl nicht mehr existiert, zurücksetzen
    aktueller = flug_combobox.get()
    if aktueller not in flug_optionen:
        flug_combobox.set('')

# Event-Handler für "Flug hinzufügen"
def hinzufuegen_click():
    nummer = eintrag_flugnummer.get().strip()
    typ = typ_combobox.get().strip()
    if nummer == "" or typ == "":
        messagebox.showwarning("Eingabe fehlt", "Bitte Flugnummer und Typ angeben.")
        return
    # Flug hinzufügen versuchen
    erfolg = sim.flug_hinzufuegen(nummer, typ)
    if not erfolg:
        messagebox.showerror("Fehler", f"Flug {nummer} existiert bereits.")
        return
    # Erfolgreich hinzugefügt: neuen Flug in der Tabelle anzeigen
    flug = sim.flug_manager.finde_flug(nummer)
    if flug:
        flug_tree.insert("", "end", iid=flug.flugnummer, values=(flug.flugnummer, flug.typ, flug.status, flug.gate if flug.gate else ""))
    # Gate-Liste aktualisieren, falls ein Gate belegt wurde (bei Start-Flug)
    if flug and flug.gate:
        aktualisiere_gateliste()
    # Flugoptionen für Ticketverkauf aktualisieren
    aktualisiere_flug_options()
    # Eingabefelder zurücksetzen
    eintrag_flugnummer.delete(0, tk.END)
    typ_combobox.set('')

# Event-Handler für "Flug entfernen"
def entfernen_click():
    auswahl = flug_tree.selection()
    if not auswahl:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Flug aus der Liste.")
        return
    flugnummer = auswahl[0]  # bei gesetztem id entspricht dies der Flugnummer
    flug = sim.flug_manager.finde_flug(flugnummer)
    # Merken, ob dieser Flug ein Gate belegt hat, um das Gate anschliessend freizugeben
    gate_id = flug.gate if flug else None
    erfolg = sim.flug_entfernen(flugnummer)
    if not erfolg:
        messagebox.showerror("Fehler", f"Flug {flugnummer} konnte nicht entfernt werden.")
        return
    # Flug aus der Treeview entfernen
    flug_tree.delete(flugnummer)
    # Gate-Liste aktualisieren, falls ein Gate frei wurde
    if gate_id:
        aktualisiere_gateliste()
    # Flugoptionen für Ticketverkauf aktualisieren (falls ein Start-Flug entfernt wurde)
    aktualisiere_flug_options()

# Event-Handler für "Landung durchführen"
def landung_click():
    auswahl = flug_tree.selection()
    if not auswahl:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen landenden Flug aus.")
        return
    flugnummer = auswahl[0]
    flug = sim.flug_manager.finde_flug(flugnummer)
    if not flug or flug.typ != "Landung":
        messagebox.showerror("Ungültig", "Der ausgewählte Flug ist kein Landungs-Flug.")
        return
    if flug.gate:
        messagebox.showinfo("Bereits gelandet", f"Flug {flugnummer} ist bereits an einem Gate.")
        return
    # Status auf "Landen" setzen und anzeigen
    flug.status = "Landen"
    flug_tree.item(flugnummer, values=(flug.flugnummer, flug.typ, flug.status, ""))  # Gate bleibt leer bis Zuweisung
    # Button vorübergehend deaktivieren, um Doppelklick zu vermeiden
    landung_btn.config(state="disabled")
    # Nach 2 Sekunden Landung abschliessen (Gate zuweisen)
    root.after(2000, lambda: _landung_abschliessen(flugnummer))

def _landung_abschliessen(flugnummer: str):
    """Interne Funktion, die nach kurzer Verzögerung die Landung abschließt."""
    erfolgreich = sim.landung_durchfuehren(flugnummer)
    flug = sim.flug_manager.finde_flug(flugnummer)
    if erfolgreich and flug:
        # Flug wurde einem Gate zugewiesen
        flug_tree.item(flugnummer, values=(flug.flugnummer, flug.typ, flug.status, flug.gate if flug.gate else ""))
        aktualisiere_gateliste()
    else:
        # Kein Gate frei, Landung zurückstellen
        if flug:
            flug.status = "Wartet"
            flug_tree.item(flugnummer, values=(flug.flugnummer, flug.typ, flug.status, ""))
        messagebox.showwarning("Landung verschoben", f"Flug {flugnummer} konnte nicht landen, kein Gate frei.")
    # Button wieder aktivieren
    landung_btn.config(state="normal")

# Event-Handler für "Start durchführen"
def start_click():
    auswahl = flug_tree.selection()
    if not auswahl:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen startenden Flug aus.")
        return
    flugnummer = auswahl[0]
    flug = sim.flug_manager.finde_flug(flugnummer)
    if not flug or flug.typ != "Start":
        messagebox.showerror("Ungültig", "Der ausgewählte Flug ist kein Start-Flug.")
        return
    if not flug.gate:
        # Versuche JETZT ein freies Gate zu finden
        freie = sim.gate_manager.freie_gates()
        if freie:
            gate_obj = freie[0]
            gate_obj.besetzt_von = flug.flugnummer
            flug.gate = gate_obj.gate_id
            flug.status = "Gate belegt"
            # Anzeige sofort aktualisieren
            flug_tree.item(flugnummer, values=(flug.flugnummer, flug.typ, flug.status, flug.gate))
            aktualisiere_gateliste()
        else:
            messagebox.showerror("Kein Gate", f"Flug {flugnummer} hat kein Gate und kann nicht starten.")
            return
    # Status auf "Starten" setzen und anzeigen
    flug.status = "Starten"
    flug_tree.item(flugnummer, values=(flug.flugnummer, flug.typ, flug.status, flug.gate))
    start_btn.config(state="disabled")
    # Nach 2 Sekunden den Start (Entfernen des Flugs) abschliessen
    root.after(2000, lambda: _start_abschliessen(flugnummer, flug.gate))

def _start_abschliessen(flugnummer: str, gate_id: str):
    """Interne Funktion, die nach kurzer Verzögerung den Start abschliesst (Flug entfernen)."""
    sim.start_durchfuehren(flugnummer)
    # Flug aus der Anzeige entfernen
    try:
        flug_tree.delete(flugnummer)
    except Exception:
        pass
    # Gate-Liste aktualisieren (Gate freigeben)
    if gate_id:
        aktualisiere_gateliste()
    # Flugoptionen aktualisieren (Flug ist entfernt)
    aktualisiere_flug_options()
    start_btn.config(state="normal")

# Event-Handler für "Flug in Wartung versetzen"
def wartung_click():
    auswahl = flug_tree.selection()
    if not auswahl:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Flug aus.")
        return
    flugnummer = auswahl[0]
    flug = sim.flug_manager.finde_flug(flugnummer)
    if not flug:
        return
    if flug.gate is None:
        messagebox.showerror("Nicht möglich", "Dieser Flug ist nicht an einem Gate und kann nicht in Wartung gehen.")
        return
    # Flug in Wartung versetzen
    sim.flug_in_wartung(flugnummer)
    flug = sim.flug_manager.finde_flug(flugnummer)
    if flug:
        # Anzeige aktualisieren (Flug nun "Wartung", Gate frei)
        flug_tree.item(flugnummer, values=(flug.flugnummer, flug.typ, flug.status, ""))
        aktualisiere_gateliste()

# Event-Handler für "Gate Wartung umschalten"
def gate_wartung_click():
    auswahl = gate_tree.selection()
    if not auswahl:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie ein Gate aus.")
        return
    gate_id = auswahl[0]
    erfolgreich = sim.gate_wartung_umschalten(gate_id)
    if not erfolgreich:
        messagebox.showerror("Aktion nicht möglich", "Gate kann nicht gewartet werden, solange es belegt ist.")
    # Anzeige (Gate-Liste) aktualisieren
    aktualisiere_gateliste()

# Event-Handler für "Ticket ausstellen"
def ticket_kaufen_click():
    name = name_entry.get().strip()
    flugnr = flug_combobox.get().strip()
    if name == "" or flugnr == "":
        messagebox.showwarning("Eingabe fehlt", "Bitte Name und Flug auswählen.")
        return
    erfolg = sim.ticket_kaufen(name, flugnr)
    if not erfolg:
        messagebox.showerror("Fehler", f"Ticket für Flug {flugnr} konnte nicht erstellt werden.")
        return
    # Neues Ticket in der Ticketliste anzeigen
    ticket_tree.insert("", "end", values=(name, flugnr))
    # Eingabefelder zurücksetzen
    name_entry.delete(0, tk.END)
    flug_combobox.set('')

# Funktion, die beim Schliessen des Fensters aufgerufen wird (zum Speichern der Daten)
def beenden():
    sim.speichere_alles()  # alle aktuellen Daten in JSON-Dateien speichern
    root.destroy()

root.protocol("WM_DELETE_WINDOW", beenden)

# Notebook für verschiedene Bereiche der Simulation (Flugbetrieb, Ticketverkauf)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Frame für Flugbetrieb (Flüge und Gates)
frame_betrieb = ttk.Frame(notebook)
notebook.add(frame_betrieb, text="Flugbetrieb")

# Frame für Ticketverkauf
frame_tickets = ttk.Frame(notebook)
notebook.add(frame_tickets, text="Ticketverkauf")

# --- Bereich Flugbetrieb (Flüge & Gates) ---

# Labelframe für Flüge
fluege_frame = ttk.LabelFrame(frame_betrieb, text="Flüge")
fluege_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# Treeview für die Flüge
columns = ("Flug", "Typ", "Status", "Gate")
flug_tree = ttk.Treeview(fluege_frame, columns=columns, show="headings", height=10)
flug_tree.heading("Flug", text="Flug")
flug_tree.heading("Typ", text="Typ")
flug_tree.heading("Status", text="Status")
flug_tree.heading("Gate", text="Gate")
# Scrollbar für die Flugliste
flug_scroll = ttk.Scrollbar(fluege_frame, orient="vertical", command=flug_tree.yview)
flug_tree.configure(yscrollcommand=flug_scroll.set)
# Treeview und Scrollbar anordnen
flug_tree.pack(side="left", fill="both", expand=True)
flug_scroll.pack(side="left", fill="y")

# Rahmen für die Flug-Steuerung-Buttons und Eingabefelder
flug_controls_frame = ttk.Frame(fluege_frame)
flug_controls_frame.pack(side="bottom", fill="x", padx=5, pady=5)

# Unterer Rahmen für "Flug hinzufügen"
add_frame = ttk.Frame(flug_controls_frame)
add_frame.pack(fill="x", pady=2)
ttk.Label(add_frame, text="Flugnr:").pack(side="left")
eintrag_flugnummer = ttk.Entry(add_frame, width=10)
eintrag_flugnummer.pack(side="left", padx=5)
ttk.Label(add_frame, text="Typ:").pack(side="left")
typ_combobox = ttk.Combobox(add_frame, values=["Landung", "Start"], width=7, state="readonly")
typ_combobox.pack(side="left", padx=5)
typ_combobox.set("")  # Keine Vorauswahl
hinzufuegen_btn = ttk.Button(add_frame, text="Hinzufügen", command=hinzufuegen_click)
hinzufuegen_btn.pack(side="left", padx=5)

# Rahmen für Aktions-Buttons (Entfernen, Landung, Start, Wartung)
action_frame = ttk.Frame(flug_controls_frame)
action_frame.pack(fill="x", pady=2)
entfernen_btn = ttk.Button(action_frame, text="Entfernen", command=entfernen_click)
entfernen_btn.pack(side="left", padx=5)
landung_btn = ttk.Button(action_frame, text="Landung", command=landung_click)
landung_btn.pack(side="left", padx=5)
start_btn = ttk.Button(action_frame, text="Start", command=start_click)
start_btn.pack(side="left", padx=5)
wartung_btn = ttk.Button(action_frame, text="Wartung", command=wartung_click)
wartung_btn.pack(side="left", padx=5)

# Labelframe für Gates
gates_frame = ttk.LabelFrame(frame_betrieb, text="Gates")
gates_frame.pack(side="left", fill="y", expand=False, padx=5, pady=5)

# Treeview für Gates
gate_columns = ("Gate", "Status", "Flug")
gate_tree = ttk.Treeview(gates_frame, columns=gate_columns, show="headings", height=10)
gate_tree.heading("Gate", text="Gate")
gate_tree.heading("Status", text="Status")
gate_tree.heading("Flug", text="Flug")
# Scrollbar für Gate-Liste (falls benötigt)
gate_scroll = ttk.Scrollbar(gates_frame, orient="vertical", command=gate_tree.yview)
gate_tree.configure(yscrollcommand=gate_scroll.set)
gate_tree.pack(side="left", fill="y", expand=False)
gate_scroll.pack(side="left", fill="y")

# Button für Gate-Wartung umschalten
gate_btn_frame = ttk.Frame(gates_frame)
gate_btn_frame.pack(side="bottom", fill="x", pady=5)
gate_wartung_btn = ttk.Button(gate_btn_frame, text="Wartung an/aus", command=gate_wartung_click)
gate_wartung_btn.pack(padx=5)

# --- Bereich Ticketverkauf ---

# Labelframe für Ticketerstellung
ticket_input_frame = ttk.LabelFrame(frame_tickets, text="Neues Ticket ausstellen")
ticket_input_frame.pack(fill="x", padx=5, pady=5)
# Eingabefelder für Name und Flugauswahl
ttk.Label(ticket_input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = ttk.Entry(ticket_input_frame, width=20)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
ttk.Label(ticket_input_frame, text="Flug:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
flug_combobox = ttk.Combobox(ticket_input_frame, values=[], width=10, state="readonly")
flug_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
ticket_btn = ttk.Button(ticket_input_frame, text="Ticket ausstellen", command=ticket_kaufen_click)
ticket_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Labelframe für Liste der verkauften Tickets
ticket_list_frame = ttk.LabelFrame(frame_tickets, text="Verkaufte Tickets")
ticket_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
# Treeview für Tickets
ticket_columns = ("Name", "Flug")
ticket_tree = ttk.Treeview(ticket_list_frame, columns=ticket_columns, show="headings", height=8)
ticket_tree.heading("Name", text="Name")
ticket_tree.heading("Flug", text="Flug")
ticket_tree.pack(fill="both", expand=True)
# (Falls viele Tickets zu erwarten, kann hier auch eine Scrollbar hinzugefügt werden)

# Initiale Daten in den Anzeigen laden
aktualisiere_flugliste()
aktualisiere_gateliste()
aktualisiere_flug_options()
# Bereits gespeicherte Tickets anzeigen
for ticket in sim.ticket_manager.tickets:
    ticket_tree.insert("", "end", values=(ticket.name, ticket.flugnummer))

# Hauptloop starten
root.mainloop()
