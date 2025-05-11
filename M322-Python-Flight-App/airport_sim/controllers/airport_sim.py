from __future__ import annotations
import random, itertools
from pathlib import Path
from collections import Counter
from PySide6 import QtCore
from models.flight import Flight
from models.ticket import Ticket

AIRPORTS        = ["ZRH", "FRA", "LHR", "CDG"]
GATES_PER_AP    = 4
FLEET_SIZE      = 30                 # fixe Anzahl Flugzeuge
SPAWN_PROB      = 0.00               # keine neuen Flieger – fixe Flotte
CRASH_BASE_PROB = 0.005              # Grundwahrscheinlichkeit pro Tick
TICK_MS         = 800                # Sim‑Tick in ms

class AirportSim(QtCore.QObject):
    flights_changed = QtCore.Signal()
    tickets_changed = QtCore.Signal()

    def __init__(self, path: Path):
        super().__init__()
        self.flights: list[Flight] = []
        self.tickets: list[Ticket] = []
        self.free_gates = {ap: list(range(1, GATES_PER_AP + 1)) for ap in AIRPORTS}
        self._fid = itertools.count(1)
        self._tid = itertools.count(1)
        self._speed = 1.0

        self._spawn_initial_fleet()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._loop)
        self.timer.start(TICK_MS)

    # ---------- public ----------
    def set_speed(self, factor: float):
        self._speed = max(0.05, factor)

    def handle_crashes(self):
        """Crash‑Flieger in Maintenance überführen."""
        changed = False
        for f in self.flights:
            if f.status == "Crash":
                f.status = "Maintenance"
                f.wear = 0
                # auf Gate stellen, falls frei
                if self.free_gates[f.dest]:
                    f.gate = self.free_gates[f.dest].pop(0)
                changed = True
        if changed:
            self.flights_changed.emit()

    def count_by_status(self):
        return Counter(f.status for f in self.flights)

    # ---------- intern ----------
    def _after(self, ms: int, fn):
        QtCore.QTimer.singleShot(int(ms / self._speed), fn)

    def _spawn_initial_fleet(self):
        while len(self.flights) < FLEET_SIZE:
            origin, dest = random.sample(AIRPORTS, 2)
            fid = f"FL{next(self._fid):04d}"
            fl = Flight(id=fid,
                        airline=random.choice(["LH", "BA", "AF", "LX", "DL"]),
                        origin=origin,
                        dest=dest)
            self.flights.append(fl)
        self.flights_changed.emit()

    # ---------- loop ----------
    def _loop(self):
        # Crash‑check und Bewegungen
        for f in list(self.flights):
            if f.status == "En Route":
                # Crash‑Chance steigt mit Verschleiss
                if random.random() < (CRASH_BASE_PROB + f.wear / 800):
                    f.status = "Crash"
                    self.flights_changed.emit()
                    continue
                self._after(400, lambda f=f: self._land_attempt(f))

            elif f.status == "At Gate":
                f.status = "Boarding"
                self.flights_changed.emit()
                self._after(2500, lambda f=f: self._depart(f))

            elif f.status == "Delay":
                self._after(1500, lambda f=f: self._land_attempt(f))

            elif f.status == "Maintenance":
                # nach 6 s zurück in En Route
                self._after(6000, lambda f=f: self._exit_maintenance(f))

        # Tickets verkaufen
        if self.flights and random.random() < 0.9:
            self._sell_tickets_batch()

    # ---------- actions ----------
    def _land_attempt(self, f: Flight):
        if f.status not in ("En Route", "Delay"):
            return
        gates = self.free_gates[f.dest]
        if gates:
            f.gate = gates.pop(0)
            f.status = "At Gate"
            f.delay_reason = None
        else:
            f.status = "Delay"
            f.delay_reason = "No Gate"
        self.flights_changed.emit()

    def _depart(self, f: Flight):
        if f.status != "Boarding":
            return
        # Gate frei machen
        if f.gate is not None:
            self.free_gates[f.dest].append(f.gate)
            self.free_gates[f.dest].sort()
            f.gate = None
        # Verschleiss erhöhen
        f.wear = min(100, f.wear + 5)
        # Nächster Flughafen im Ring
        next_idx = (AIRPORTS.index(f.dest) + 1) % len(AIRPORTS)
        f.origin, f.dest = f.dest, AIRPORTS[next_idx]
        f.status = "En Route"
        self.flights_changed.emit()

    def _exit_maintenance(self, f: Flight):
        if f.status != "Maintenance":
            return
        # Gate frei geben
        if f.gate is not None:
            self.free_gates[f.dest].append(f.gate)
            self.free_gates[f.dest].sort()
            f.gate = None
        f.status = "En Route"
        self.flights_changed.emit()

    def _sell_tickets_batch(self):
        active = [fl for fl in self.flights if fl.status in ("En Route", "At Gate", "Boarding")]
        for _ in range(random.randint(1, 5)):
            fl = random.choice(active)
            self.tickets.append(Ticket(
                id=next(self._tid),
                passenger=random.choice(["Ada", "Ben", "Cora", "Dan", "Eva", "Finn", "Gina"]),
                flight=fl.id,
                seat=f"{random.randint(1, 30)}{random.choice('ABCDEF')}"
            ))
        self.tickets_changed.emit()
