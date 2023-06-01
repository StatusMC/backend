"""Java status module for API v1."""
import typing as t

from src.logic.get_status import get_status
from src.models.v1 import JavaStatusResponse, OfflineStatusResponse
from src.models.v1.exc import MCStatusException
from src.modules.v1 import AbstractModule


class JavaStatusModule(AbstractModule):
    """Java status module for API v1."""

    @classmethod
    async def execute(cls, ip: str) -> t.Union[JavaStatusResponse, OfflineStatusResponse, MCStatusException]:
        """Execute the module."""
        return await get_status(ip, java=True)


Module = JavaStatusModule
"""Alias, so we can automatically import the module."""
