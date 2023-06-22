"""Logic for getting the status of the server."""
import typing as t

import mcstatus

from src.logic import cacher
from src.models.v1 import (
    BedrockStatusResponse,
    JavaStatusResponse,
    OfflineStatusResponse,
)
from src.models.v1.exc import MCStatusException


@t.overload
async def get_status(  # noqa: D103
    ip: str, *, java: t.Literal[True] = True
) -> t.Union[JavaStatusResponse, OfflineStatusResponse, MCStatusException]:
    ...


@t.overload
async def get_status(  # noqa: D103
    ip: str, *, java: t.Literal[False]
) -> t.Union[BedrockStatusResponse, OfflineStatusResponse, MCStatusException]:
    ...


@t.overload
async def get_status(  # noqa: D103
    ip: str, *, java: bool = True
) -> t.Union[JavaStatusResponse, BedrockStatusResponse, OfflineStatusResponse, MCStatusException]:
    ...


@cacher.cached(ttl=5 * 60)
async def get_status(
    ip: str, *, java: bool = True
) -> t.Union[JavaStatusResponse, BedrockStatusResponse, OfflineStatusResponse, MCStatusException]:
    """Get the status of the server."""
    try:
        server = await mcstatus.JavaServer.async_lookup(ip) if java else mcstatus.BedrockServer.lookup(ip)
    except Exception as exception:
        return MCStatusException.from_exception(exception)

    assert isinstance(server, (mcstatus.JavaServer, mcstatus.BedrockServer))  # mypy thinks that it's their base class
    try:
        status = await server.async_status()
    except Exception as exception:
        return await OfflineStatusResponse.from_mcstatus_object(server, MCStatusException.from_exception(exception))

    model: t.Union[t.Type[JavaStatusResponse], t.Type[BedrockStatusResponse]] = (
        JavaStatusResponse if java else BedrockStatusResponse
    )
    return await model.from_mcstatus_object(server, status)  # type: ignore[arg-type] # breaks liskov. in runtime everything okay
