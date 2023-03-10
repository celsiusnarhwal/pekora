from pathlib import Path
from typing import ClassVar, Self

from pydantic import BaseSettings

from pekora import utils


class PekoraPreferences(BaseSettings):
    class Config:
        extra = "forbid"

    file: ClassVar[Path] = utils.pekora_home() / "config.json"

    debug: bool = False

    @classmethod
    def load(cls) -> Self:
        if not cls.file.exists():
            cls.file.write_text(cls().json())

        return cls.parse_file(cls.file)

    def save(self):
        self.file.write_text(self.json())

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
