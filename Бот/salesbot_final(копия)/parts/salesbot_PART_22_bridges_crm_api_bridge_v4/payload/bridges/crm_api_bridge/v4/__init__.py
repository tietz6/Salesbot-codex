
from .client import CRMClientV4 as CRMClient
from .auth import CRMAuth
from .schemas import Contact, Deal, Note
from .errors import CRMError
__all__ = ["CRMClient","CRMAuth","Contact","Deal","Note","CRMError"]
