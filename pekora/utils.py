from __future__ import annotations

from pathlib import Path
from typing import Callable

import typer
from colour import Color
from pydantic import validate_arguments
from yarl import URL

from pekora.exceptions import *
from pekora.models import *


@validate_arguments
def ninjin(term: str) -> str | int:
    """
    Convert a Pekora expression term to a Python literal.

    Pekora expression terms are:
    - Integers
    - Discord permission flags (e.g. `read_messages`)
    - Pekora permission groups (e.g. `pekora.general`)

    Parameters
    ----------
    term : str
        A valid Pekora expression term.

    Returns
    -------
    str | int
        Returns a string representation of the operator if the term is an operator. Otherwise, returns the integer
        value of the permission set represented by th term.

    """
    # Handle integers.
    if PekoraPattern.INTEGER.regex.match(term):
        return int(term)

    # Handle Discord permission flags.
    if term in PekoraPermissions.VALID_FLAGS:
        return PekoraPermissions(**{term: True}).value

    # Handle Pekora permission groups.
    match term.split("."):
        case ["pekora", group_name]:
            if isinstance(
                group := getattr(PekoraPermissions, group_name, None), Callable
            ):
                if isinstance(permissions := group(), PekoraPermissions):
                    return permissions.value

    # Handle unsupported operators.
    if PekoraPattern.UNSUPPORTED.regex.match(term):
        raise Otsupeko(f"Unsupported operator: {term}")

    # Handle other invalid input.
    raise Otsupeko(f"Invalid value: {term}")


def pekora_home() -> Path:
    home = Path(typer.get_app_dir("pekora"))
    home.mkdir(exist_ok=True)
    return home


def pekora_repo() -> URL:
    return URL("https://github.com/celsiusnarhwal/pekora")


def pekora_blue() -> Color:
    return Color("#b0bfe9")


def debug_epilog() -> str:
    return "[dim]Debug mode is [green]on[/]. Turn it off with [bold cyan]pekora --debug[/]."
