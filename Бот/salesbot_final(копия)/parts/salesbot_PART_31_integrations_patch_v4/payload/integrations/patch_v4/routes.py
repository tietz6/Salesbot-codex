
from fastapi import APIRouter, Request
from .payment_gateway import PaymentGateway
from .sms_provider import SmsProvider
from .email_provider import EmailProvider
from .external_api import ExternalAPI

router = APIRouter(prefix="/integrations/v4", tags=["integrations_v4"])

pg = PaymentGateway()
sms = SmsProvider()
email = EmailProvider()
ext = ExternalAPI()

@router.post("/payment/create")
async def create_payment(req: Request):
    data = await req.json()
    amount = data.get("amount", 0)
    currency = data.get("currency", "KGS")
    return pg.create_payment(amount, currency)

@router.post("/payment/webhook")
async def payment_webhook(req: Request):
    data = await req.json()
    return pg.process_webhook(data)

@router.post("/sms/send")
async def sms_send(req: Request):
    data = await req.json()
    return sms.send(data.get("phone"), data.get("text"))

@router.post("/email/send")
async def email_send(req: Request):
    data = await req.json()
    return email.send(data.get("email"), data.get("subject",""), data.get("body",""))

@router.post("/ext/fetch")
async def ext_fetch(req: Request):
    data = await req.json()
    return ext.fetch(data.get("url",""), data.get("params"))
