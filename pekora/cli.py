from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from importlib import metadata
from pathlib import Path

import alianator
import inflect as ifl
import pyperclip
import typer
from InquirerPy.base import Choice
from rich import print
from rich.json import JSON
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from pekora import prompts
from pekora.models import *
from pekora.utils import Otsupeko, ninjin, set_context

app = typer.Typer(rich_markup_mode="rich")
inflect = ifl.engine()


# noinspection PyUnusedLocal
@app.command(name="calc")
@set_context
def calculate(
    context: typer.Context = None,
    expression: str = typer.Argument(..., help="The expression to evaluate."),
    raw: bool = typer.Option(
        None,
        "--raw",
        "-r",
        help="Don't use pretty formatting in the result. Ideal for piping to [cyan]pekora read[/] or other commands.",
    ),
    copy: bool = typer.Option(
        None,
        "--copy",
        "-c",
        help="Copy the result to the clipboard.",
    ),
):
    """
    Evaluate an expression.
    """

    def evaluate(expr: str) -> int:
        return eval(PekoraPattern.all().sub(lambda x: str(ninjin(x.group())), expr))

    parts = re.split(rf"({PekoraPattern.COMPARATOR.pattern})", expression)

    if len(parts) == 2:
        raise Otsupeko("Comparators must have an expression on both sides.")

    if len(parts) > 3:
        raise Otsupeko("Expressions may only have up to one comparator.")

    if len(parts) == 1:
        result = evaluate(parts[0])
    else:
        left, comparator, right = parts

        left = PekoraPermissions(evaluate(left))
        right = PekoraPermissions(evaluate(right))

        result = eval(f"left {comparator} right")

    print(
        result
        if raw
        else Panel(
            f"[cyan]{result}[/]", title="Result", title_align="left", style="green"
        )
    )

    if copy:
        pyperclip.copy(str(result))


# noinspection PyUnusedLocal
@app.command(name="read")
@set_context
def read(
    ctx: typer.Context = None,
    value: str = typer.Argument(
        ...,
        help="A permission flag, integer value, or Pekora permission group.",
        show_default=False,
    ),
    include: list[PekoraPermissionData.Category] = typer.Option(
        None,
        "--with",
        "--include",
        "-i",
        help="Explicitly include a data category, excluding all others not passed with -i.",
        show_default=False,
    ),
    exclude: list[PekoraPermissionData.Category] = typer.Option(
        None,
        "--without",
        "--exclude",
        "-e",
        "-x",
        help="Explicitly exclude a data category. Supersedes -i.",
        show_default=False,
    ),
    as_json: bool = typer.Option(None, "--json", help="Output the result as JSON."),
):
    """
    Read a permission.
    """
    if value == "-":
        value = sys.stdin.read()

    if not re.match(
        PekoraPattern.permissions().pattern + "$",
        value,
    ):
        raise Otsupeko(f"Invalid permission: {value}")

    include = (set(include) or set(PekoraPermissionData.Category)) - set(exclude)

    if not include:
        raise Otsupeko("You must include at least one data category.")

    permset = PekoraPermissionSet.from_permissions(PekoraPermissions(ninjin(value)))

    if as_json:
        print(
            JSON(
                json.dumps(
                    permset.dict(
                        include={
                            "permissions": {
                                "__all__": {category.value for category in include}
                            },
                            "derived_from": True,
                        }
                    )
                )
            )
        )
    else:
        table_caption = f"Derived from: {permset.derived_from}"
        table = Table(caption=table_caption, min_width=len(table_caption))

        table.add_column("Flag", style="cyan")
        table.add_column("Name", style="yellow")
        table.add_column("Value", style="green")

        for perm in permset.permissions:
            table.add_row(*perm)

        for col in table.columns.copy():
            if not any(col.header.casefold() == category.value for category in include):
                table.columns.remove(col)

        print(table)


# noinspection PyUnusedLocal
@app.command(name="make")
@set_context
def make(
    ctx: typer.Context = None,
    start: str = typer.Option(
        None,
        "--from",
        help="A permission flag, integer value, or Pekora permission group representing the permissions to start with.",
        show_default=False,
    ),
):
    """
    Interactively create a permission.
    """
    if start:
        if not re.match(
            PekoraPattern.permissions() + "$",
            start,
        ):
            raise Otsupeko(f"Invalid expression: {start}")

        permissions = PekoraPermissions(ninjin(start))
    else:
        permissions = PekoraPermissions()

    choices = []
    for flag, name in alianator.resolutions(escape_mentions=False).items():
        if not any(
            PekoraPermissions(**{c.value: True}) == PekoraPermissions(**{flag: True})
            for c in choices
        ):
            choices.append(
                Choice(value=flag, name=name, enabled=getattr(permissions, flag))
            )

    permissions += prompts.fuzzy(
        message="Choose some permissions. Type to search.",
        choices=choices,
        multiselect=True,
        border=True,
        transformer=lambda v: inflect.no("permission", len(v)),
        filter=lambda v: PekoraPermissions(**{choice: True for choice in v}),
    ).execute()

    print(
        Panel(
            f"[cyan]{permissions}[/]", title="Result", title_align="left", style="green"
        )
    )

    post = prompts.select(
        message="What would you like to do with the result?",
        choices=[
            Choice(
                value=lambda: pyperclip.copy(str(permissions)), name="Copy to clipboard"
            ),
            Choice(
                value=lambda: read(
                    value=str(permissions), include=set(), exclude=set(), as_json=False
                ),
                name="Read",
            ),
            Choice(
                value=lambda: make(ctx=ctx, start=str(permissions)),
                name="Restart using this result as the starting value",
            ),
            Choice(value=lambda: ..., name="Nothing"),
        ],
    ).execute()()


# noinspection PyUnusedLocal
@app.callback(
    epilog=f"Pekora © {datetime.now().year} celsius narhwal. Licensed under MIT (see --license)."
)
def konpeko(
    view_license: bool = typer.Option(
        None,
        "--license",
        is_eager=True,
        help="View Pekora's license.",
        callback=lambda v: (
            print(
                Panel(
                    Markdown(
                        (
                            next(
                                p
                                for p in Path(__file__).parents
                                if (p / "LICENSE.md").exists()
                            )
                            / "LICENSE.md"
                        ).read_text()
                    ),
                    title="License",
                    border_style="#b0bfe9",
                )
            ),
            exec("raise typer.Exit()"),
        )
        if v
        else ...,
    ),
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        is_eager=True,
        help="View Pekora's version.",
        callback=lambda v: (
            print(
                Panel(
                    f"Pekora [cyan]{metadata.version('pekora')}[/]",
                    title="Version",
                    title_align="left",
                    border_style="#b0bfe9",
                )
            ),
            exec("raise typer.Exit()"),
        )
        if v
        else ...,
    ),
):
    """
    Pekora is a calculator for Discord permission values.
    """


if __name__ == "__main__":
    app()
