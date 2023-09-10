"""Logic for caching the results of some functions."""
import asyncio
import datetime
import functools
import time
import typing as t

import asyncache
import cachetools
import pydantic
import typing_extensions as te

_P = te.ParamSpec("_P")
_R = t.TypeVar("_R")


def cached(
    ttl: t.Union[int, t.Literal["forever"]] = "forever", max_amount: int = 1024
) -> t.Callable[[t.Callable[_P, _R]], t.Callable[_P, _R]]:
    """Cache the result of the function.

    Args:
        ttl:
            The time to live of the cache. If set to "forever", the cache will never expire.
            We use TTL cache strategy if the ttl is an integer, and FIFO cache strategy otherwise.
        max_amount:
            The maximum number of the cached results. Mostly useful for FIFO cache strategy.

            Why is default value 1024? I wrote a small script, that generates random models and caches them.
            Then I generated 1024, 10 000 and 100 000 models and checked the memory usage of the script minus
            memory usage if there were 0 objects generated. Here are the results:

            +------------+-------------------+
            | Amount     | Memory usage, MiB |
            +============+===================+
            | 1024       | 9.4               |
            | 10 000     | 89.4              |
            | 100 000    | 892.9             |
            +------------+-------------------+

            10 mb is not that much, so I decided to use 1024 as the default value.

    Example:
        .. code-block:: python

            @cached(ttl=5 * 60)
            def my_func():
                ...
    """
    cache_storage: cachetools.Cache = (  # type: ignore[type-arg] # missing generic args for cache, doesn't matter here
        cachetools.TTLCache(max_amount, ttl) if isinstance(ttl, int) else cachetools.FIFOCache(max_amount)
    )

    def decorate(func: t.Callable[_P, _R]) -> t.Callable[_P, _R]:
        @functools.wraps(func)
        async def async_wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            result = await asyncache.cached(cache_storage)(func)(*args, **kwargs)
            return result  # type: ignore[no-any-return]

        @functools.wraps(func)
        def sync_wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            result = cachetools.cached(cache_storage)(func)(*args, **kwargs)
            return result

        if asyncio.iscoroutinefunction(func):
            return t.cast("t.Callable[_P, _R]", async_wrapper)
        return t.cast("t.Callable[_P, _R]", sync_wrapper)

    return decorate
