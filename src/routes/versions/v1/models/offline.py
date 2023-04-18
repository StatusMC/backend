import typing as t

import mcstatus.motd
import typing_extensions as te
from routes.versions.v1.models.exc import MCStatusException

from src.routes.versions.v1.models.shared import (
    AddressInResponse,
    BaseStatusResponse,
    InternalInfo,
)


class OfflineStatusResponse(BaseStatusResponse):
    online: t.Literal[False]
    error: MCStatusException

    @classmethod
    async def from_mcstatus_object(  # type: ignore[override] # we do not need liskov here
        cls, server: t.Union[mcstatus.JavaServer, mcstatus.BedrockServer], error: MCStatusException
    ) -> te.Self:
        return cls(
            online=False,
            address=AddressInResponse(
                host=server.address.host,
                port=server.address.port,
            ),
            internal=InternalInfo(
                cached_at=0,
                cache_ends_at=0,
            ),
            error=error,
        )
