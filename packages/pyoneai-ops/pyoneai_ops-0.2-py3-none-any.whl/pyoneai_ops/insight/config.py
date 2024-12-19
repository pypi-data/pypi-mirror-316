__all__ = (
    "Config",
    "get_config",
)
import os
from dataclasses import dataclass
from functools import lru_cache

import yaml

from ..logger import LogConfig

INSIGHT_CONF_PATH: str = os.environ.get(
    "PYONEAIOPS_INSIGHT_CONF_PATH", "/etc/one/aiops/insight.conf"
)


@dataclass
class Config:
    """
    Configuration data class for Insight Server settings.

    Attributes
    ----------
    host : str
        The host address for the service.
    port : int
        The port number for the service.
    version : str
        The API version.
    config_path : os.PathLike or None, optional
        The path to the configuration file, by default None.
    log : LogConfig
        The logging configuration, defaults to a new instance of
        LogConfig.
    """

    host: str
    port: int
    version: str
    config_path: os.PathLike | None = None
    log: LogConfig = LogConfig()

    def __post_init__(self):
        if isinstance(self.log, dict):
            self.log = LogConfig(**self.log)

    @property
    def path(self) -> str:
        """
        API path based on the version.

        Returns
        -------
        str
            The API path as a string.
        """
        return f"/api/{self.version}"


@lru_cache(maxsize=1)
def get_config() -> Config:
    """
    Load and return the configuration from a YAML file.

    Returns
    -------
    Config
        An instance of the Config class populated with settings from
        the YAML file.
    """
    with open(INSIGHT_CONF_PATH, "r") as file:
        return Config(**yaml.safe_load(file))
