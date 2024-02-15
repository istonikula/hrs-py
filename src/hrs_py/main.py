from datetime import datetime
from typing_extensions import Annotated
import typer

app = typer.Typer()


@app.command()
def main(
    file: Annotated[typer.FileText, typer.Argument()], date: Annotated[datetime, typer.Argument(formats=["%d.%m"])]
):
    print(f"file:{file.name} date:{date.day}.{date.month}")
    for line in file:
        print(f"line: {line}")
