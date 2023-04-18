"""Module for the abstract base class for all API routers."""
import abc

import fastapi

import src.config


class ApiRouter(abc.ABC):
    """Abstract base class for all API routers."""

    version: int

    def __init__(self) -> None:
        self.router = fastapi.APIRouter(prefix=f"/v{self.version}")
        self._config = src.config.Config()

    @abc.abstractmethod
    def register(self) -> None:
        """Register all routes to the router."""
