
import typing as T
from .roles import Role
from .permissions import Permission, PERMISSIONS_BY_ROLE

def has_permission(role: Role|str, perm: Permission)->bool:
    key = role.name if isinstance(role, Role) else str(role).upper()
    allowed = PERMISSIONS_BY_ROLE.get(key, set())
    return perm in allowed

def require_permission(role: Role|str, perm: Permission):
    if not has_permission(role, perm):
        raise PermissionError(f"Permission denied: role={role} perm={perm}")

# Optional FastAPI/Starlette middleware
try:
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response
    class ACLMiddleware(BaseHTTPMiddleware):
        def __init__(self, app, get_role: T.Callable[[Request], T.Union[Role,str]]):
            super().__init__(app); self._get_role = get_role
        async def dispatch(self, request: Request, call_next):
            request.state.role = self._get_role(request)
            return await call_next(request)
except Exception:  # starlette not installed
    class ACLMiddleware:
        def __init__(self, app, get_role):
            self.app = app; self._get_role = get_role
        async def __call__(self, scope, receive, send):
            return await self.app(scope, receive, send)
