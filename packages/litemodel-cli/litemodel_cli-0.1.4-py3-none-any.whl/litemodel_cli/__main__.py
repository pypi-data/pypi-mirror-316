import typer
from rich import print
from litemodel_cli.project_structure import ProjectStructure

app = typer.Typer()


@app.command()
def new(app_name: str):
    ProjectStructure()()
    print(f"Creating {app_name}")


app()
