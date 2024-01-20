import typing as t

import mcstatus.motd
import mcstatus.querier
import typing_extensions as te

from src.models.v1.shared import (
    AddressInResponse,
    BaseModel,
    BaseOnlineStatusResponse,
    FormattedString,
    PlayersInfo,
    VersionInfoOnlyName,
)


class QueryPlayersInfo(PlayersInfo):
    names: t.List[str]


class PluginInfo(BaseModel):
    name: str
    version: str

    @classmethod
    def from_string(cls, string: str) -> te.Self:
        try:
            name, version = string.rsplit(" ", maxsplit=1)
        except ValueError:
            return cls(name=string, version="")

        return cls(name=name, version=version)


class QueryVersionInfo(VersionInfoOnlyName):
    brand: FormattedString
    plugins: t.List[PluginInfo]


class QueryResponse(BaseOnlineStatusResponse):
    map_name: str
    players: QueryPlayersInfo
    version: QueryVersionInfo  # type: ignore[assignment] # we do not need liskov here

    @classmethod
    def from_mcstatus_object(
        cls,
        server: mcstatus.JavaServer,  # type: ignore[override] # we do not need liskov here
        query: mcstatus.querier.QueryResponse,  # type: ignore[override] # we do not need liskov here
    ) -> te.Self:
        motd = query.motd.simplify()
        version_name = mcstatus.motd.Motd.parse(query.software.version, bedrock=False).simplify()
        brand = mcstatus.motd.Motd.parse(query.software.brand, bedrock=False).simplify()

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
            map_name=query.map,
            version=QueryVersionInfo(
                name=FormattedString(
                    minecraft=version_name.to_minecraft(),
                    plain=version_name.to_plain(),
                    html=version_name.to_html(),
                    ansi=version_name.to_ansi(),
                ),
                brand=FormattedString(
                    minecraft=brand.to_minecraft(),
                    plain=brand.to_plain(),
                    html=brand.to_html(),
                    ansi=brand.to_ansi(),
                ),
                plugins=[PluginInfo.from_string(plugin) for plugin in query.software.plugins],
            ),
            players=QueryPlayersInfo(
                online=query.players.online,
                max=query.players.max,
                names=query.players.names,
            ),
        )
