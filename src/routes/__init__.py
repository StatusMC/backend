"""Package for all routers and API."""
import importlib

import fastapi

from src.config import Config


def register_all_routers(app: fastapi.FastAPI) -> None:
    """Register all routers to the application."""
    register_home_route(app)
    for version in Config().api_versions:
        module = importlib.import_module(f"src.routes.versions.v{version}")
        router = getattr(module, f"V{version}ApiRouter")()
        router.register()
        app.include_router(router.router)


def register_home_route(app: fastapi.FastAPI) -> None:
    """Register home route that redirects to API docs."""

    @app.get("/")
    def home() -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(url="https://statusmc.perchun.it/api")
