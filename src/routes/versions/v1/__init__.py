"""Package for API version 1."""
import asyncio
import importlib
import typing as t
from pathlib import Path

import fastapi

from src.logic.get_icon import get_icon
from src.modules.v1 import AbstractModule
from src.routes.abc import ApiRouter


class V1ApiRouter(ApiRouter):
    """Router for API version 1."""

    version = 1

    def register(self) -> None:
        """Register all routes to the router."""
        self.router.add_api_route("/icon/{ip}", self.get_icon, methods=["GET"])
        self.router.add_api_route("/icon", self.get_icon, methods=["GET"])
        self.router.add_api_route("/{ip}", self.execute_modules, methods=["GET"])

    async def execute_modules(  # type: ignore[misc] # explicit any
        self, ip: str, modules: str
    ) -> t.Union[t.Dict[str, t.Any], str]:
        """Execute provided modules in an API endpoint."""
        modules = modules.split(",")
        if modules is None or len(modules) == 0:
            return (
                "No modules specified, please specify at least one module.\n"
                "If you don't know what I am talking about, please read the documentation at "
                "https://statusmc.perchun.it/api."
            )

        results, _ = await asyncio.wait(
            self._generate_tasks_with_modules(ip, modules),
            return_when=asyncio.ALL_COMPLETED,
        )

        return {task.get_name(): task.result() for task in results}

    def _generate_tasks_with_modules(
        self, ip: str, modules_names: t.List[str]
    ) -> t.Set[asyncio.Task]:  # type: ignore[type-arg] # generic in asyncio task
        to_return = set()
        for module_name in modules_names:
            reasons_for_fail = self._validate_module_name(module_name)

            if reasons_for_fail:
                message = f"Module name {module_name!r} is invalid ({', '.join(reasons_for_fail)})."
                to_return.add(asyncio.create_task(self._fail_module(message), name=module_name))
                continue

            module = self._import_module(module_name)
            to_return.add(asyncio.create_task(module.execute(ip), name=module_name))

        return to_return

    def _validate_module_name(self, module_name: str) -> t.List[str]:
        reasons: t.List[str] = []
        if module_name == "":
            reasons.append("empty")
        if module_name.startswith("_"):
            reasons.append("starts with `_`")
        if all(not Path(f"src/modules/v{self.version}/{module_name}{suffix}").exists() for suffix in {"", ".py"}):
            reasons.append("does not exist")
        return reasons

    async def _fail_module(self, message: str) -> str:
        return message

    def _import_module(self, module_name: str) -> t.Type[AbstractModule]:
        """Import a module by a name."""
        return importlib.import_module(f"src.modules.v{self.version}.{module_name}").Module  # type: ignore[no-any-return] # too dinamic for typing

    async def get_icon(self, ip: t.Optional[str] = None) -> fastapi.Response:
        """Get the icon of the server.

        If ``ip`` is not provided - returns the default icon.
        """
        return fastapi.Response(content=await get_icon(ip), media_type="image/png")
