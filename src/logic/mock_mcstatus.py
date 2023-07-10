"""Small fixes to ``mcstatus`` for the purpose of this project."""
import importlib

import mcstatus.server
import mcstatus.utils


def apply_mcstatus_mocks() -> None:
    """Apply all mock functions for ``mcstatus``."""
    _mock_retry_decorator_retry_only_once()


def _mock_retry_decorator_retry_only_once() -> None:
    """Mock ``mcstatus.utils.retry`` to retry only once."""
    mcstatus.utils.retry = lambda *_, **__: lambda f: f  # type: ignore
    importlib.reload(mcstatus.server)  # only this module uses the retry decorator
