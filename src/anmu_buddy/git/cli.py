import typer
from .service import GitService
from typing import List, Annotated

app = typer.Typer(help="Git automation commands for AnmuBuddy.")
service = GitService()

@app.command()
def commit(
        files: Annotated[
            List[str],
            typer.Option(
                "--files", "-f",
                help="List of files to commit."
            )
        ]
    ):
    """Commit change to the repository."""
    try:
        service.commit(files= files)
        typer.echo("Commit completed successfully.")
    except Exception as e:
        typer.echo(f"Commit failed: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def push(
        files: Annotated[
            List[str],
            typer.Option(
                "--files", "-f",
                help="List of files to push."
            )
        ], 
        remote:Annotated[
            str,
            typer.Option(
                "--remote", "-r",
                help="Remote name."
            )
        ]="origin", 
        branch:Annotated[
            str,
            typer.Option(
                "--branch", "-b",
                help="Branch name to push to. Optional; uses the current branch when omitted."
            )]=None,
    ):
    """Commit and push change to the repository."""
    try:
        branch_display = service.push(
            files= files, 
            remote= remote, 
            branch= branch
        )
        typer.echo(f"Push to {remote}/{branch_display} cempleted successfully.")
    except Exception as e:
        typer.echo(f"Push failed: {e}", err=True)
        raise typer.Exit(code=1)