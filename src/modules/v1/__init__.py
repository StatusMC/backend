"""Abstract module class for v1 modules."""
import abc
import typing as t


class AbstractModule(abc.ABC):
    """Abstract module class for v1 modules."""

    @classmethod
    @abc.abstractmethod
    async def execute(cls, ip: str, arg: t.Optional[str] = None, /) -> t.Any:  # type: ignore[misc] # explicit any
        """Execute the module."""
        raise NotImplementedError("I'm abstract!")
