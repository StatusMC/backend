"""Package for all routers and API."""
import importlib

import fastapi

from src.config import Config


def register_all_routers(app: fastapi.FastAPI) -> None:
    """Register all routers to the application."""
    for version in Config().api_versions:
        module = importlib.import_module(f"src.routes.versions.v{version}")
        router = getattr(module, f"V{version}ApiRouter")()
        router.register()
        app.include_router(router.router)
