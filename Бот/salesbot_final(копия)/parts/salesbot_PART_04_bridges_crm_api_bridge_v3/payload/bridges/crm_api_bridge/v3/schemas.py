
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List

def to_json(o):
    if hasattr(o, "__dataclass_fields__"):
        return asdict(o)
    return o

@dataclass
class Contact:
    id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    extra: Dict[str, Any] = None

@dataclass
class Deal:
    id: Optional[str] = None
    title: str = ""
    amount: float = 0.0
    currency: str = "KGS"
    status: str = "new"
    contact_id: Optional[str] = None
    extra: Dict[str, Any] = None

@dataclass
class Note:
    id: Optional[str] = None
    deal_id: Optional[str] = None
    contact_id: Optional[str] = None
    text: str = ""
    extra: Dict[str, Any] = None
