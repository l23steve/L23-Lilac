import click
from pathlib import Path

from lilac.adapters import load_resources, load_spec, write_resource
from lilac.domain.validation import validate_against_spec
from lilac.services import scan_resources

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


@main.command()
@click.option("--namespace", required=True, help="Namespace to scan.")
@click.option(
    "--output-dir",
    default="resource_files",
    help="Directory to write resources.",
)
def scan(namespace: str, output_dir: str) -> None:
    """Scan AWS and write discovered resources."""
    try:
        resources = scan_resources(namespace)
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for idx, res in enumerate(resources):
            file_path = out_dir / f"{res.resource_type}_{idx}.yaml"
            write_resource(res, file_path)
    except Exception as exc:  # pragma: no cover - tested via CliRunner
        raise click.ClickException(str(exc))
    click.echo(f"Wrote {len(resources)} resources to {out_dir}")

if __name__ == "__main__":
    main()
