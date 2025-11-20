
from .utils import integration_result

class EmailProvider:
    def send(self, email: str, subject: str, body: str):
        if "@" not in email:
            return integration_result(False, error="Invalid email")
        return integration_result(True, {
            "subject": subject,
            "body": body,
            "address": email
        })
