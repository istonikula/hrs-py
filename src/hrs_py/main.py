from datetime import datetime, timedelta

import typer
from termcolor import colored
from typing_extensions import Annotated

from hrs_py.lib import find_and_collect_day, process_lines

app = typer.Typer()


@app.command()
def main(
    file: Annotated[typer.FileText, typer.Argument()], date: Annotated[datetime, typer.Argument(formats=["%d.%m"])]
):
    lines_in_day = list(find_and_collect_day((line.rstrip() for line in file), date.date()))
    durations, by_tag = process_lines(lines_in_day)
    total: timedelta = timedelta()

    print("----")
    for duration, line in durations:
        total += duration
        print(f"{HumanDuration(duration).line()} {line}")

    print("----")
    for tag, deltas in by_tag.items():
        print(f"{HumanDuration(sum((delta for delta in deltas), timedelta())).tag()} {tag}")

    print("----")
    full_day = timedelta(hours=7, minutes=30)
    diff = total - full_day
    if diff == timedelta():
        print(HumanDuration(total).total())
    else:
        print(f"{HumanDuration(total).total()} {HumanDuration(diff).diff()}")


class HumanDuration:
    def __init__(self, duration: timedelta):
        self.duration = duration

    def plain(self) -> str:
        return str(self)

    def line(self) -> str:
        return colored(self, "green", attrs=["bold"])

    def tag(self) -> str:
        return colored(self, "blue", attrs=["bold"])

    def total(self) -> str:
        return colored(self, "white", attrs=["bold"])

    def diff(self) -> str:
        return colored(f"-{self}", "red") if self.duration < timedelta() else colored(f"+{self}", "green")

    def __str__(self) -> str:
        delta = abs(self.duration)
        hours = delta // timedelta(hours=1)
        minutes = (delta // timedelta(minutes=1)) % 60
        return f"{hours:02}:{minutes:02}"
