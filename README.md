# Lilac

A minimal scaffold for the Lilac project. This repository provides the basic
package structure, testing setup, and continuous integration workflow.

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

## Scanning resources

Run `lilac scan` to discover infrastructure resources and write them as YAML
files. The command calls the `scan_resources` function from
`lilac.services.scanner` to perform the AWS lookup.
