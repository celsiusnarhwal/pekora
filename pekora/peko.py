from __future__ import annotations

import textwrap

import typer
from rich import print
from rich.panel import Panel

from pekora import utils
from pekora.exceptions import PekoraException
from pekora.settings import PekoraSettings

settings = PekoraSettings.load()


class Pekora(typer.Typer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("no_args_is_help", True)
        kwargs.setdefault("rich_markup_mode", "rich")
        super().__init__(*args, **kwargs)

    def command(self, *args, **kwargs):
        if settings.debug:
            kwargs.setdefault("epilog", utils.debug_epilog())

        return super().command(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        try:
            super().__call__(*args, **kwargs)
        except PekoraException:
            raise
        except Exception as e:
            if settings.debug:
                raise
            elif e is not typer.Exit:
                msg = f"""
                An error ocurred. If this keeps happening, please open an issue: {utils.pekora_repo() / "issues/new"}
                """

                print(
                    Panel(
                        textwrap.dedent(msg).strip(),
                        title="Error",
                        title_align="left",
                        border_style="red",
                    )
                )
