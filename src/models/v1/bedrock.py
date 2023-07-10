"""Models for Bedrock Edition servers."""
import typing as t

import mcstatus.motd
import mcstatus.status_response
import typing_extensions as te

from src.models.v1.shared import (
    AddressInResponse,
    BaseOnlineStatusResponse,
    FormattedString,
    PlayersInfo,
    VersionInfo,
)


class BedrockVersionInfo(VersionInfo):
    edition: t.Literal["MCPE", "MCEE"]


class BedrockStatusResponse(BaseOnlineStatusResponse):
    version: BedrockVersionInfo
    map_name: t.Optional[str]
    gamemode: t.Optional[str]

    @classmethod
    async def from_mcstatus_object(  # type: ignore[override] # we do not need liskov here
        cls, server: mcstatus.BedrockServer, status: mcstatus.status_response.BedrockStatusResponse
    ) -> te.Self:
        version_name = mcstatus.motd.Motd.parse(status.version.name, bedrock=True).simplify()
        motd = status.motd.simplify()

        return cls(
            online=True,
            address=AddressInResponse(
                host=server.address.host,
                port=server.address.port,
            ),
            motd=FormattedString(
                minecraft=motd.to_minecraft(),
                plain=motd.to_plain(),
                html=motd.to_html(),
                ansi=motd.to_ansi(),
            ),
            version=BedrockVersionInfo(
                name=FormattedString(
                    minecraft=version_name.to_minecraft(),
                    plain=version_name.to_plain(),
                    html=version_name.to_html(),
                    ansi=version_name.to_ansi(),
                ),
                protocol=status.version.protocol,
                edition=status.version.brand,  # type: ignore[arg-type] # literal in our signature
            ),
            players=PlayersInfo(
                online=status.players.online,
                max=status.players.max,
            ),
            map_name=status.map_name,
            gamemode=status.gamemode,
        )
