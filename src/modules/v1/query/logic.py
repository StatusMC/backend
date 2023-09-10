"""Logic for the query module."""
import typing as t

import mcstatus

from src.logic import cacher
from src.models.v1 import OfflineStatusResponse, QueryResponse
from src.models.v1.exc import MCStatusException


@cacher.cached(ttl=3)
async def get_query(ip: str) -> t.Union[QueryResponse, OfflineStatusResponse, MCStatusException]:
    """Get the query response."""
    try:
        server = await mcstatus.JavaServer.async_lookup(ip, timeout=1)
    except Exception as exception:
        return await OfflineStatusResponse.from_mcstatus_object(
            ip, MCStatusException.from_exception(exception), is_java=True
        )

    try:
        query = await server.async_query()
    except Exception as exception:
        return await OfflineStatusResponse.from_mcstatus_object(
            server, MCStatusException.from_exception(exception), is_java=True
        )

    return QueryResponse.from_mcstatus_object(server, query)
