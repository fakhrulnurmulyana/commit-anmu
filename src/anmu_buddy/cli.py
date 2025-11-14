import typer
from anmu_buddy.git import app as git_app

app = typer.Typer(help="")
app.add_typer(git_app, name="git")