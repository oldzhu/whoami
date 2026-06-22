"""Simple in-memory rate limiter."""
import time
from collections import defaultdict
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._clients: dict[str, list[float]] = defaultdict(list)

    def _cleanup(self, key: str, now: float):
        self._clients[key] = [t for t in self._clients[key] if now - t < self.window]

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        self._cleanup(key, now)
        if len(self._clients[key]) >= self.max_requests:
            return False
        self._clients[key].append(now)
        return True


limiter = RateLimiter(max_requests=30, window_seconds=60)


async def rate_limit_middleware(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not limiter.is_allowed(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
