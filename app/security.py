"""
Security dependencies for the FastAPI layer.

- API key auth: simple, explicit, no framework magic. Swap for OAuth2/JWT
  if this ever sits behind real user accounts instead of service-to-service
  calls.
- Rate limiting: per-IP, sliding window, in-memory. Fine for a single
  instance / demo; swap for Redis-backed limiting (e.g. slowapi + redis)
  before running more than one process.
"""
import hmac
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader

from app.config import settings

_request_log: dict[str, deque] = defaultdict(deque)

# Registering auth this way (instead of a plain Header param) makes FastAPI
# publish it as a named security scheme in the OpenAPI schema — that's what
# makes Swagger UI render a single global "Authorize" button instead of a
# per-endpoint header field.
_api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(x_api_key: str = Security(_api_key_scheme)) -> None:
    """Constant-time comparison to avoid timing side-channel leaks."""
    if not x_api_key or not hmac.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key. Set the X-API-Key header.",
        )


def rate_limit(request: Request) -> None:
    client_id = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - 60
    log = _request_log[client_id]

    while log and log[0] < window_start:
        log.popleft()

    if len(log) >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} requests/minute.",
        )

    log.append(now)