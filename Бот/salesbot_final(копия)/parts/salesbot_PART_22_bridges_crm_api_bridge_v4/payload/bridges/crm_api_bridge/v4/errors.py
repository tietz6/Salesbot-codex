
class CRMError(Exception):
    def __init__(self, code: str, message: str, payload=None):
        super().__init__(message)
        self.code = code
        self.payload = payload

    def to_dict(self):
        return {"code": self.code, "message": str(self), "payload": self.payload}
