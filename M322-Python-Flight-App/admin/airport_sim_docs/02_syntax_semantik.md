# Ergänzung zu **Teil 2 — Syntaktik & Semantik**

## 2.1 Dataclasses vs. QObject

| Aspekt         | `dataclass`‑Objekt                    | `QObject`‑basiert                         |
| -------------- | ------------------------------------- | ----------------------------------------- |
| Boilerplate    | minimal (`@dataclass` + Felder)       | Konstruktor + Getter/Setter + Signals     |
| Serialisierung | ein Zeile → `json.dumps(asdict(obj))` | eigenes `to_dict()` oder `QJson*` nötig   |
| Qt‑Signale     | nicht direkt verfügbar (bewusst)      | integriert (`pyqtSignal`, `Signal`)       |
| Mutierbarkeit  | frei mutierbar (kein Notify)          | Properties können Change‑Signale auslösen |
| Performance    | reine Python‑Objekte, schnell         | geringfügiger Overhead durch Meta‑Klasse  |

Für unser Modell reichen Dataclasses:
*Änderungen* am Flug werden **zentral** durch das Engine‑Signal
`flights_changed` kommuniziert, keine Einzel‑Signals je Instanz nötig.

---

## 2.2 Typanmerkungen – Best Practice

* Verwende `Optional[str]` statt `str | None`, wenn du noch <= Python 3.9
  unterstützen willst.
* Nutze **Unions nur sparsam** – sie erschweren MyPy‑Inferenz.
* Public‑Attribute: `snake_case`, Konstanten: `UPPER_SNAKE`.
* Private Helfer mit `_`: `_after(self, ms: int, fn: Callable[[], None])`.

Beispiel – klarer Funktions‑Header:

```python
def _land_attempt(self, flight: Flight) -> None:
    ...
```

---

## 2.3 Crash‑Formel detailliert

```python
p_crash = CRASH_BASE_PROB + wear / divisor
```

| Variable          | Einheit | Beschreibung                                               |
| ----------------- | ------- | ---------------------------------------------------------- |
| `CRASH_BASE_PROB` | 0–1     | Grundrisiko pro Tick (z. B. 0.03)                          |
| `wear`            | %       | Verschleiss­grad 0–100                                      |
| `divisor`         | int     | Dämpfungs­faktor (je grösser, desto geringer Zusatz­risiko) |

### Rechenbeispiel

| wear | Basis | Zusatz             | Gesamt‑Risiko |
| ---- | ----- | ------------------ | ------------- |
| 20 % | 0.03  | 0.20 / 200 = 0.001 | **0.031**     |
| 80 % | 0.03  | 0.80 / 200 = 0.004 | **0.034**     |

Die Funktion steigt **linear** mit `wear`.
Willst du stärker ansteigendes Risiko, ersetze den linearen Anteil
durch eine *quadratische* Komponente:

```python
p_crash = CRASH_BASE_PROB + (wear / 100) ** 2 * 0.02
```

Dann ergibt wear = 80 % ≈ 0.03 + 0.64 × 0.02 = 0.0428 → merklich höher.

---

## 2.4 Status‑Enum statt Strings (optional)

Um Tippfehler zu vermeiden, kannst du `Enum` nutzen:

```python
from enum import Enum, auto

class FStatus(str, Enum):
    EN_ROUTE   = "En Route"
    DELAY      = "Delay"
    AT_GATE    = "At Gate"
    BOARDING   = "Boarding"
    CRASH      = "Crash"
    MAINTENANCE= "Maintenance"
```

Dataclass‑Attribut:

```python
status: FStatus = FStatus.EN_ROUTE
```

Vorteil: MyPy meldet, wenn du `status=="Enroute"` (ohne Leerzeichen)
schreibst; Nachteil: JSON‑Dump muss `status.value` verwenden.