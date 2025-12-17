"""Main CLI application using Typer."""

from typing import Optional

import typer

from proj.commands import projects
from proj.commands.inventory import inv_app

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


# Register project commands (8 core commands)
app.command(name="list")(projects.list_projects)
app.command(name="get")(projects.get_project)
app.command(name="create")(projects.create_project)
app.command(name="update")(projects.update_project)
app.command(name="delete")(projects.delete_project)
app.command(name="search")(projects.search_projects)
app.command(name="import-json")(projects.import_json)
app.command(name="archive")(projects.archive_project)

# Register inventory command group
app.add_typer(inv_app, name="inv")


if __name__ == "__main__":
    app()
