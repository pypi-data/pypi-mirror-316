import sys

from typing import Annotated

import typer

from typer.core import TyperGroup

from .Lib import Add


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.commands.keys()


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
@app.command(
    "EntryPoint",
    help=__doc__,
    no_args_is_help=False,
)
def EntryPoint(
    a: Annotated[int, typer.Argument(..., help="The value for 'a'")],
    b: Annotated[int, typer.Argument(..., help="The value for 'b'")],
) -> None:
    sys.stdout.write(f"{a} + {b} = {Add(a, b)}\n")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()
