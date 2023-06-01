"""Icon module for API v1."""
import base64

from src.modules.v1 import AbstractModule
from src.modules.v1.icon import logic


class IconModule(AbstractModule):
    """Icon module for API v1."""

    @classmethod
    async def execute(cls, ip: str) -> str:
        """Execute the module."""
        return base64.b64encode(await logic.get_icon(ip)).decode("utf-8")


Module = IconModule
"""Alias, so we can automatically import the module."""
