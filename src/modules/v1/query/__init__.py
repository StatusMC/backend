"""Query module for API v1."""
import typing as t

from src.models.v1 import OfflineStatusResponse, QueryResponse
from src.models.v1.exc import MCStatusException
from src.modules.v1 import AbstractModule
from src.modules.v1.query.logic import get_query


class QueryModule(AbstractModule):
    """Query module for API v1."""

    @classmethod
    async def execute(cls, ip: str) -> t.Union[QueryResponse, OfflineStatusResponse, MCStatusException]:
        """Execute the module."""
        return await get_query(ip)


Module = QueryModule
"""Alias, so we can automatically import the module."""
