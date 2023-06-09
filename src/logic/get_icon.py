"""Module for icon getter."""
import base64
import typing as t

from src.logic import cacher, get_status
from src.models import v1
from src.models.v1 import exc

DEFAULT_ICON = base64.b64decode(
    """
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAAXNSR0IArs4c6QAAAARnQU1BAACx
jwv8YQUAAAIcUExURa+vr7CwsLW1tcDAwMfHx83NzdPT076+vtTU1Ly8vLGxsbm5uc7OzsnJycTE
xL+/v7S0tMrKys/Pz7q6ure3t5CQkJubm5qamqurq8vLy9DQ0NLS0p+fn3BwcEBAQD4+Pj09PXl5
eampqbKysq6urlRUVDs7Ozc3NzY2NmFhYba2tszMzMjIyMHBwbi4uKenp0tLSzw8PFlZWaOjo62t
rbOzs0xMTDg4OENDQ0pKSlNTUzExMS4uLiwsLC8vLzo6Ojk5OZiYmIeHh3h4eGVlZYmJiaysrH9/
f29vb1hYWHFxcZycnGhoaC0tLUFBQTQ0NF9fX2ZmZk1NTU9PT0lJSWpqanR0dIuLi4aGhkJCQnx8
fMPDw4KCgk5OTjU1NURERFVVVUdHR1dXV15eXlxcXG5ubkhISH19fcXFxYyMjGlpaUVFRTIyMlBQ
UFZWVltbW8LCwru7u2JiYkZGRjMzM1FRUTAwMHd3d3Jycl1dXVJSUioqKpaWlmNjY729vcbGxj8/
P3t7e35+foCAgKioqGBgYHV1dZOTk4+Pj5eXl52dnVpaWqqqqoqKiqSkpJ6ennNzc4iIiJSUlHZ2
dpmZmW1tbY6OjmRkZI2NjYGBgYODgysrK4WFhXp6eikpKWtraygoKCcnJyYmJiUlJR8fHyQkJCMj
IyAgIBwcHCEhIR0dHSIiIoSEhJWVlZGRkaGhoaKioqWlpZKSkmdnZ7YtMnMAAAAJcEhZcwAADsMA
AA7DAcdvqGQAAAm0SURBVFhH7Zb9d9PWGcdVAoOQNTAIFApIoqAXKE3ltOjFkiWR0KYBLIEkIHKQ
ZDmpHJBlIJIFyGXIYaShaSGFthRcvLwUGFtL6fYP7hq8s0H5qf1h5+zsYx3r3qvn+d7n3vtcXUH/
53+C134j/1WBFV0rV/3utwis/t2aNWt+i0A38F8Drf319Pz+9d51v1Jgfc+63j9s2NjX1/cKgU2b
39jSKb6aFVvf3PaMla8S2L4DRtCdb3Vqr2TFc/dt2zb0AIFdL7IbwwmURPZ0qq9k77Y3397X+053
Tz/gZYF3KYLMkOjAe7ve77T8kv09/8EvBGiSYMgMm+F2dFpewf5+4Nnf37d3/fpdLwu8leWFnCjh
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
SUVORK5CYII=
    """
)


@cacher.cached(ttl=5 * 60)
async def get_icon(ip: t.Optional[str]) -> bytes:
    """Get the server icon as a PNG image."""
    if ip is None:
        return DEFAULT_ICON

    status = await get_status.get_status(ip, java=True)
    if (isinstance(status, v1.JavaStatusResponse) and status.icon is None) or isinstance(
        status, (exc.MCStatusException, v1.OfflineStatusResponse)
    ):
        return DEFAULT_ICON

    assert status.icon is not None
    encoded = status.icon[22:] if status.icon.startswith("data:image/png;base64,") else status.icon
    return base64.b64decode(encoded + "==")
