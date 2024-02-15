import typer

app = typer.Typer()


@app.callback()
def callback():
    """
    callback
    """


@app.command()
def shoot():
    """
    shoot
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    load
    """
    typer.echo("Loading portal gun")
