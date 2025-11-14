import typer
from .service import GitService
from typing import List

app = typer.Typer(help="Git automation commands for AnmuBuddy.")
service = GitService()

@app.command()
def commit(files: List[str], message_file:str):
    """Commit change to the repository."""
    try:
        service.commit(files= files, message_file= message_file)
        typer.echo("Commit completed successfully.")
    except Exception as e:
        typer.echo(f"Commit failed: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def push(
        files: List[str], 
        remote:str="origin", 
        branch:str=None,
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