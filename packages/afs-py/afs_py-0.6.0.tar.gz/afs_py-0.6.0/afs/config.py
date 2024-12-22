import logging
import pathlib
import tempfile
import typing

import diskcache
from faker import Faker
from pydantic import Field, PrivateAttr, SecretStr
from pydantic_settings import BaseSettings
from rich.console import Console

console = Console()
fake = Faker()

LOGGER_NAME = "afs"


class Settings(BaseSettings):
    # LLMs
    OPENAI_API_KEY: typing.Optional[SecretStr] = Field(default=None)
    AZURE_OPENAI_API_KEY: typing.Optional[SecretStr] = Field(default=None)
    AZURE_OPENAI_ENDPOINT: typing.Optional[typing.Text] = Field(default=None)
    OPENAI_API_VERSION: typing.Optional[typing.Text] = Field(default=None)

    # Cache
    LOCAL_CACHE_PATH: typing.Text = Field(
        default=str(pathlib.Path(tempfile.gettempdir()).joinpath(".afs_cache"))
    )

    # Private
    _local_cache: typing.Optional[diskcache.Cache] = PrivateAttr(default=None)

    @property
    def local_cache(self) -> diskcache.Cache:
        if self._local_cache is None:
            self._local_cache = diskcache.Cache(self.LOCAL_CACHE_PATH)
        return self._local_cache


settings = Settings()
logger = logging.getLogger(LOGGER_NAME)
