from __future__ import annotations

import re
from enum import Enum, StrEnum, auto
from typing import Self

import alianator
import discord
from pydantic import BaseModel, validate_arguments

__all__ = [
    "PekoraPermissions",
    "PekoraPattern",
    "PekoraPermissionData",
    "PekoraPermissionSet",
]


class PekoraPermissions(discord.Permissions):
    @property
    def flags(self) -> list[str]:
        return [perm for perm, granted in self if granted]

    @classmethod
    def from_flags(cls, *flags: str) -> Self:
        return cls(**{flag: True for flag in flags})

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        cls = type(self)
        return cls.__base__.__iter__(cls.__base__(self.value))


class PekoraPattern(Enum):
    # These values must be ordered by match precedence.
    GROUP = r"pekora\.\w+"
    INTEGER = r"\d+"
    FLAG = r"\w+"
    COMPARATOR = r"==|!=|[<>]=?"
    UNSUPPORTED = "[*/%@=]"

    @classmethod
    def all(cls) -> tuple[Self]:
        return tuple(iter(cls))

    @classmethod
    def permissions(cls) -> tuple[Self]:
        return cls.GROUP, cls.INTEGER, cls.FLAG

    @property
    def regex(self) -> re.Pattern:
        return re.compile(self.value)

    def __str__(self):
        return self.value


class PekoraPermissionData(BaseModel):
    class Category(StrEnum):
        FLAG = auto()
        NAME = auto()
        VALUE = auto()

    flag: str
    name: str
    value: str

    def __iter__(self):
        return iter((self.flag, self.name, self.value))


class PekoraPermissionSet(BaseModel):
    derived_from: int
    permissions: list[PekoraPermissionData]

    @classmethod
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def from_permissions(cls, permissions: PekoraPermissions):
        return cls(
            derived_from=permissions.value,
            permissions=[
                PekoraPermissionData(
                    flag=perm,
                    name=alianator.resolve(perm, escape_mentions=False)[0],
                    value=str(PekoraPermissions(**{perm: True}).value),
                )
                for perm in permissions.flags
            ],
        )
