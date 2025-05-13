# Teil 4 — Tests, Deployment, Roadmap (ausführlich)

---

## 4.1 Tests

### 4.1.1 Struktur

| Test‑Ebene     | Typisches Ziel                                       | Tooling                               | Beispiel‑Datei         |
| -------------- | ---------------------------------------------------- | ------------------------------------- | ---------------------- |
| **Unit**       | Pure Business‑Logik (Zustände, Wahrscheinlichkeiten) | `pytest`, `hypothesis`                | `tests/test_engine.py` |
| **GUI**        | Widgets, Buttons, Signal‑Slots                       | `pytest‑qt`, `qtbot`‑Fixture          | `tests/test_gui.py`    |
| **End‑to‑End** | App als Black‑Box, Timer‑Ticks beschleunigt          | `pytest`, `pytest‑qt` + `QTest.qWait` | `tests/test_e2e.py`    |

### 4.1.2 Beispiel Unit‑Test

```python
@pytest.mark.parametrize("wear,expected", [(0, False), (90, True)])
def test_crash_probability(wear, expected):
    sim = AirportSim(Path("/dev/null"))
    f = sim.flights[0]; f.wear = wear

    crashed = False
    for _ in range(10_000):          # Monte‑Carlo
        if random.random() < (CRASH_BASE_PROB + wear / DIVISOR_WEAR):
            crashed = True
            break
    assert crashed is expected
```

### 4.1.3 Beispiel GUI‑Test

```python
def test_maintenance_button(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    # Crash erzwingen
    f = window.sim.flights[0]; f.status = "Crash"
    window.refresh_ui()

    # Klick auf Button
    qtbot.mouseClick(window.findChild(QPushButton), Qt.LeftButton)
    qtbot.wait(50)

    assert f.status == "Maintenance"
```

*`qtbot.wait(50)` reicht, weil Button‑Slot synchron läuft.*

---

## 4.2 Deployment

| Zielplattform         | Vorgehen                                   | Besonderheiten            |
| --------------------- | ------------------------------------------ | ------------------------- |
| **Windows (.exe)**    | `pyinstaller --onefile --noconsole app.py` | Icons via `--icon=`       |
| **macOS (.app)**      | `pyinstaller --onefile --windowed app.py`  | notarization nötig        |
| **Linux (.AppImage)** | `appimagetool` nach PyInstaller‑Build      | LibQt5/6 static verlinken |

**Docker Headless Test**

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y libgl1
COPY . /sim
WORKDIR /sim
RUN pip install PySide6 pytest
CMD ["pytest", "-q"]
```

Für CI‑Pipelines, in GitHub‑Action:

```yaml
- name: Run Tests
  run: docker build -t sim-test . && docker run sim-test
```

---

## 4.3 Roadmap

| Phase   | Feature                              | Nutzen                       | Status       |
| ------- | ------------------------------------ | ---------------------------- | ------------ |
| **v10** | JSON‑Persistenz (Autosave beim Quit) | Spielstand laden/fortsetzen  | geplant      |
|         | REST‑API (FastAPI)                   | Remote‑Dashboard, Mobile‑App | POC          |
|         | Animated Map (QGraphicsView)         | Visuelle Flugpfade           | in Recherche |
| **v11** | Multi‑Thread Simulation              | > 500 Flüge ohne UI‑Lag      | noch offen   |
|         | Live Metrics Prometheus Export       | DevOps‑Monitoring            | Idee         |

> *Hinweis*: jede Roadmap‑Spalte ist ein GitHub‑Issue mit Milestone‑Tag – so bleibt der Fortschritt transparent.

---

### 4.4 Best Practices

* **Red+Green‑Refactor**: erst Test fehlschlagen lassen, dann fixen.
* **Fixture‑Factories** für `AirportSim` mit custom Parametern (`fleet_size`, `gates` …).
* **Coverage > 90 %** für Business‑Logik, GUI‑Teile ≥ 50 % reichen oft.
* **Semantic Versioning**: vX.Y.Z (Major = Breaking, Minor = Feature, Patch = Bugfix).

Damit ist Teil 4 jetzt praxisnah ausgebaut – Testszenarien, CI‑Indikation, Deployment‑Rezepte und eine konkrete Roadmap.
