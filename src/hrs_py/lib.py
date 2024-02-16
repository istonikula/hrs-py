import re
from collections import defaultdict
from collections.abc import Iterator
from datetime import date, datetime, timedelta
from typing import DefaultDict, Dict, List, Tuple

from hrs_py.types import Line, Tag


def find_and_collect_day(lines: Iterator[str], date: date) -> Iterator[str]:
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


def process_lines(lines: List[str]) -> Tuple[List[Tuple[timedelta, Line]], Dict[Tag, List[timedelta]]]:
    line_re = re.compile(r"^([0-9\.]{1,5})-([0-9\.]{1,5})\s+(\[.*?\])?.*$")
    durations: List[Tuple[timedelta, Line]] = []
    durations_by_tag: DefaultDict[Tag, List[timedelta]] = defaultdict(list)
    prev_tag: Tag | None = None
    today = datetime.now().date()

    def parse(time: str) -> datetime:
        time_with_mins = time if "." in time else f"{time}.00"
        return datetime.strptime(f"{today} {time_with_mins}", "%Y-%m-%d %H.%M")

    for line in lines:
        match = line_re.match(line)
        if match:
            groups = match.groups()

            start: str = groups[0]
            end: str = groups[1]
            tag: Tag = Tag(groups[2] if groups[2] is not None else line[len(f"{start}-{end} ") :])

            if prev_tag and tag.startswith('-"-'):
                tag = prev_tag
            else:
                prev_tag = tag

            duration = parse(end) - parse(start)
            durations.append((duration, Line(line)))
            durations_by_tag[tag].append(duration)

    return durations, durations_by_tag
