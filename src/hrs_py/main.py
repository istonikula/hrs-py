from datetime import datetime
from typing_extensions import Annotated
import typer

from hrs_py.lib import find_and_collect_day

app = typer.Typer()


@app.command()
def main(
    file: Annotated[typer.FileText, typer.Argument()], date: Annotated[datetime, typer.Argument(formats=["%d.%m"])]
):
    lines_in_day = list(find_and_collect_day((line.rstrip() for line in file), date))
    for line in lines_in_day:
        print(f"line: {line}")
