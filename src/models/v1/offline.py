import typing as t

import mcstatus.motd
import typing_extensions as te

from src.models.v1.exc import MCStatusException
from src.models.v1.shared import AddressInResponse, BaseStatusResponse


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
            error=error,
        )
