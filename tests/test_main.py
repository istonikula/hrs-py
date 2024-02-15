from typer.testing import CliRunner

from hrs_py.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["tests/data/hours.txt", "1.3"])
    assert result.exit_code == 0
