from click.testing import CliRunner
from lilac.cli.main import main


def test_cli_invocation() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
