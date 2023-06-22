import typing as t

import mcstatus.motd
import mcstatus.status_response
import typing_extensions as te

from src.models.v1.shared import (
    AddressInResponse,
    BaseModel,
    BaseOnlineStatusResponse,
    FormattedString,
    PlayersInfo,
    VersionInfo,
)


class PlayerInfo(BaseModel):
    name: FormattedString
    uuid: str


class JavaPlayersInfo(PlayersInfo):
    list: t.Optional[t.List[PlayerInfo]]


class JavaStatusResponse(BaseOnlineStatusResponse):  # type: ignore[misc] # Explicit "Any"
    players: JavaPlayersInfo
    icon: t.Optional[str]
    additional: t.Optional[t.Dict[str, t.Any]]  # type: ignore[misc] # Explicit "Any"

    @classmethod
    async def from_mcstatus_object(  # type: ignore[override] # we do not need liskov here
        cls, server: mcstatus.JavaServer, status: mcstatus.status_response.JavaStatusResponse
    ) -> te.Self:
        version_name = mcstatus.motd.Motd.parse(status.version.name, bedrock=False).simplify()
        motd = status.motd.simplify()
        additional_data = cls.get_additional_data(dict(status.raw.copy()))

        return cls(
            online=True,
            address=AddressInResponse(
                host=server.address.host,
                port=server.address.port,
            ),
            motd=FormattedString(
                raw=status.motd.raw,  # type: ignore[arg-type] # typed dicts
                plain=motd.to_plain(),
                html=motd.to_html(),
                ansi=motd.to_ansi(),
            ),
            version=VersionInfo(
                name=FormattedString(
                    raw=status.version.name,
                    plain=version_name.to_plain(),
                    html=version_name.to_html(),
                    ansi=version_name.to_ansi(),
                ),
                protocol=status.version.protocol,
            ),
            players=JavaPlayersInfo(
                online=status.players.online,
                max=status.players.max,
                list=cls.get_players_list(status.players.sample),
            ),
            icon=status.icon,
            additional=additional_data,
        )

    @staticmethod
    def get_additional_data(raw: t.Dict[str, t.Any]) -> t.Optional[t.Dict[str, t.Any]]:  # type: ignore[misc] # Explicit "Any"
        if isinstance(raw["description"], dict):
            for known_key in {
                "text",
                "translation",
                "color",
                "bold",
                "strikethrough",
                "italic",
                "underlined",
                "obfuscated",
            }:
                raw["description"].pop(known_key, None)

            if raw["description"].get("extra") is not None:
                for extra in raw["description"]["extra"]:
                    for known_key in {
                        "text",
                        "translation",
                        "color",
                        "bold",
                        "strikethrough",
                        "italic",
                        "underlined",
                        "obfuscated",
                    }:
                        extra.pop(known_key, None)

                raw["description"]["extra"] = list(filter(None, raw["description"]["extra"]))
                if not raw["description"]["extra"]:
                    raw["description"].pop("extra")

            if not raw["description"]:
                raw.pop("description")
        else:
            raw.pop("description")

        raw["players"].pop("online")
        raw["players"].pop("max")

        if raw["players"].get("sample") is not None:
            for player in raw["players"]["sample"]:
                player.pop("name")
                player.pop("id")

            raw["players"]["sample"] = list(filter(None, raw["players"]["sample"]))
            if not raw["players"]["sample"]:
                raw["players"].pop("sample")

        if not raw["players"]:
            raw.pop("players")

        raw["version"].pop("name")
        raw["version"].pop("protocol")
        if not raw["version"]:
            raw.pop("version")

        raw.pop("favicon", None)

        return raw if raw else None

    @staticmethod
    def get_players_list(
        players_sample: t.Optional[t.List[mcstatus.status_response.JavaStatusPlayer]],
    ) -> t.Optional[t.List[PlayerInfo]]:
        if players_sample is None:
            return None

        players = []
        for player in players_sample:
            player_name = mcstatus.motd.Motd.parse(player.name, bedrock=False)
            players.append(
                PlayerInfo(
                    name=FormattedString(
                        raw=player.name,
                        plain=player_name.to_plain(),
                        html=player_name.to_html(),
                        ansi=player_name.to_ansi(),
                    ),
                    uuid=player.uuid,
                )
            )

        return players
