"""Package for API version 1."""
import time
import typing as t

import fastapi
from routes.versions.v1.models.exc import MCStatusException

from src.routes.abc import ApiRouter
from src.routes.versions.v1.logic import get_icon, get_status
from src.routes.versions.v1.models import (
    BedrockStatusResponse,
    JavaStatusResponse,
    OfflineStatusResponse,
)


class V1ApiRouter(ApiRouter):
    """Router for API version 1."""

    version = 1

    def register(self) -> None:
        """Register all routes to the router."""
        self.router.add_api_route("/status/{edition}/{ip}", self.get_status, methods=["GET"])
        self.router.add_api_route("/icon/{ip}", self.get_icon, methods=["GET"])
        self.router.add_api_route("/icon", self.get_icon, methods=["GET"])

    async def get_status(
        self, edition: t.Literal["java", "bedrock"], ip: str
    ) -> t.Union[JavaStatusResponse, BedrockStatusResponse, OfflineStatusResponse, MCStatusException]:
        """Get the status of the server."""
        model = await get_status.get_status(ip, java=edition == "java")
        model.internal.cached_at = int(time.time())
        model.internal.cache_ends_at = model.internal.cached_at + self._config.cache_time + 1
        return model

    async def get_icon(self, ip: t.Optional[str] = None) -> fastapi.Response:
        """Get the icon of the server.

        If ``ip`` is not provided - returns the default icon.
        """
        return fastapi.Response(content=await get_icon.get_icon(ip), media_type="image/png")
