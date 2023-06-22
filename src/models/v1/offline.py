import typing as t

import mcstatus.address
import mcstatus.motd
import typing_extensions as te

from src.models.v1.exc import MCStatusException
from src.models.v1.shared import AddressInResponse, BaseStatusResponse


class OfflineStatusResponse(BaseStatusResponse):
    online: t.Literal[False]
    address: AddressInResponse
    error: MCStatusException

    @classmethod
    async def from_mcstatus_object(  # type: ignore[override] # we do not need liskov here
        cls,
        server: t.Union[mcstatus.JavaServer, mcstatus.BedrockServer, str],
        error: MCStatusException,
        *,
        is_java: bool,
    ) -> te.Self:
        address = (
            server.address
            if not isinstance(server, str)
            else mcstatus.address.Address.parse_address(server, default_port=25565 if is_java else 19132)
        )

        return cls(
            online=False,
            address=AddressInResponse(
                host=address.host,
                port=address.port,
            ),
            error=error,
        )
