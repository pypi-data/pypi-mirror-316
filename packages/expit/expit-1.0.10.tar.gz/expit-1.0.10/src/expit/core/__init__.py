import math

import click
import preparse

__all__ = ["function", "main"]


def function(x: float) -> float:
    "The expit function."
    try:
        p = math.exp(-x)
    except OverflowError:
        p = float("+inf")
    return 1 / (1 + p)


@preparse.PreParser(posix=False).click()
@click.command(add_help_option=False)
@click.help_option("-h", "--help")
@click.version_option(None, "-V", "--version")
@click.argument("x", type=float)
def main(x: float) -> None:
    "Apply the expit function to x."
    click.echo(function(x))
