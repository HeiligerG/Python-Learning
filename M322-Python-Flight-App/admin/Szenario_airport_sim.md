## Demo‑Szenario (Version v10) – alle Funktionen in Aktion

> **Ziel:** Man erlebt jeden Code‑Baustein live und versteht, wie
> Flug‑Wear, Gate‑Engpässe, Ticketverkauf, Crash‑→ Maintenance‑Workflow und GUI‑Steuerung zusammen­spielen.

| Schritt | Aktion in der GUI                                                                   | Erw. Ergebnis / geprüfte Funktion                                                                       | Gedeckte Bereiche                   |
| ------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| **0**   | **Programm starten**                                                                | • 30 orange „En Route“-Flüge (Start‑Fleet)<br>• 4 Gates pro Airport, alle frei<br>• Ticket‑Tabelle leer | Laden, Timer, fixed Fleet           |
| **1**   | Tempo‑Slider → **64 ×**                                                             | Ticks rasen, Tickets füllen Tabelle                                                                     | Speed‑Control, Ticket‑Model‑Refresh |
| **2**   | Warten bis **ZRH** alle 4 Gates belegt                                              | Nächster ZRH‑Flug wird rot „Delay“                                                                      | Delay‑Logik, Gate‑Check             |
| **3**   | Tempo auf **8 ×** drosseln                                                          | Boarding‑Flüge wechseln von Grün→Blau                                                                   | Boarding‑Timer                      |
| **4**   | Crash abwarten (dunkelrot „Crash“)                                                  | Crash‑Zähler (Counter) +1                                                                               | Wear‑basierte Crash‑Formel          |
| **5**   | **Button „Send Crashes → Maintenance“** klicken                                     | Crash‑Zeilen gelb „Maintenance“, Wear → 0 %                                                             | Button‑Signal, Maintenance‑Status   |
| **6**   | 6 s beobachten                                                                      | Gelber Flug wird wieder Orange (En Route), Gate frei                                                    | Maintenance‑Timer, Gate‑Freigabe    |
| **7**   | In Ticket‑Tabelle neueste Zeile anklicken                                           | Flug‑ID stimmt mit En‑Route‑Flug überein                                                                | Ticket‑Verkauf / Datenbindung       |
| **8**   | **Tempo ← Zeitlupe 1 / 16 ×**                                                       | Liste scrollt langsam → klar erkennbar                                                                  | Slider‑Min‑Grenze                   |
| **9**   | In `controllers/airport_sim.py` **`GATES_PER_AP = 2`**, App neu starten             | Flut roter Delays; Lernende sehen Infrastruktur‑Limit                                                   | Param‑Tuning, Gate‑Kapazität        |
| **10**  | In gleicher Datei **`CRASH_BASE_PROB = 0.005`** & `DIVISOR_WEAR = 500`, App restart | Crashes werden selten (< 1 / Min), Monitoring im Counter                                                | Risiko‑Parametrisierung             |
| **11**  | **pytest tests/test\_delay\_when\_no\_gate.py** laufen lassen                       | Test *passed* – Delay‑Business‑Regel greift                                                             | Unit‑Test‑Anbindung                 |

---

### Kern‑Bausteine, die damit abgedeckt sind

* **Flüge dynamisch im Ring** (En Route ↔ At Gate ↔ Boarding)
* **Gate‑Belegung / ‑Freigabe** mit Delay‑Fallback
* **Verschleiss → Crash → Maintenance** inklusive Wear‑Reset
* **Ticketverkauf** & sofortige Tabellen‑Aktualisierung
* **Globale Counter** für alle Status
* **Benutzer‑Steuerung**: Tempo‑Slider, Crash‑Maintenance‑Button
* **Param‑Tuning** durch einfache Konstanten‑Änderung
* **Automatisierte Tests** mit `pytest` / `pytest‑qt`

---

### Mögliche Erweiterungen

| Aufgabe                         | Wo ändern                                                               | Effekt                                      |
| ------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| **Verspätungs­grund erweitern** | `_land_attempt()` → `f.delay_reason = "Weather"`                        | zusätzlicher Tooltip im Table‑Model         |
| **Mehr Gates/CDG**              | `GATES_PER_AP = 6`                                                      | Delay‑Rate sinkt, Boarding‑Durchsatz steigt |
| **Boarding‑Zähler je Flug**     | Attribut `tickets_sold` in `Flight`; beim Ticket‑Verkauf `+=1`          | Spalte im FlightModel anzeigen              |
| **Persistenz**                  | Am Ende von `AirportSim` `save_state()`→JSON; beim Start `load_state()` | Sim‑Fortsetzung nach App‑Restart            |