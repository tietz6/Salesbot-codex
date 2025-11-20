
from .utils import integration_result, retry

class SmsProvider:
    def send(self, phone: str, text: str):
        def _send():
            if not phone:
                raise Exception("Invalid phone")
            return integration_result(True, {"sent_to": phone, "text": text})
        return retry(_send)
