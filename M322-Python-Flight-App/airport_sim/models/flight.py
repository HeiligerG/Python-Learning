from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Flight:
    id: str
    airline: str
    origin: str
    dest: str
    status: str = "En Route"          # En Route | Delay | At Gate | Boarding | Crash | Maintenance
    gate: Optional[int] = None
    wear: int = 0                     # 0 – 100 %, steigt pro Umlauf
    delay_reason: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)