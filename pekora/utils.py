from __future__ import annotations

from typing import Annotated, Callable

import typer
from decorator import decorator
from pydantic import Field, validate_arguments

from pekora.models import *

CONTEXT: typer.Context = None


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


# noinspection PyPep8Naming
@validate_arguments
def Otsupeko(msg: str, code: Annotated[int, Field(ge=1, le=255)] = 1):
    """
    An exception that causes Pekora to exit with a non-zero exit code.

    For code 0 exits, use :class:`typer.Exit()` instead.

    Parameters
    ----------
    msg : str
        The error message to display.
    code : int, defaul: 1
        The exit code to return.

    Examples
    --------
    >>> raise Otsupeko("Something went wrong.")
    """
    exception = OtsupekoException(msg.strip())
    exception.exit_code = code
    setattr(exception, "ctx", CONTEXT)
    return exception


@decorator
def set_context(func: Callable, *args, **kwargs):
    """
    A decorator that sets :data:`pekora.utils.CONTEXT` to the first argument of the decorated function.
    """
    global CONTEXT
    CONTEXT = args[0]
    return func(*args, **kwargs)
