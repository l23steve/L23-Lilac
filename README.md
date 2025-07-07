# Lilac

Lilac (Live Infrastructure Lifecycle As Code) is a lightweight helper for
planning and deploying AWS resources. It describes the current infrastructure in
YAML and compares it with your desired state. The code base is intentionally
small and comes with a full test suite.

## Prerequisites

- Python 3.11 or higher

## Setup

Install the project in editable mode and run the checks:

```bash
pip install -e .
ruff check .
pytest
```

## Usage

After installation the `lilac` CLI is available:

```bash
lilac --help
```

## Features

- **Tagged discovery** – `lilac scan` only collects AWS resources that include a
  `namespace` tag matching the provided value.
- **Validation** – `lilac validate` can check resource files against the
  CloudFormation specification.
- **Change planning** – `lilac plan` compares your YAML definitions with the
  tagged resources found in AWS and reports creations, updates and deletions.
- **Deployment** – basic create, update and delete operations for supported
  resource types (currently S3 buckets).

## Scanning resources

Run `lilac scan --namespace <env>` to discover infrastructure resources tagged
with that namespace and write them as YAML files. The command uses
`scan_resources` which filters AWS resources by the `namespace` tag.

## Planning changes

Run `lilac plan --namespace <env>` to see what resources would be created,
updated or deleted compared to the tagged resources in AWS. Only resources with
the matching tag are considered.

## Deploying changes

Use `lilac deploy --namespace <env>` to apply a plan for resources tagged with
that namespace. The command lists all create and update operations, highlights
recreations, asks for confirmation and supports `--dry-run` to preview changes.

## What sets Lilac apart

Unlike many IaC solutions, Lilac originally focused purely on planning.
It now includes lightweight deployment capabilities for select resource types
via boto3 while still gathering detailed plans beforehand. The YAML format
mirrors AWS data closely and the small code base makes it easy to extend or
embed in other systems.
