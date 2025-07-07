from click.testing import CliRunner
from lilac.cli.main import main
from lilac.domain.models import Resource
from lilac.domain.plan import PlanAction
import importlib


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


def test_validate_with_spec_success(tmp_path, monkeypatch) -> None:
    valid = tmp_path / "valid.yaml"
    valid.write_text(
        """
        type: AWS::S3::Bucket
        namespace: default
        depends_on: []
        properties:
          BucketName: my-bucket
        """
    )

    spec = {"ResourceTypes": {"AWS::S3::Bucket": {"Properties": {"BucketName": {}}}}}
    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(cli_main, "load_spec", lambda region: spec)

    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(tmp_path), "--region", "us-east-1"])
    assert result.exit_code == 0
    assert "Validated 1 resource files" in result.output


def test_validate_with_spec_failure(tmp_path, monkeypatch) -> None:
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text(
        """
        type: AWS::S3::Bucket
        namespace: default
        depends_on: []
        properties:
          Wrong: value
        """
    )

    spec = {"ResourceTypes": {"AWS::S3::Bucket": {"Properties": {"BucketName": {}}}}}
    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(cli_main, "load_spec", lambda region: spec)

    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(tmp_path), "--region", "us-east-1"])
    assert result.exit_code != 0
    assert "Unknown property" in result.output


def test_scan_success(tmp_path, monkeypatch) -> None:
    res = Resource(
        resource_type="s3-bucket",
        namespace="prod",
        depends_on=[],
        properties={"name": "bucket"},
    )
    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(cli_main, "scan_resources", lambda ns: [res])

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["scan", "--namespace", "prod", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 0
    assert (tmp_path / "s3-bucket" / "bucket.yaml").exists()


def test_scan_sanitizes_name(tmp_path, monkeypatch) -> None:
    res = Resource(
        resource_type="s3-bucket",
        namespace="prod",
        depends_on=[],
        properties={"name": "my bucket/v1"},
    )
    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(cli_main, "scan_resources", lambda ns: [res])

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["scan", "--namespace", "prod", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 0
    assert (tmp_path / "s3-bucket" / "my_bucket_v1.yaml").exists()


def test_scan_failure(monkeypatch) -> None:
    def bad_scan(ns: str) -> list[Resource]:
        raise RuntimeError("boom")

    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(cli_main, "scan_resources", bad_scan)

    runner = CliRunner()
    result = runner.invoke(main, ["scan", "--namespace", "prod"])

    assert result.exit_code != 0
    assert "boom" in result.output


def test_scan_requires_namespace() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["scan"])
    assert result.exit_code != 0
    assert "--namespace" in result.output


def test_plan_success(tmp_path, monkeypatch) -> None:
    res = Resource("s3-bucket", "prod", [], {"name": "bucket"})
    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(
        cli_main,
        "plan_changes",
        lambda d, ns: [PlanAction("create", res)],
    )

    runner = CliRunner()
    result = runner.invoke(main, ["plan", str(tmp_path), "--namespace", "prod"])

    assert result.exit_code == 0
    assert "CREATE" in result.output


def test_plan_failure(monkeypatch) -> None:
    cli_main = importlib.import_module("lilac.cli.main")

    def bad_plan(d: str, ns: str):
        raise RuntimeError("boom")

    monkeypatch.setattr(cli_main, "plan_changes", bad_plan)

    runner = CliRunner()
    result = runner.invoke(main, ["plan", "dir", "--namespace", "prod"])

    assert result.exit_code != 0
    assert "boom" in result.output


def test_deploy_dry_run(monkeypatch) -> None:
    res = Resource("s3-bucket", "prod", [], {"name": "bucket"})
    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(
        cli_main,
        "plan_changes",
        lambda d, ns: [PlanAction("update", res)],
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["deploy", "--namespace", "prod", "--dry-run"],
    )

    assert result.exit_code == 0
    assert "UPDATE" in result.output
    assert "Dry run" in result.output


def test_deploy_confirmation(monkeypatch) -> None:
    res = Resource("s3-bucket", "prod", [], {"name": "bucket"})
    cli_main = importlib.import_module("lilac.cli.main")
    monkeypatch.setattr(
        cli_main,
        "plan_changes",
        lambda d, ns: [PlanAction("update", res)],
    )
    monkeypatch.setattr(
        cli_main,
        "deploy_service",
        lambda d, ns: [PlanAction("update", res)],
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["deploy", "--namespace", "prod"],
        input="y\n",
    )

    assert result.exit_code == 0
    assert "Apply these changes?" in result.output

