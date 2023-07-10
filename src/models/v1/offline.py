import typing as t

import mcstatus.address
import mcstatus.motd
import typing_extensions as te

from src.models.v1.exc import MCStatusException
from src.models.v1.shared import AddressInResponse, BaseStatusResponse


class OfflineStatusResponse(BaseStatusResponse):
    online: t.Literal[False]
    address: t.Union[AddressInResponse, str]
    error: MCStatusException

    @classmethod
    async def from_mcstatus_object(  # type: ignore[override] # we do not need liskov here
        cls,
        server: t.Union[mcstatus.JavaServer, mcstatus.BedrockServer, str],
        error: MCStatusException,
        *,
        is_java: bool,
    ) -> te.Self:
        address = cls._parse_address(server, is_java)

        return cls(
            online=False,
            address=(
                address
                if isinstance(address, str)
                else AddressInResponse(
                    host=address.host,
                    port=address.port,
                )
            ),
            error=error,
        )

    @staticmethod
    def _parse_address(
        server: t.Union[mcstatus.JavaServer, mcstatus.BedrockServer, str],
        is_java: bool,
    ) -> t.Union[mcstatus.address.Address, str]:
        if not isinstance(server, str):
            return server.address

        try:
            return mcstatus.address.Address.parse_address(server, default_port=25565 if is_java else 19132)
        except ValueError:  # the address is invalid
            return server
