from click.testing import CliRunner
from lilac.cli.main import main


def test_cli_invocation() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_validate_success(tmp_path) -> None:
    valid = tmp_path / "valid.yaml"
    valid.write_text(
        """
        type: s3-bucket
        namespace: default
        depends_on: []
        properties: {}
        """
    )

    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(tmp_path)])
    assert result.exit_code == 0
    assert "Validated 1 resource files" in result.output


def test_validate_failure(tmp_path) -> None:
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text(
        """
        type: s3-bucket
        namespace: default
        properties: {}
        """
    )

    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(tmp_path)])
    assert result.exit_code != 0
    assert "Missing required field" in result.output
