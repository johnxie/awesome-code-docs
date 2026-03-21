---
layout: default
title: "Chapter 5: API and MCP Deployment"
nav_order: 5
parent: Langflow Tutorial
---


# Chapter 5: API and MCP Deployment

Welcome to **Chapter 5: API and MCP Deployment**. In this part of **Langflow Tutorial: Visual AI Agent and Workflow Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Langflow can expose workflows as APIs and MCP tools, making flows reusable across applications and agents.

## Deployment Surfaces

| Surface | Use Case |
|:--------|:---------|
| API endpoint | app/service integration |
| MCP server | tool interoperability for agent ecosystems |

## Deployment Checklist

- version flow definitions
- enforce auth and rate limits
- log invocation traces
- validate input/output schemas

## Source References

- [Langflow Deployment Overview](https://docs.langflow.org/deployment-overview)
- [Langflow README](https://github.com/langflow-ai/langflow)

## Summary

You now have a practical approach for publishing Langflow workflows as reusable runtime interfaces.

Next: [Chapter 6: Observability and Security](06-observability-and-security.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `scripts/migrate_secret_key.py`

The `get_default_database_url` function in [`scripts/migrate_secret_key.py`](https://github.com/langflow-ai/langflow/blob/HEAD/scripts/migrate_secret_key.py) handles a key part of this chapter's functionality:

```py


def get_default_database_url(config_dir: Path) -> str | None:
    """Get database URL from default SQLite location."""
    default_db = config_dir / "langflow.db"
    if default_db.exists():
        return f"sqlite:///{default_db}"
    return None


DATABASE_URL_DISPLAY_LENGTH = 50


def migrate(
    config_dir: Path,
    database_url: str,
    old_key: str | None = None,
    new_key: str | None = None,
    *,
    dry_run: bool = False,
):
    """Run the secret key migration.

    Args:
        config_dir: Path to Langflow config directory containing secret_key file.
        database_url: SQLAlchemy database connection URL.
        old_key: Current secret key. If None, reads from config_dir/secret_key.
        new_key: New secret key. If None, generates a secure random key.
        dry_run: If True, simulates migration without making changes.

    The migration runs as an atomic transaction - either all database changes
    succeed or none are applied. Key files are only modified after successful
```

This function is important because it defines how Langflow Tutorial: Visual AI Agent and Workflow Platform implements the patterns covered in this chapter.

### `scripts/migrate_secret_key.py`

The `migrate` function in [`scripts/migrate_secret_key.py`](https://github.com/langflow-ai/langflow/blob/HEAD/scripts/migrate_secret_key.py) handles a key part of this chapter's functionality:

```py

Usage:
    uv run python scripts/migrate_secret_key.py --help
    uv run python scripts/migrate_secret_key.py --dry-run
    uv run python scripts/migrate_secret_key.py --database-url postgresql://...
"""

import argparse
import base64
import json
import os
import platform
import random
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from platformdirs import user_cache_dir
from sqlalchemy import create_engine, text

MINIMUM_KEY_LENGTH = 32
SENSITIVE_AUTH_FIELDS = ["oauth_client_secret", "api_key"]
# Must match langflow.services.variable.constants.CREDENTIAL_TYPE
CREDENTIAL_TYPE = "Credential"


def get_default_config_dir() -> Path:
    """Get the default Langflow config directory using platformdirs."""
    return Path(user_cache_dir("langflow", "langflow"))

```

This function is important because it defines how Langflow Tutorial: Visual AI Agent and Workflow Platform implements the patterns covered in this chapter.

### `scripts/migrate_secret_key.py`

The `main` function in [`scripts/migrate_secret_key.py`](https://github.com/langflow-ai/langflow/blob/HEAD/scripts/migrate_secret_key.py) handles a key part of this chapter's functionality:

```py


def main():
    default_config = get_config_dir()

    parser = argparse.ArgumentParser(
        description="Migrate Langflow encrypted data to a new secret key",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview what will be migrated
  %(prog)s --dry-run

  # Run migration with defaults
  %(prog)s

  # Custom database and config
  %(prog)s --database-url postgresql://user:pass@host/db --config-dir /etc/langflow  # pragma: allowlist secret

  # Provide keys explicitly
  %(prog)s --old-key "current-key" --new-key "replacement-key"
        """,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying anything",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
```

This function is important because it defines how Langflow Tutorial: Visual AI Agent and Workflow Platform implements the patterns covered in this chapter.

### `scripts/generate_coverage_config.py`

The `extract_sidebar_bundles` function in [`scripts/generate_coverage_config.py`](https://github.com/langflow-ai/langflow/blob/HEAD/scripts/generate_coverage_config.py) handles a key part of this chapter's functionality:

```py


def extract_sidebar_bundles(frontend_path: Path) -> set[str]:
    """Extract component names from SIDEBAR_BUNDLES in styleUtils.ts."""
    style_utils_path = frontend_path / "src/utils/styleUtils.ts"

    if not style_utils_path.exists():
        print(f"Warning: styleUtils.ts not found at {style_utils_path}")
        return set()

    bundle_names = set()

    with style_utils_path.open(encoding="utf-8") as f:
        content = f.read()

    # Find SIDEBAR_BUNDLES array
    sidebar_match = re.search(r"export const SIDEBAR_BUNDLES = \[(.*?)\];", content, re.DOTALL)
    if not sidebar_match:
        print("Warning: SIDEBAR_BUNDLES not found in styleUtils.ts")
        return set()

    bundles_content = sidebar_match.group(1)

    # Extract name fields using regex
    name_matches = re.findall(r'name:\s*["\']([^"\']+)["\']', bundles_content)

    for name in name_matches:
        bundle_names.add(name)

    print(f"Found {len(bundle_names)} bundled components from SIDEBAR_BUNDLES")
    return bundle_names

```

This function is important because it defines how Langflow Tutorial: Visual AI Agent and Workflow Platform implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[get_default_database_url]
    B[migrate]
    C[main]
    D[extract_sidebar_bundles]
    A --> B
    B --> C
    C --> D
```
