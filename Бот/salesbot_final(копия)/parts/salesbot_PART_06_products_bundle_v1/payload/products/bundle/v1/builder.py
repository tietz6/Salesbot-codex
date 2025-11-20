
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class ProductBundle:
    name: str
    items: List[Dict[str, Any]]
    base_price: float
    currency: str = "KGS"
    tags: List[str] = None

    def to_dict(self):
        return asdict(self)

# Example rules — can be extended
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

    name = "Bundle: "
    parts = []
    if song: parts.append("Song")
    if video: parts.append("Video")
    if premium: parts.append("Premium")
    name += " + ".join(parts) if parts else "Empty"

    return ProductBundle(name=name, items=items, base_price=price)
