from importlib import metadata
from pathlib import Path

import typer
from decorator import decorator
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel

from pekora import utils
from pekora.settings import PekoraSettings


@decorator
def callback(func, execute: bool):
    if execute:
        func(execute)
        raise typer.Exit()


@callback
def docs(_):
    typer.launch("https://pekora.celsiusnarhwal.dev")


@callback
def version(_):
    print(
        Panel(
            f"Pekora [cyan]{metadata.version('pekora')}[/]",
            title="Version",
            title_align="left",
            border_style=utils.pekora_blue().hex,
        )
    )


@callback
def license(_):
    license_file = (
        next(p for p in Path(__file__).parents if (p / "LICENSE.md").exists())
        / "LICENSE.md"
    )

    print(
        Panel(
            Markdown(license_file.read_text()),
            title="License",
            border_style=utils.pekora_blue().hex,
        )
    )


@callback
def debug(_):
    settings = PekoraSettings.load()
    settings.debug = not settings.debug
    status = "[green]enabled[/]" if settings.debug else "[red]disabled[/]"

    print(
        Panel(
            f"Debug mode {status}.",
            title="Debug Mode",
            title_align="left",
            border_style="violet",
        )
    )
