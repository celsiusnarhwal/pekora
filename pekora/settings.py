from pathlib import Path
from typing import ClassVar, Self

from pydantic import BaseSettings

from pekora import utils

__all__ = ["PekoraSettings"]


class PekoraSettings(BaseSettings):
    class Config:
        extra = "ignore"

    file: ClassVar[Path] = utils.pekora_home() / "config.json"

    debug: bool = False

    @classmethod
    def load(cls) -> Self:
        if not cls.file.exists():
            cls.file.write_text(cls().json())

        return cls.parse_file(cls.file)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self.file.write_text(self.json())
