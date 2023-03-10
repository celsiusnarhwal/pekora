from click import ClickException

from pekora.context import get_context


class PekoraProblem(ClickException):
    """
    Base exception for Pekora.

    Parameters
    ----------
    message : str, default: ""
    """

    def __init__(self, message: str = ""):
        super().__init__(message.strip())


class Otsupeko(PekoraProblem):
    """
    An exception that signals Pekora to perform a nonzero exit.

    For code 0 exits, use :class:`typer.Exit()` instead.

    Parameters
    ----------
    message : str, default: ""
    code : int, default: 0
        The code to exit with.
    """

    def __init__(self, message: str = "", code: int = 0):
        super().__init__(message)
        setattr(self, "ctx", get_context())
        self.exit_code = code
