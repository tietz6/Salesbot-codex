
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

@dataclass
class ProductBundle:
    name: str
    items: List[Dict[str, Any]]
    base_price: float
    currency: str = "KGS"
    tags: List[str] = None
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return asdict(self)

# базовые цены в KGS
BASE_PRICES = {
    "song": 3500,
    "video_postcard": 5000,
    "premium_story": 8000,
}

def build_bundle(song: bool=True, video: bool=False, premium: bool=False)->ProductBundle:
    items = []
    price = 0

    if song:
        items.append({"type":"song","desc":"Personalized Song"})
        price += BASE_PRICES["song"]

    if video:
        items.append({"type":"video_postcard","desc":"AI Video Postcard"})
        price += BASE_PRICES["video_postcard"]

    if premium:
        items.append({"type":"premium_story","desc":"Premium Story"})
        price += BASE_PRICES["premium_story"]

    parts = []
    if song: parts.append("Song")
    if video: parts.append("Video")
    if premium: parts.append("Premium")
    name = "Bundle: " + (" + ".join(parts) if parts else "Empty")

    return ProductBundle(name=name, items=items, base_price=price, meta={"version":"v1_quality"})

def build_custom(name: str, items: List[Dict[str, Any]], base_price: float, currency: str="KGS", tags: List[str]|None=None, meta: Dict[str, Any]|None=None)->ProductBundle:
    return ProductBundle(name=name, items=items, base_price=float(base_price), currency=currency, tags=tags or [], meta=meta or {})
