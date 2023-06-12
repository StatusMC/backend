"""Logic for the query module."""
import typing as t

import mcstatus

from src.models.v1 import OfflineStatusResponse, QueryResponse
from src.models.v1.exc import MCStatusException


async def get_query(ip: str) -> t.Union[QueryResponse, OfflineStatusResponse, MCStatusException]:
    """Get the query response."""
    try:
        server = await mcstatus.JavaServer.async_lookup(ip)
    except Exception as exception:
        return MCStatusException.from_exception(exception)

    try:
        query = await server.async_query()
    except Exception as exception:
        return await OfflineStatusResponse.from_mcstatus_object(
            server, MCStatusException.from_exception(exception, with_internal_info=False)
        )

    return QueryResponse.from_mcstatus_object(server, query)