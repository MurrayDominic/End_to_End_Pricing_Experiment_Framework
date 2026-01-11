from dataclasses import dataclass
from typing import Optional

@dataclass
class PolicyRecord:
    age: int
    tenure: float
    ncd: int
    region: str
    base_risk: float
    premium: Optional[float] = None
    burn_cost: Optional[float] = None