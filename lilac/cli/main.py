import click
from pathlib import Path

from lilac.adapters import load_resources, load_spec, write_resource
from lilac.domain.validation import validate_against_spec
from lilac.domain.models import Resource
from lilac.domain.plan import PlanAction
from lilac.services import plan_changes, scan_resources, deploy as deploy_service
from lilac.utils.helpers import sanitize_filename

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
            dir_path = out_dir / res.resource_type
            dir_path.mkdir(parents=True, exist_ok=True)
            base_name = str(
                res.properties.get("name") or res.properties.get("id") or idx
            )
            safe_name = sanitize_filename(base_name)
            file_path = dir_path / f"{safe_name}.yaml"
            write_resource(res, file_path)
    except Exception as exc:  # pragma: no cover - tested via CliRunner
        raise click.ClickException(str(exc))
    click.echo(f"Wrote {len(resources)} resources to {out_dir}")


@main.command()
@click.argument("directory", default="resource_files")
@click.option("--namespace", required=True, help="Namespace to plan.")
def plan(directory: str, namespace: str) -> None:
    """Show planned changes between DIRECTORY and AWS."""
    try:
        actions = plan_changes(directory, namespace)
        for act in actions:
            click.echo(f"{act.action.upper()}: {act.resource.resource_type}")
    except Exception as exc:  # pragma: no cover - tested via CliRunner
        raise click.ClickException(str(exc))
    click.echo(f"Planned {len(actions)} actions")


@main.command()
@click.argument("directory", default="resource_files")
@click.option("--namespace", required=True, help="Namespace to deploy.")
@click.option("--dry-run", is_flag=True, help="Show actions without applying changes.")
def deploy(directory: str, namespace: str, dry_run: bool) -> None:
    """Deploy changes based on resource files."""
    try:
        actions = plan_changes(directory, namespace)

        def _ident(res: Resource) -> str:
            return str(
                res.properties.get("name")
                or res.properties.get("id")
                or res.properties.get("arn")
                or "?"
            )

        creates = [a for a in actions if a.action == "create"]
        deletes = [a for a in actions if a.action == "delete"]
        updates = [a for a in actions if a.action == "update"]

        recreate: list[PlanAction] = []
        used_del: set[int] = set()
        remaining_creates: list[PlanAction] = []
        for c_idx, c in enumerate(creates):
            cid = _ident(c.resource)
            match = None
            for d_idx, d in enumerate(deletes):
                if d_idx in used_del:
                    continue
                if (
                    d.resource.resource_type == c.resource.resource_type
                    and _ident(d.resource) == cid
                ):
                    match = d_idx
                    break
            if match is not None:
                recreate.append(c)
                used_del.add(match)
            else:
                remaining_creates.append(c)

        remaining_deletes = [d for idx, d in enumerate(deletes) if idx not in used_del]

        for r in recreate:
            click.echo(
                f"RECREATE: {r.resource.resource_type} {_ident(r.resource)}"
            )
        for u in updates:
            click.echo(
                f"UPDATE: {u.resource.resource_type} {_ident(u.resource)} (in-place)"
            )
        for c in remaining_creates:
            click.echo(f"CREATE: {c.resource.resource_type} {_ident(c.resource)}")
        for d in remaining_deletes:
            click.echo(f"DELETE: {d.resource.resource_type} {_ident(d.resource)}")

        if dry_run:
            click.echo("Dry run: no changes applied.")
            return

        if not click.confirm("Apply these changes?", default=False):
            click.echo("Aborted!")
            return

        deploy_service(directory, namespace)
    except Exception as exc:  # pragma: no cover - tested via CliRunner
        raise click.ClickException(str(exc))
    click.echo(f"Deployed {len(actions)} actions")

if __name__ == "__main__":
    main()
