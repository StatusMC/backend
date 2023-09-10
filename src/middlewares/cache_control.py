"""Set ``Cache-Control`` header to 5 minutes."""
from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

import src.config


class CacheControlMiddleware(BaseHTTPMiddleware):
    """Set Cache-Control header to 5 minutes.

    If a header is set already by route handler or other middleware, do not set it.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._config = src.config.Config()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Function, that is called by FastAPI."""
        response = await call_next(request)
        if "Cache-Control" not in response.headers:
            response.headers["Cache-Control"] = f"public, max-age={self._config.cache_time}"
        return response
