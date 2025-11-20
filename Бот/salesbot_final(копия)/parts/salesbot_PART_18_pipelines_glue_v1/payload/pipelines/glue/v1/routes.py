
from fastapi import APIRouter
from .orchestrator import Glue

router = APIRouter(prefix="/glue", tags=["glue"])
glue = Glue()

@router.post("/build_bundle")
async def build_bundle(song: bool=True, video: bool=False, premium: bool=False):
    return glue.build_bundle(song=song, video=video, premium=premium)

@router.post("/create_deal")
async def create_deal(title: str, amount: float, currency: str="KGS", phone: str|None=None, email: str|None=None, name: str|None=None):
    contact = {"phone": phone, "email": email, "name": name}
    return glue.create_deal(title=title, amount=amount, currency=currency, contact=contact)

@router.post("/buy_bundle")
async def buy_bundle(song: bool=True, video: bool=False, premium: bool=False, phone: str|None=None, email: str|None=None, name: str|None=None):
    contact = {"phone": phone, "email": email, "name": name}
    return glue.buy_bundle(song=song, video=video, premium=premium, contact=contact)

@router.get("/invoice_status/{invoice_id}")
async def invoice_status(invoice_id: str):
    return glue.invoice_status(invoice_id)
