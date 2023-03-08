from __future__ import annotations

import re
from enum import Enum, StrEnum, auto

import alianator
import click
import discord
from pydantic import BaseModel, validate_arguments

__all__ = [
    "PekoraPermissions",
    "PekoraPattern",
    "PekoraPermissionData",
    "PekoraPermissionSet",
    "OtsupekoException",
]


class PekoraPatternParent(Enum):
    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = re.compile(value)
        return member


class PekoraPattern(PekoraPatternParent):
    """
    Enumerates useful regular expressions.

    All members of this enumeration are :class:`re.Pattern` objects.
    """

    # These values must be ordered by match precedence.
    GROUP = r"pekora\.\w+"
    INTEGER = r"\d+"
    FLAG = r"\w+"
    COMPARATOR = r"==|!=|[<>]=?"
    UNSUPPORTED = "[*/%@=]"

    @classmethod
    def combine(cls, *patterns: PekoraPattern | re.Pattern | str) -> re.Pattern:
        return re.compile(
            "|".join(
                pattern if type(pattern) is str else pattern.pattern
                for pattern in patterns
            )
        )

    # noinspection PyArgumentList
    @classmethod
    def all(cls) -> re.Pattern:
        return cls.combine(*cls)

    @classmethod
    def permissions(cls) -> re.Pattern:
        return cls.combine(cls.GROUP, cls.INTEGER, cls.FLAG)

    @property
    def regex(self) -> re.Pattern:
        return self.value

    @property
    def pattern(self):
        return self.regex.pattern


class PekoraPermissions(discord.Permissions):
    def flags(self) -> list[str]:
        return [perm for perm, granted in self if granted]

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        cls = type(self)
        return cls.__base__.__iter__(cls.__base__(self.value))


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
                for perm in permissions.flags()
            ],
        )


class OtsupekoException(click.ClickException):
    """
    The exception raised by :func:`pekora.utils.Otsupeko`.

    Use :func:`pekora.utils.Otsupeko` rather than instantiating this class directly.
    """
