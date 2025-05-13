# Teil 1 — Architektur‑Überblick

## 1.1 Komponenten & Schichten

| Ebene          | Datei/Ordner                       | Aufgabe                                               |
|----------------|------------------------------------|-------------------------------------------------------|
| **GUI**        | `views/mainwindow.py`              | Qt‑Fenster, Layout, User‑Interaktionen                |
|                | `views/tablemodels.py`             | `QAbstractTableModel` + Farblogik                     |
| **Logik**      | `controllers/airport_sim.py`       | Simulations‑Engine, Timer, Zustands­übergänge         |
| **Domänen‑Daten** | `models/flight.py`, `models/ticket.py` | Dataclasses für Flüge & Tickets                       |

#### 1.1.1 Feingliederung der GUI‑Ebene

| Datei / Klasse                      | Zweck                                                                                            | Wichtige Methoden / Signale                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| **`views/mainwindow.MainWindow`**   | Root‑Fenster; erzeugt Layout (2 × 2‑Airport‑Grid, Ticket‑Tabelle, Counter‑Bar, Buttons, Slider). | `refresh_ui()` – zählt Status, aktualisiert Counter.                                          |
| **`views.tablemodels.FlightModel`** | Subklasse von `QAbstractTableModel`; stellt farbkodierte Flugzeilen bereit.                      |  `data()` – hinterlegt Hintergrundfarbe je Status.<br>`refresh()` – volles Reset nach Signal. |
| **`views.tablemodels.TicketModel`** | Table‑Model für Tickets; zieht Spalten dynamisch nach, sobald erste Tickets existieren.          |  `refresh()`                                                                                  |

> **Warum Table‑Models statt Widgets?**
>  Sie trennen Daten von Darstellung, erleichtern Sortier‑/Filter‑Proxies und minimieren Redraw‑Kosten.

---

#### 1.1.2 Feingliederung der Logik‑Ebene

| Abschnitt im Code        | Aufgabe                                                                                           | Typische Laufzeit                |
| ------------------------ | ------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Timer‑Loop (`_loop`)** | zentraler Scheduler; entscheidet pro Tick über Landen, Boarding, Crash, Ticket‑Verkauf.           | alle 800 ms (Standard)           |
| **`_land_attempt`**      | Gate‑Check, Status *At Gate* oder *Delay*.                                                        |  ≈ 400 ms nach En‑Route‑Eintritt |
| **`_depart`**            |  Boarding → En‑Route, erhöht Verschleiss, setzt nächstes Ziel.                                     |  2.5 s nach *Boarding*           |
| **Maintenance‑Workflow** | manuell via Button oder Auto‑Timer – Crash‑Flug wechselt zu *Maintenance*, verlässt sie nach 6 s. |  6 s                             |

---

#### 1.2 Erweiterter Datenfluss (mit Signalen & Proxies)

```
┌────────────┐       (1) QtTimer Tick
│    Qt      │ ───────────────────────────────────┐
└────────────┘                                      │
       │                                            │
       ▼                                            │
┌───────────────────────────────┐                   │
│ controllers/airport_sim._loop │                   │
└───────────────────────────────┘                   │
   │      │                     │                   │
   │      │                     │                   │
   │      ├── Status‑Update ➝ emit flights_changed ─┼─► FlightModel.refresh()
   │      │                                         │    ▲
   │      │                                         │    │ (Qt re‑paints views
   │      └── Ticket‑Erzeugung ➝ emit tickets_changed◄────┘      via proxies)
   │
   └─ `_after(...)` planen             (QtEventQueue)
```

---

#### 1.3 Thread‑Modell – Detail

| Aufgabe                         | Thread                              | Begründung                                     |
| ------------------------------- | ----------------------------------- | ---------------------------------------------- |
| GUI‑Rendering                   | Qt‑Main‑Thread                      | Qt‑Vorgabe.                                    |
| Simulation‑Timer                | ebenfalls Qt‑Main‑Thread (`QTimer`) | vermeidet Race‑Conditions, reicht für ≤ 60 Hz. |
| Schwergewichts‑Tasks (optional) | separat (z. B. `QThreadPool`)       | nur nötig bei > 10 000 Flügen.                 |

*Alle* Daten‑Mutationen passieren synchron → kein Locking / `QMutex` nötig.

---

#### 1.4 Zustandsmaschine (Flug)

| Von          | Ereignis                | Nach            | Kommentar                 |
| ------------ | ----------------------- | --------------- | ------------------------- |
| **En Route** | Gate frei               | **At Gate**     | Landeanflug ok            |
| En Route     | Gate belegt             | **Delay**       | roter Status              |
| Delay        | Gate frei               | **At Gate**     | erneuter Check jede 1.5 s |
| At Gate      | Timer 2.5 s             | **Boarding**    | Passagierwechsel          |
| Boarding     | Timer 0 s               | **En Route**    | Abflug, Verschleiss +5 %   |
| En Route     | Crash‑Bedingung erfüllt | **Crash**       | bleibt dunkelrot          |
| Crash        | Button / Auto‑Timer     | **Maintenance** | wear → 0 %, Gelb          |
| Maintenance  | Timer 6 s               | En Route        | zurück in Umlauf          |