
from enum import Enum, auto
class Permission(Enum):
    VIEW_DASHBOARD = auto()
    EDIT_CLIENT = auto()
    RUN_EXAM = auto()
    CONFIGURE_SYSTEM = auto()
    VIEW_PAYMENTS = auto()
    TAKE_CALL = auto()

PERMISSIONS_BY_ROLE = {
    "ADMIN": {p for p in Permission},
    "MANAGER": {Permission.VIEW_DASHBOARD, Permission.EDIT_CLIENT, Permission.VIEW_PAYMENTS, Permission.TAKE_CALL, Permission.RUN_EXAM},
    "TRAINEE": {Permission.VIEW_DASHBOARD, Permission.TAKE_CALL},
}
