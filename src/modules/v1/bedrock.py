"""Bedrock module for API v1."""
import typing as t

from src.logic.get_status import get_status
from src.models.v1 import BedrockStatusResponse, OfflineStatusResponse
from src.models.v1.exc import MCStatusException
from src.modules.v1 import AbstractModule


class BedrockStatusModule(AbstractModule):
    """Bedrock module for API v1."""

    @classmethod
    async def execute(
        cls, ip: str, ip_from_args: t.Optional[str] = None
    ) -> t.Union[BedrockStatusResponse, OfflineStatusResponse, MCStatusException]:
        """Execute the module."""
        return await get_status(ip_from_args or ip, java=False)


Module = BedrockStatusModule
"""Alias, so we can automatically import the module."""
