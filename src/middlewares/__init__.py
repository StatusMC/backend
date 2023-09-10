"""Package for middlewares."""
import fastapi

import src.middlewares.cache_control


def register_middlewares(app: fastapi.FastAPI) -> None:
    """Register all middlewares to the application."""
    app.add_middleware(src.middlewares.cache_control.CacheControlMiddleware)
