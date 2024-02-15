from collections.abc import Iterator
from datetime import datetime


def find_and_collect_day(lines: Iterator[str], date: datetime) -> Iterator[str]:
    in_day = False
    date_str = f"{date.day}.{date.month}"

    for line in lines:
        if not in_day:
            if line == date_str or line.startswith(f"{date_str} "):
                in_day = True
                yield line
        else:
            if not line:
                break

            yield line
