import typer
from rich import print

app = typer.Typer()


@app.command()
def new(app_name: str):
    print(f"Creating {app_name}")


if __name__ == "__main__":
    app()
