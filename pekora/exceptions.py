from typing import Annotated

from click import ClickException
from pydantic import Field, validate_arguments

from pekora.context import get_context


class PekoraProblem(ClickException):
    """
    Base exception for Pekora.
    """

    def __init__(self, message: str):
        super().__init__(message.strip())


class Otsupeko(PekoraProblem):
    """
    An exception that signals Pekora to perform a nonzero exit with an error message.

    To exit code 0 or without a message, use :class:`typer.Exit()` instead.

    Parameters
    ----------
    message : str
        The error message.
    code : int, default: 1
        The code to exit with.
    """

    @validate_arguments
    def __init__(self, message: str, code: Annotated[int, Field(ge=1, le=255)] = 1):
        super().__init__(message)
        setattr(self, "ctx", get_context())
        self.exit_code = code
