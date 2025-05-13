## Airport Simulation

### Inhaltsverzeichnis

- [Airport Simulation](#airportsimulation)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Überblick](#überblick)
  - [Hauptfunktionen](#hauptfunktionen)
  - [Schnellstart](#schnellstart)
  - [Konfiguration](#konfiguration)
  - [Projektstruktur](#projektstruktur)
  - [Erweiterungsmöglichkeiten](#erweiterungsmöglichkeiten)
  - [Beitragen](#beitragen)
  - [Kontakt](#kontakt)

---

### Überblick

Dieses Desktop‑Projekt entstand als **Schulprojekt** im Modul *Software Engineering* und wurde komplett in **Python 3.10+** mit **PySide6** umgesetzt.

Vier Flughäfen (ZRH | FRA | LHR | CDG) teilen sich eine feste Flotte von Flugzeugen.
Das Dashboard zeigt Live‑Status der Flüge, aktuelle Ticketverkäufe sowie Zähler für En‑Route, Delay, Boarding, Maintenance und Crash.

**[Docs](/M322-Python-Flight-App/admin/airport_sim_docs/01_architektur.md)**
**[Szenario](/M322-Python-Flight-App/admin/Szenario_airport_sim.md)**

---

### Hauptfunktionen

| Bereich                | Details                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| **Fixe Flotte**        | Standardmässig 30 Flugzeuge, die dauerhaft im Ring fliegen.                                       |
| **Gate‑Logik**         | 4 Gates pro Flughafen. Fehlen freie Gates, wechselt der Flug auf *Delay*.                        |
| **Verschleiss & Crash** | Jeder Flug erhöht den Verschleiss (+5 %). Crash‑Chance = Basis + Verschleissfaktor.                |
| **Maintenance**        | Crashes werden per Button in *Maintenance* verschoben, Verschleiss wird dort auf 0 % gesetzt.     |
| **Tickets**            | 1–6 Tickets pro Tick, sofortige Anzeige in der Ticket‑Tabelle.                                   |
| **Status‑Zähler**      | Kopfzeile aggregiert alle Flugzustände live.                                                     |
| **Benutzersteuerung**  | Tempo‑Slider (1 / 16 × bis 64 ×) und Button „Send Crashes → Maintenance“.                        |
| **Farben**             | Orange En Route · Rot Delay · Grün At Gate · Blau Boarding · Gelb Maintenance · Dunkelrot Crash. |

---

### Schnellstart

```bash
# Repository klonen oder ZIP entpacken
cd airport_sim

# Virtuelle Umgebung
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Abhängigkeiten
pip install --upgrade pip
pip install PySide6

# Starten
python app.py
```

Das Dashboard öffnet im Maximized‑Modus.
Der Tempo‑Slider befindet sich unten, der Wartungs‑Button oben rechts.

---

### Konfiguration

Alle zentralen Parameter findest du oben in **`controllers/airport_sim.py`**.

| Konstante         | Beschreibung                            | Default         |
| ----------------- | --------------------------------------- | --------------- |
| `GATES_PER_AP`    | Gates pro Flughafen                     | `4`             |
| `FLEET_SIZE`      | Anzahl Flugzeuge                        | `30`            |
| `CRASH_BASE_PROB` | Basis‑Crash‑Risiko pro Tick             | `0.03`          |
| Verschleiss‑Faktor | `wear / divisor` in der Crash‑Bedingung | `divisor = 200` |
| `TICK_MS`         | Dauer eines Sim‑Ticks                   | `800` ms        |

Farben kannst du in **`views/tablemodels.py`** (`COLOR`‑Dict) ändern.

---

### Projektstruktur

```
airport_sim/
├─ app.py                 # Einstiegspunkt
├─ models/
│  ├─ flight.py           # Flug‑Dataclass
│  └─ ticket.py           # Ticket‑Dataclass
├─ controllers/
│  └─ airport_sim.py      # Sim‑Engine und Timer
├─ views/
│  ├─ tablemodels.py      # Qt‑Modelle + Farben
│  └─ mainwindow.py       # GUI‑Layout
└─ resources/
   └─ state.json          # Platzhalter (aktuell nicht verwendet)
```

---

### Erweiterungsmöglichkeiten

| Idee              | Anknüpfungspunkt                                                                          |
| ----------------- | ----------------------------------------------------------------------------------------- |
| Weitere Flughäfen | `AIRPORTS`‑Liste erweitern, ggf. `GATES_PER_AP` anpassen.                                 |
| Treibstoff‑System | Attribut `fuel` in `Flight` ergänzen, Verbrauch pro Umlauf senken, Tanken in Maintenance. |
| Datenspeicherung  | `AirportSim` beim Beenden Flotte & Tickets nach JSON schreiben.                           |
| Statistiken       | In einem separaten Fenster matplotlib‑Plots zu Delays oder Crash‑Raten anzeigen.          |
| Unit‑Tests        | `pytest` verwenden, Qt‑Timer mit `QTest.qWait` mocken.                                    |

---

### Beitragen

Wir freuen uns über Beiträge der Community!

1. **Fork** das Repository

   ```bash
   git fork https://github.com/username/WebDevTools.git
   ```

2. **Feature oder Fix erstellen**

   ```bash
   git checkout -b feature/<DeinFeature>
   # Änderungen vornehmen …
   git commit -m "Neues Feature: <DeinFeature>"
   ```

3. **Push**

   ```bash
   git push origin feature/<DeinFeature>
   ```

4. **Pull‑Request** eröffnen und kurze Beschreibung der Änderungen angeben.

---

### Kontakt

* **Autor:** HolyG
* **E‑Mail:** [devholyg@gmail.com](mailto:devholyg@gmail.com)

Fragen, Vorschläge oder Feedback sind jederzeit willkommen!