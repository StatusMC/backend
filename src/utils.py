"""Module for some of our utils."""
import os
import pathlib
import typing as t

import sentry_sdk


class Singleton(type):
    """Metaclass to do Singleton pattern."""

    _instances: dict[type, t.Any] = {}  # type: ignore[misc] # Explicit "Any" is not allowed

    def __call__(cls, *args, **kwargs):
        """Actual logic in this class.

        See https://stackoverflow.com/a/6798042.
        """
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)

            if hasattr(instance, "_setup"):
                instance = instance._setup()
            cls._instances[cls] = instance

        return cls._instances[cls]


def start_sentry() -> None:
    """Start Sentry listening."""
    # circular imports
    from src.config import BASE_DIR, Config

    config = Config()

    if not config.sentry.enabled:
        return

    sentry_sdk.init(
        dsn=config.sentry.dsn,
        traces_sample_rate=config.sentry.traces_sample_rate,
        release=_get_commit(BASE_DIR / "commit.txt"),
        environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
        _experiments={
            "profiles_sample_rate": 1.0,
        },
    )


def _get_commit(commit_txt_path: pathlib.Path) -> t.Optional[str]:
    """Get current commit from ``commit.txt`` file."""
    if not commit_txt_path.exists():
        return None

    with commit_txt_path.open() as commit_txt_file:
        commit = commit_txt_file.read().strip()
        return commit
