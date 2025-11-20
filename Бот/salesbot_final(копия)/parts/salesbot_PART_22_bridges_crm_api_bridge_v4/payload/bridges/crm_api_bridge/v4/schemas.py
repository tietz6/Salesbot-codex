
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

def to_json(o):
    if hasattr(o, "__dataclass_fields__"):
        return asdict(o)
    return o

def _strip(s):
    if s is None: return None
    s = str(s).strip()
    return s or None

@dataclass
class Contact:
    id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    extra: Dict[str, Any] = None

    def validate(self):
        self.phone = _strip(self.phone)
        self.email = _strip(self.email)
        self.name = _strip(self.name)
        return self

@dataclass
class Deal:
    id: Optional[str] = None
    title: str = ""
    amount: float = 0.0
    currency: str = "KGS"
    status: str = "new"
    contact_id: Optional[str] = None
    extra: Dict[str, Any] = None

    def validate(self):
        self.title = _strip(self.title) or "Untitled"
        try:
            self.amount = float(self.amount or 0.0)
        except Exception:
            self.amount = 0.0
        self.currency = (self.currency or "KGS").upper()
        return self

@dataclass
class Note:
    id: Optional[str] = None
    deal_id: Optional[str] = None
    contact_id: Optional[str] = None
    text: str = ""
    extra: Dict[str, Any] = None

    def validate(self):
        self.text = _strip(self.text) or ""
        return self
