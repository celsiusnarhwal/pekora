from __future__ import annotations

import re
import sys
from datetime import datetime
from functools import partial

import alianator
import inflect as ifl
import pyperclip
import typer
from InquirerPy.base import Choice
from rich import print, print_json
from rich.panel import Panel
from rich.table import Table

from pekora import callbacks, prompts, utils
from pekora.context import set_context
from pekora.exceptions import *
from pekora.models import *
from pekora.peko import Pekora

app = Pekora()
inflect = ifl.engine()


@app.command(name="calc", no_args_is_help=True)
@set_context
def calculate(
    _: typer.Context = None,
    expression: str = typer.Argument(
        ..., help="The expression to evaluate.", show_default=False
    ),
    raw: bool = typer.Option(
        None,
        "--raw",
        "-r",
        help="Don't use pretty formatting in the output. Ideal for piping to [bold cyan]pekora read[/] or "
        "other commands.",
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
        return eval(
            re.compile("|".join((str(p) for p in PekoraPattern.all()))).sub(
                lambda x: str(utils.ninjin(x.group())), expr
            )
        )

    # Split the expression on its comparators.
    parts = list(filter(None, re.split(rf"({PekoraPattern.COMPARATOR})", expression)))

    # No comparators.
    if len(parts) == 1:
        result = evaluate(*parts)

    # Balanced comparators.
    elif len(parts) % 2:
        # Equality comparators must stand alone.
        if len(parts) > 3 and set(parts).intersection({"==", "!="}):
            raise Otsupeko(
                "An equality comparator may not be used in the same expression as other comparators "
                "(including other equality comparators).",
            )

        result = eval(
            "".join(
                [
                    part if index % 2 else str(evaluate(part))
                    for index, part in enumerate(parts)
                ]
            )
        )

    # Imbalanced comparators.
    else:
        raise Otsupeko("Comparators must have an expression on both sides.")

    if result < 0:
        # If the result is negative, this will make it positive without losing any permission data.
        result = PekoraPermissions.from_flags(*PekoraPermissions(result).flags)

    print(
        result
        if raw
        else Panel(
            f"[cyan]{result}[/]", title="Result", title_align="left", style="green"
        )
    )

    if copy:
        pyperclip.copy(result)


@app.command(name="read", no_args_is_help=True)
@set_context
def read(
    _: typer.Context = None,
    permission: str = typer.Argument(
        ...,
        help="A permission flag, integer value, or Pekora permission group.",
        show_default=False,
        allow_dash=True,
    ),
    include: list[PekoraProperties.Category] = typer.Option(
        None,
        "--with",
        "--include",
        "-i",
        help="Explicitly include a data category, excluding all others not passed with -i.",
        show_default=False,
        rich_help_panel="Format Options",
    ),
    exclude: list[PekoraProperties.Category] = typer.Option(
        None,
        "--without",
        "--exclude",
        "-e",
        "-x",
        help="Explicitly exclude a data category. Supersedes -i.",
        show_default=False,
        rich_help_panel="Format Options",
    ),
    as_json: bool = typer.Option(
        None,
        "--json",
        help="Output the result as JSON.",
        rich_help_panel="Format Options",
    ),
    copy: bool = typer.Option(
        None,
        "--copy",
        "-c",
        help="Copy a JSON representation of the result to the clipboard (does not require --json).",
    ),
):
    """
    Read a permission.
    """
    if permission == "-":
        permission = sys.stdin.read()

    if not re.match(
        "|".join(map(str, PekoraPattern.permissions())) + "$",
        permission,
    ):
        raise Otsupeko(f"Invalid permission: {permission}")

    include = (set(include) or set(PekoraProperties.Category)) - set(exclude)

    if not include:
        raise Otsupeko("You must include at least one data category.")

    permset = PekoraPack.from_permissions(PekoraPermissions(utils.ninjin(permission)))

    json = permset.json(
        include={
            "permissions": {"__all__": {category.value for category in include}},
            "derived_from": True,
        }
    )

    if as_json:
        print_json(json)
    else:
        table_caption = f"Derived from: {permset.derived_from}"
        table = Table(
            caption=table_caption,
            min_width=len(table_caption),
            border_style=utils.pekora_blue().hex,
        )

        table.add_column("Flag", style="cyan")
        table.add_column("Name", style="yellow")
        table.add_column("Value", style="green")

        for perm in permset.permissions:
            table.add_row(*perm)

        for col in table.columns.copy():
            if not any(col.header.casefold() == category.value for category in include):
                table.columns.remove(col)

        print(table)

    if copy:
        pyperclip.copy(json)


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
    permissions = PekoraPermissions()

    if start:
        if not re.match(
            "|".join(map(str, PekoraPattern.permissions())) + "$",
            start,
        ):
            raise Otsupeko(f"Invalid expression: {start}")

        permissions += PekoraPermissions(utils.ninjin(start))

    choices = []
    for flag, name in alianator.resolutions(escape_mentions=False).items():
        if not any(
            PekoraPermissions.from_flags(c.value) == PekoraPermissions.from_flags(flag)
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
        filter=lambda v: PekoraPermissions.from_flags(*v),
    ).execute()

    print(
        Panel(
            f"[cyan]{permissions}[/]", title="Result", title_align="left", style="green"
        )
    )

    prompts.select(
        message="What would you like to do with the result?",
        choices=[
            Choice(
                value=partial(pyperclip.copy, str(permissions)),
                name="Copy to clipboard",
            ),
            Choice(
                value=partial(
                    read,
                    permission=str(permissions),
                    include=set(),
                    exclude=set(),
                    as_json=False,
                ),
                name="Read",
            ),
            Choice(
                value=partial(make, ctx=ctx, start=str(permissions)),
                name="Restart using this result as the starting value",
            ),
            Choice(value=lambda: ..., name="Nothing"),
        ],
    ).execute()()


# noinspection PyUnusedLocal
@app.callback(epilog=f"Pekora © {datetime.now().year} celsius narhwal.")
def konpeko(
    docs: bool = typer.Option(
        None,
        "--docs",
        is_eager=True,
        help="View Pekora's documentation.",
        callback=callbacks.docs,
        rich_help_panel="About Pekora",
    ),
    version: bool = typer.Option(
        None,
        "--version",
        is_eager=True,
        help="View Pekora's version.",
        callback=callbacks.version,
        rich_help_panel="About Pekora",
    ),
    license: bool = typer.Option(
        None,
        "--license",
        is_eager=True,
        help="View Pekora's license.",
        callback=callbacks.license,
        rich_help_panel="About Pekora",
    ),
    repo: bool = typer.Option(
        None,
        "--repo",
        is_eager=True,
        help="Visit Pekora on GitHub.",
        callback=callbacks.repo,
        rich_help_panel="About Pekora",
    ),
    debug: bool = typer.Option(
        None,
        "--debug",
        is_eager=True,
        hidden=True,
        callback=callbacks.debug,
    ),
):
    """
    Pekora is a calculator for Discord permission values.
    """


if __name__ == "__main__":
    app()
