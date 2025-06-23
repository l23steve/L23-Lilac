import click

from lilac.adapters import load_resources, load_spec
from lilac.domain.validation import validate_against_spec

@click.group()
def main() -> None:
    """Lilac command line interface."""
    pass


@main.command()
@click.argument("directory", default="resource_files")
@click.option("--region", help="Validate against AWS spec for REGION.")
def validate(directory: str, region: str | None) -> None:
    """Validate resource YAML files in DIRECTORY."""
    try:
        resources = load_resources(directory)
        if region:
            spec = load_spec(region)
            for res in resources:
                validate_against_spec(res, spec)
    except Exception as exc:  # pragma: no cover - tested via CliRunner
        raise click.ClickException(str(exc))
    click.echo(f"Validated {len(resources)} resource files")

if __name__ == "__main__":
    main()
