"""Middleware for IP restriction and auth dependency."""
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from .core.auth import get_auth

LOCAL_IPS = {"127.0.0.1", "::1", "localhost"}
PROTECTED_PREFIXES = ("/api/auth", "/api/settings", "/api/admin")

security = HTTPBearer(auto_error=False)


class LocalOnlyMiddleware(BaseHTTPMiddleware):
    """Restrict access to protected routes to localhost only."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in PROTECTED_PREFIXES):
            client_host = (
                request.headers.get("x-forwarded-for", "").split(",")[0].strip()
                or request.client.host
                if request.client
                else ""
            )
            if client_host not in LOCAL_IPS:
                raise HTTPException(status_code=403, detail="Access restricted to localhost")
        return await call_next(request)


async def auth_required(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """FastAPI dependency — validates Bearer token, returns username."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    token = credentials.credentials
    auth = get_auth()
    if not auth.verify_session(token):
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    username = auth.iter_session(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return username
