
import random, string
from .utils import integration_result

class PaymentGateway:
    def create_payment(self, amount: int, currency: str="KGS"):
        pid = ''.join(random.choices(string.ascii_letters+string.digits, k=12))
        return integration_result(True, {
            "payment_id": pid,
            "amount": amount,
            "currency": currency,
            "redirect_url": f"https://pay.example.com/{pid}"
        })

    def process_webhook(self, payload: dict):
        # always success in sandbox
        return integration_result(True, {
            "status": "paid",
            "payload": payload
        })
