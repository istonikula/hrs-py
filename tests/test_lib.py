from datetime import datetime
from hrs_py.lib import find_and_collect_day


def test_find_and_collect_day():
    def lines():
        return iter(
            """


27.2
--
foo


28.2 (day info)
--
bar

1.3  day info
--
baz
""".splitlines()
        )

    assert list(find_and_collect_day(iter([]), __d("27.2"))) == []
    assert list(find_and_collect_day(lines(), __d("27.2"))) == ["27.2", "--", "foo"]
    assert list(find_and_collect_day(lines(), __d("28.2"))) == ["28.2 (day info)", "--", "bar"]
    assert list(find_and_collect_day(lines(), __d("28.02"))) == ["28.2 (day info)", "--", "bar"]
    assert list(find_and_collect_day(lines(), __d("1.3"))) == ["1.3  day info", "--", "baz"]


def __d(date: str):
    return datetime.strptime(date, "%d.%m")
