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
DEV_MODE = not bool(os.environ.get("PROD"))


@dataclasses.dataclass
class SentryConfigSection:
    """Sentry config section."""

    enabled: bool = False
    dsn: str = "..."
    traces_sample_rate: float = 1.0

    def __post_init__(self) -> None:
        """Disable Sentry if in dev mode."""
        if DEV_MODE:
            self.enabled = False


@dataclasses.dataclass
class Config(metaclass=src.utils.Singleton):
    """The main config that holds everything in itself."""

    api_versions: t.List[int] = dataclasses.field(default_factory=lambda: [1])
    sentry: SentryConfigSection = dataclasses.field(default_factory=SentryConfigSection)

    @classmethod
    def _setup(cls) -> te.Self:
        """Set up the config.

        It is just load config from file, also it is rewrite config with merged data.

        Returns:
            :py:class:`.Config` instance.
        """
        config_path = BASE_DIR / "data" / "config.yml"
        config_path.parent.mkdir(exist_ok=True)
        cfg = omegaconf.OmegaConf.structured(cls)

        if config_path.exists():
            loaded_config = omegaconf.OmegaConf.load(config_path)
            cfg = omegaconf.OmegaConf.merge(cfg, loaded_config)

        cls._handle_env_variables(cfg)

        with open(config_path, "w") as config_file:
            omegaconf.OmegaConf.save(cfg, config_file)

        return t.cast(te.Self, cfg)

    @staticmethod
    def _handle_env_variables(cfg: dictconfig.DictConfig, *, prefix: t.Optional[str] = None) -> None:
        """Process all values, and redef them with values from env variables.

        Args:
            cfg: :py:class:`.Config` instance.
            prefix:
                Prefix for env variable. Example ``prefix="sentry"`` and
                ``key="enabled"`` will look for ``SENTRY_ENABLED``.
        """
        for key in cfg:
            key_to_look_for = (f"{prefix}_{key!r}" if prefix else str(key)).upper()
            if isinstance(cfg[key], dictconfig.DictConfig):
                Config._handle_env_variables(cfg[key], prefix=key_to_look_for)
                continue

            if key_to_look_for in os.environ:
                cfg[key] = os.environ[key_to_look_for]
