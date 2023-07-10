import abc
import typing as t

import mcstatus.querier
import mcstatus.status_response
import pydantic
import typing_extensions as te


class BaseModel(pydantic.BaseModel):
    @pydantic.root_validator(pre=False)
    def check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:  # type: ignore[misc] # Explicit "Any"
        result = values.copy()
        for key, value in values.items():
            if value is None:
                del result[key]
        return result


class AddressInResponse(BaseModel):
    host: str
    port: int


class InternalInfo(BaseModel):
    cached_at: int
    cache_ends_at: int


class FormattedString(BaseModel):  # type: ignore[misc] # Explicit "Any"
    raw: t.Union[t.Dict[str, t.Any], t.List[t.Dict[str, t.Any]], str]  # type: ignore[misc] # Explicit "Any"
    plain: str
    html: str
    ansi: str


class VersionInfoOnlyName(BaseModel):
    name: FormattedString


class VersionInfo(VersionInfoOnlyName):
    protocol: int


class PlayersInfo(BaseModel):
    online: int
    max: int


class BaseStatusResponse(BaseModel, abc.ABC):
    online: bool
    address: AddressInResponse

    @classmethod
    @abc.abstractmethod
    def from_mcstatus_object(
        cls,
        server: t.Union[mcstatus.JavaServer, mcstatus.BedrockServer],
        status_or_query: t.Union[
            mcstatus.status_response.JavaStatusResponse,
            mcstatus.status_response.BedrockStatusResponse,
            mcstatus.querier.QueryResponse,
        ],
        /,
    ) -> te.Self:
        ...


class BaseOnlineStatusResponse(BaseStatusResponse, abc.ABC):
    online: t.Literal[True]
    motd: FormattedString
    version: VersionInfo
    players: PlayersInfo
