"""Main CLI application using Typer."""

from typing import Optional

import typer

app = typer.Typer(
    name="proj",
    help="Unified CLI for project and inventory management.",
    no_args_is_help=True,
)


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from proj import __version__
        typer.echo(f"proj version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """Unified CLI for project and inventory management.
    
    Project commands manage projects in the work-prod API.
    Inventory commands scan and manage project inventory.
    """
    pass


if __name__ == "__main__":
    app()

