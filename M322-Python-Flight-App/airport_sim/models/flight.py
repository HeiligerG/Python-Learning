
from dataclasses import dataclass, asdict
from typing import Optional
@dataclass
class Flight:
    id:str
    airline:str
    origin:str
    dest:str
    status:str
    gate:Optional[int]
    delay_reason:Optional[str]=None
    def to_dict(self):return asdict(self)
