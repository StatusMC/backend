import traceback

import pydantic
import typing as t
import typing_extensions as te

from src.routes.versions.v1.models.shared import InternalInfo


class MCStatusException(pydantic.BaseModel):
    short_name: str
    traceback: str
    internal: t.Optional[InternalInfo] = None
    """Present if returned by itself, not as a part of another model."""

    @classmethod
    def from_exception(cls, exception: Exception, *, with_internal_info: bool = True) -> te.Self:
        return cls(
            short_name=repr(exception),
            traceback="".join(traceback.format_exception(type(exception), exception, exception.__traceback__)),
            internal=InternalInfo(
                cached_at=0,
                cache_ends_at=0,
            ) if with_internal_info else None,
        )
