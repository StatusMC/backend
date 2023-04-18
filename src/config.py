"""File for the main config."""
import dataclasses
import os
import pathlib
import typing as t

import omegaconf
import typing_extensions as te
import yaml
from omegaconf import dictconfig

import src.utils

BASE_DIR = pathlib.Path(__file__).parent.parent
DEV_MODE = os.environ.get("DETA_SPACE_APP", "false") != "true"


@dataclasses.dataclass
class SentryConfigSection:
    """Sentry config section."""

    enabled: bool = False
    dsn: str = "..."
    traces_sample_rate: float = 1.0


@dataclasses.dataclass
class Config(metaclass=src.utils.Singleton):
    """The main config that holds everything in itself."""

    api_versions: t.List[int] = dataclasses.field(default_factory=lambda: [1])
    cache_time: int = 300
    sentry: SentryConfigSection = dataclasses.field(default_factory=SentryConfigSection)

    @classmethod
    def _setup(cls) -> te.Self:
        """Set up the config.

        It is just load config from file, also it is rewrite config with merged data.

        Returns:
            :py:class:`.Config` instance.
        """
        cfg = omegaconf.OmegaConf.structured(cls)

        if DEV_MODE:
            spacefile = yaml.safe_load((BASE_DIR / "Spacefile").open())
            assert spacefile["v"] == 0

            registered_env_variables = t.cast(
                t.List[str], list(map(lambda e: e["name"], spacefile["micros"][0]["presets"]["env"]))  # type: ignore[no-any-return]
            )
            right_env_variables = Config._get_right_env_variables(cfg)

            ridiculous = list(filter(lambda e: e not in right_env_variables, registered_env_variables))
            unregistered = list(filter(lambda e: e not in registered_env_variables, right_env_variables))
            if ridiculous or unregistered:
                formatted_ridiculous = "\n".join(ridiculous)
                formatted_unregistered = "\n".join(unregistered)

                raise ValueError(
                    (f"Ridiculous environment variables found:\n{formatted_ridiculous}\n\n" if ridiculous else "")
                    + f"Unregistered environment variables found:\n{formatted_unregistered}"
                    if unregistered
                    else ""
                )

        cls._handle_env_variables(cfg)

        return t.cast(te.Self, cfg)

    @staticmethod
    def _get_right_env_variables(cfg: dictconfig.DictConfig, *, prefix: str = "MWB") -> t.List[str]:
        result = []
        for key in cfg:
            key_to_look_for = f"{prefix}_{key!s}" if prefix else str(key)
            if isinstance(cfg[key], dictconfig.DictConfig):
                result.extend(Config._get_right_env_variables(cfg[key], prefix=key_to_look_for))
                continue

            result.append(key_to_look_for.upper())
        return result

    @staticmethod
    def _handle_env_variables(cfg: dictconfig.DictConfig, *, prefix: str = "MWB") -> None:
        """Process all values, and redef them with values from env variables."""
        for key in cfg:
            key_to_look_for = f"{prefix}_{key!s}" if prefix else str(key)
            if isinstance(cfg[key], dictconfig.DictConfig):
                Config._get_right_env_variables(cfg[key], prefix=key_to_look_for)
                continue

            if key_to_look_for in os.environ:
                cfg[key] = os.environ[key_to_look_for.upper()]
