
from dataclasses import dataclass, asdict
@dataclass
class Ticket:
    id:int
    passenger:str
    flight:str
    seat:str
    def to_dict(self): return asdict(self)
