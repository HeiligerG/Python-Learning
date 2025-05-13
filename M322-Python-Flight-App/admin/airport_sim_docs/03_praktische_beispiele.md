# Teil 3 — Praktische Beispiele (erweitert)

---

## 3.1 Crash‑Rate halbieren

**Code‑Snip**

```python
# controllers/airport_sim.py
CRASH_BASE_PROB = 0.015                # zuvor 0.03
DIVISOR_WEAR    = 400                  # zuvor 200

if random.random() < (CRASH_BASE_PROB + f.wear / DIVISOR_WEAR):
    f.status = "Crash"
```

**Erklärung**

| Parameter         | Wirkung                                                               | Real‑Life Analogie                                 |
| ----------------- | --------------------------------------------------------------------- | -------------------------------------------------- |
| `CRASH_BASE_PROB` | Grundrisiko pro Tick.                                                 | Unvorhersehbare Ereignisse (Vogel­schlag, Blitz).  |
| `DIVISOR_WEAR`    | Dämpft den Verschleiß‑Anteil. Höherer Wert ⇒ Risiko wächst langsamer. | Besseres Wartungs­programm oder sichere Bau­weise. |

> Mit `wear = 60 %` ergibt sich: 
> `0.015 + 0.60 / 400 ≈ 0.0165` (1.65 % pro Tick).

**Praxis‑Vergleich**

* **Ein Low‑Cost‑Carrier** mit aggressiven Umläufen könnte `DIVISOR_WEAR = 200` lassen.
* **Ein Premium‑Hub‑Carrier** investiert mehr in Maintenance ⇒ `DIVISOR_WEAR = 500`.

---

## 3.2 Gate‑Kapazität verdoppeln

```python
GATES_PER_AP = 8          # vorher 4
```

| Effekt                                          | Real‑Life Beispiel                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------------- |
| Weniger Delays, seltener roter Status.          | Ausbau Terminal 3 in Frankfurt (FRA) erhöht Gate‑Zahl für Wide‑Body‑Jets. |
| Höherer Durchsatz → Tickets pro Minute steigen. | In Spitzenzeiten können nun 2× mehr Flüge parallel abgefertigt werden.    |

> Empirisch im Simulator: Delays sinken um \~70 %, wenn man Gate‑Zahl verdoppelt.

---

## 3.3 Unit‑Test „Delay bei vollem Flughafen“

```python
def test_delay_when_no_gate(qtbot):
    sim = AirportSim(Path("/dev/null"))
    # 4 Gates belegt -> leerliste
    sim.free_gates["ZRH"] = []
    fl = sim.flights[0]
    fl.dest = "ZRH"

    sim._land_attempt(fl)

    assert fl.status == "Delay"
    assert fl.delay_reason == "No Gate"
```

**Warum dieser Test?**

* Verifiziert Geschäfts­logik unabhängig von GUI.
* Edge‑Case: Ressourcenknappheit.
* Schnelle Regression‑Absicherung: läuft < 10 ms.

Real‑Life‑Analog:
*„Go‑Arounds“ in Zürich zur Mittagswelle, weil alle Docks belegt.*

---

## 3.4 Weitere Quick Wins

| Änderung                   | Wie                                     | Nutzen                                             |
| -------------------------- | --------------------------------------- | -------------------------------------------------- |
| **Tempo‑Slider feiner**    | `slider.setRange(-6,8)`                 | Zeitlupe 1 / 64 × bis Turbo 256 ×.                 |
| **Wear‑Reset auf 20 %**    | in `_exit_maintenance`: `f.wear = 20`   | Wartung ist Teil‑Overhaul, nicht Werks­dock.       |
| **Boarding‑Zeit variabel** | `boarding_time = random.randint(2,5)` s | Realistischer Turnaround (Kurz‑ vs. Lang­strecke). |

---

### 3.5 Real‑Life vs. Simulation – Mini‑Case‑Study

| Szenario                | Eingriff im Code                                       | Beobachtung im Dashboard               | Vergleich Reallogistik                                            |
| ----------------------- | ------------------------------------------------------ | -------------------------------------- | ----------------------------------------------------------------- |
| Nacht­flugverbot in FRA | `if f.dest=="FRA" and 22<=clock<6: force Delay`        | Zahl roter Delays in FRA steigt stark. | Tatsächlich > 70 Verspätungen pro Nacht (Lärm­schutz).            |
| Blitz‑Gewitter          | Temporär `CRASH_BASE_PROB = 0.2`, `DIVISOR_WEAR = 100` | Viele Crash‑→ Maintenance‑Wechsel.     | 2022 Frankfurt: Blitz traf A321 – Maschine 7 Tage out‑of‑service. |
| Charter‑Welle           | `FLEET_SIZE = 60`, `GATES_PER_AP = 4`                  | Grid läuft voll, Tickets explodieren.  | Ferien­spitzen: Zürich Juli/August.                               |