from lilac.cli.main import main


def test_cli_main_import() -> None:
    assert callable(main)
