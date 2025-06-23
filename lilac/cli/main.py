import click

from lilac.adapters.yaml_io import load_resources

@click.group()
def main() -> None:
    """Lilac command line interface."""
    pass


@main.command()
@click.argument("directory", default="resource_files")
def validate(directory: str) -> None:
    """Validate resource YAML files in DIRECTORY."""
    try:
        resources = load_resources(directory)
    except Exception as exc:  # pragma: no cover - tested via CliRunner
        raise click.ClickException(str(exc))
    click.echo(f"Validated {len(resources)} resource files")

if __name__ == "__main__":
    main()
