from __future__ import annotations

import typer
from rich import print
from rich.panel import Panel

from pekora import utils
from pekora.prefs import PekoraPreferences


class Pekora(typer.Typer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("no_args_is_help", True)
        kwargs.setdefault("rich_markup_mode", "rich")
        super().__init__(*args, **kwargs)

    def callback(self, *args, **kwargs):
        with PekoraPreferences.load() as settings:
            if settings.debug:
                kwargs["epilog"] = (
                    kwargs.get("epilog", "") + "\n\n" + utils.debug_epilog()
                ).strip()

        return super().callback(*args, **kwargs)

    def command(self, *args, **kwargs):
        with PekoraPreferences.load() as settings:
            if settings.debug:
                kwargs["epilog"] = (
                    kwargs.get("epilog", "") + "\n\n" + utils.debug_epilog()
                ).strip()

        return super().command(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        try:
            super().__call__(*args, **kwargs)
        except Exception as e:  # Yes, we really do want to catch *everything*.
            # PekoraProblem is a ClickException so Typer will handle those before we even get here.

            if e is typer.Exit:  # "except typer.Exit: pass" doesn't work, apparently.
                return

            with PekoraPreferences.load() as settings:
                if settings.debug:
                    raise

            msg = (
                f"An error ocurred. If this keeps happening, please open an issue: "
                f"{utils.pekora_repo() / 'issues/new'}"
            )

            print(
                Panel(
                    msg,
                    title="Error",
                    title_align="left",
                    border_style="red",
                )
            )
