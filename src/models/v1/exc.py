import traceback

import pydantic
import typing_extensions as te


class MCStatusException(pydantic.BaseModel):
    short_name: str
    traceback: str

    @classmethod
    def from_exception(cls, exception: Exception) -> te.Self:
        return cls(
            short_name=repr(exception),
            traceback="".join(traceback.format_exception(type(exception), exception, exception.__traceback__)),
        )
