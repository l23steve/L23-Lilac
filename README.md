# Lilac

Lilac (Live Infrastructure Lifecycle As Code) is a lightweight infrastructure-as-code helper. While many IaC tools
focus on provisioning, Lilac concentrates on *introspection*. It can scan an AWS
environment, describe resources in YAML and produce a plan of what would change
if those files were applied. The project ships with a minimal code base,
complete tests and continuous integration workflow.

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

- **Resource discovery** – `lilac scan` queries AWS APIs and serializes the
  results as YAML files that are easy to inspect and version.
- **Validation** – `lilac validate` can check resources against the
  CloudFormation specification, ensuring property names and types are correct.
- **Change planning** – `lilac plan` compares your YAML definitions with the
  live environment and reports resources to create, update or delete.
- **Dependency ordering** – resources can declare dependencies and Lilac uses a
  graph to process them in a safe order.
- **Detail stripping** – transient `details` fields are ignored during diffs so
  insignificant changes do not cause noise.

## Scanning resources

Run `lilac scan` to discover infrastructure resources and write them as YAML
files. The command calls the `scan_resources` function from
`lilac.services.scanner` to perform the AWS lookup.

## Planning changes

Run `lilac plan` to see what resources would be created, updated or deleted when comparing your YAML files to the live AWS environment. The command relies on `scan_resources` to discover the current state.

## What sets Lilac apart

Unlike many IaC solutions, Lilac does not apply changes directly. It focuses on
gathering information and producing actionable plans so you can manage updates
manually or integrate them into your existing tooling. The YAML format mirrors
AWS data closely and the small code base makes it easy to extend or embed in
other systems.
