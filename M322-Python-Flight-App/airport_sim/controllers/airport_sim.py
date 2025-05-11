
from __future__ import annotations
import random, itertools
from pathlib import Path
from PySide6 import QtCore
from models.flight import Flight
from models.ticket import Ticket

AIRPORTS=["ZRH","FRA","LHR","CDG"]
GATES=4
SPAWN_PROB=0.8
CRASH_PROB=0.03
TICK_MS=800

class AirportSim(QtCore.QObject):
    flights_changed=QtCore.Signal()
    tickets_changed=QtCore.Signal()

    def __init__(self, path:Path):
        super().__init__()
        self.flights:list[Flight]=[]
        self.tickets:list[Ticket]=[]
        self.free_gates={ap:list(range(1,GATES+1)) for ap in AIRPORTS}
        self._fid=itertools.count(1); self._tid=itertools.count(1)
        self._speed=1.0
        for _ in range(10): self._spawn()
        self.timer=QtCore.QTimer(self); self.timer.timeout.connect(self._loop); self.timer.start(TICK_MS)

    # --- public ---
    def set_speed(self,f): self._speed=max(0.05,f)
    def remove_crashes(self):
        before=len(self.flights)
        self.flights=[f for f in self.flights if f.status!="Crash"]
        if len(self.flights)!=before: self.flights_changed.emit()

    # --- helpers ---
    def _after(self,ms,fn): QtCore.QTimer.singleShot(int(ms/self._speed),fn)

    # --- main loop ---
    def _loop(self):
        if random.random()<SPAWN_PROB: self._spawn()
        if self.flights and random.random()<CRASH_PROB:
            en=[f for f in self.flights if f.status=="En Route"]
            if en:
                victim=random.choice(en)
                victim.status="Crash"; self.flights_changed.emit()
                self._after(6000, lambda f=victim:self.remove_crashes())

        for f in list(self.flights):
            if f.status=="En Route":
                self._after(400, lambda f=f: self._land_attempt(f))
            elif f.status=="At Gate":
                f.status="Boarding"; self.flights_changed.emit()
                self._after(2500, lambda f=f: self._depart(f))
            elif f.status=="Delay":
                self._after(1500, lambda f=f: self._land_attempt(f))

        if self.flights and random.random()<0.9:
            self._sell_tickets()

    # --- actions---
    def _spawn(self):
        o,d=random.sample(AIRPORTS,2)
        fid=f"FL{next(self._fid):04d}"
        self.flights.append(Flight(id=fid,airline=random.choice(["LH","BA","AF","LX","DL"]),
                                   origin=o,dest=d,status="En Route",gate=None))
        self.flights_changed.emit()

    def _land_attempt(self,f:Flight):
        if f not in self.flights or f.status not in("En Route","Delay"): return
        gates=self.free_gates[f.dest]
        if gates:
            gate=gates.pop(0)
            f.gate=gate; f.status="At Gate"; f.delay_reason=None
        else:
            f.status="Delay"; f.delay_reason="No Gate"
        self.flights_changed.emit()

    def _depart(self,f:Flight):
        if f not in self.flights or f.status!="Boarding": return
        if f.gate: self.free_gates[f.dest].append(f.gate); self.free_gates[f.dest].sort()
        self.flights.remove(f); self.flights_changed.emit()

    def _sell_tickets(self):
        for _ in range(random.randint(1,6)):
            fl=random.choice(self.flights)
            self.tickets.append(
                Ticket(
                    id=next(self._tid),
                    passenger=random.choice(["Ada", "Ben", "Cora", "Dan", "Eva", "Finn", "Gina"]),
                    flight=fl.id,
                    seat=f"{random.randint(1,30)}{random.choice('ABCDEF')}"
                )
            )

        self.tickets_changed.emit()
       #print(len(self.tickets))

    def count_by_status(self):
        from collections import Counter
        return Counter(f.status for f in self.flights)
