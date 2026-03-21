---
layout: default
title: "Chapter 6: MCP Server Patterns and Toolkit Control"
nav_order: 6
parent: Composio Tutorial
---


# Chapter 6: MCP Server Patterns and Toolkit Control

Welcome to **Chapter 6: MCP Server Patterns and Toolkit Control**. In this part of **Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on MCP integration design, including when to use dynamic session MCP versus fixed single-toolkit MCP configurations.

## Learning Goals

- choose the right MCP pattern for your product and governance constraints
- avoid over-scoped server exposure in MCP clients
- map single-toolkit MCP limitations to operational requirements
- define secure rollout and lifecycle management for MCP endpoints

## MCP Pattern Comparison

| Pattern | Strength | Tradeoff |
|:--------|:---------|:---------|
| session-backed dynamic MCP | broad flexible capability with context-aware discovery | needs stronger runtime governance |
| single-toolkit MCP configs | tighter scope and easier compliance review | less flexibility and can increase config overhead |

## Practical Controls

- gate allowed toolkits/tools by workload profile
- isolate high-risk toolkits behind separate MCP configurations
- track MCP endpoint ownership and rotation policy
- maintain fallback paths when upstream toolkits degrade

## Source References

- [Quickstart MCP Flow](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/quickstart.mdx)
- [Single Toolkit MCP](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/single-toolkit-mcp.mdx)
- [MCP Troubleshooting](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/troubleshooting/mcp.mdx)

## Summary

You now have a decision framework for MCP architecture choices in Composio deployments.

Next: [Chapter 7: Triggers, Webhooks, and Event Automation](07-triggers-webhooks-and-event-automation.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `python/scripts/generate-docs.py`

The `docs` class in [`python/scripts/generate-docs.py`](https://github.com/ComposioHQ/composio/blob/HEAD/python/scripts/generate-docs.py) handles a key part of this chapter's functionality:

```py

Generates MDX documentation from Python source code using griffe.
Output is written to the docs content directory.

Run: cd python && uv run --with griffe python scripts/generate-docs.py
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

try:
    import griffe
except ImportError:
    print("Error: griffe not installed. Run: pip install griffe")
    raise SystemExit(1)

# Paths
SCRIPT_DIR = Path(__file__).parent
PACKAGE_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = (
    PACKAGE_DIR.parent / "docs" / "content" / "reference" / "sdk-reference" / "python"
)

# GitHub base URL for source links
GITHUB_BASE = "https://github.com/composiohq/composio/blob/next/python"

# Decorators to document
```

This class is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.

### `python/scripts/generate-docs.py`

The `to_kebab_case` function in [`python/scripts/generate-docs.py`](https://github.com/ComposioHQ/composio/blob/HEAD/python/scripts/generate-docs.py) handles a key part of this chapter's functionality:

```py


def to_kebab_case(name: str) -> str:
    """Convert PascalCase to kebab-case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


def escape_yaml_string(s: str) -> str:
    """Escape a string for YAML frontmatter."""
    if any(c in s for c in [":", '"', "'", "\n", "#", "{", "}"]):
        return f'"{s.replace(chr(34), chr(92) + chr(34))}"'
    return s


def get_source_link(obj: griffe.Object) -> str | None:
    """Get GitHub source link for an object."""
    if not hasattr(obj, "filepath") or not obj.filepath:
        return None
    try:
        raw_filepath = obj.filepath
        # Handle case where filepath might be a list (griffe edge case)
        if isinstance(raw_filepath, list):
            resolved_path: Path | None = raw_filepath[0] if raw_filepath else None
        else:
            resolved_path = raw_filepath
        if not resolved_path:
            return None
        rel_path = resolved_path.relative_to(PACKAGE_DIR)
    except ValueError:
        return None
    line = obj.lineno if hasattr(obj, "lineno") and obj.lineno else 1
```

This function is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.

### `python/scripts/generate-docs.py`

The `escape_yaml_string` function in [`python/scripts/generate-docs.py`](https://github.com/ComposioHQ/composio/blob/HEAD/python/scripts/generate-docs.py) handles a key part of this chapter's functionality:

```py


def escape_yaml_string(s: str) -> str:
    """Escape a string for YAML frontmatter."""
    if any(c in s for c in [":", '"', "'", "\n", "#", "{", "}"]):
        return f'"{s.replace(chr(34), chr(92) + chr(34))}"'
    return s


def get_source_link(obj: griffe.Object) -> str | None:
    """Get GitHub source link for an object."""
    if not hasattr(obj, "filepath") or not obj.filepath:
        return None
    try:
        raw_filepath = obj.filepath
        # Handle case where filepath might be a list (griffe edge case)
        if isinstance(raw_filepath, list):
            resolved_path: Path | None = raw_filepath[0] if raw_filepath else None
        else:
            resolved_path = raw_filepath
        if not resolved_path:
            return None
        rel_path = resolved_path.relative_to(PACKAGE_DIR)
    except ValueError:
        return None
    line = obj.lineno if hasattr(obj, "lineno") and obj.lineno else 1
    return f"{GITHUB_BASE}/{rel_path}#L{line}"


def format_type(annotation: Any) -> str:
    """Format a type annotation to readable string."""
    if annotation is None:
```

This function is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.

### `python/scripts/generate-docs.py`

The `get_source_link` function in [`python/scripts/generate-docs.py`](https://github.com/ComposioHQ/composio/blob/HEAD/python/scripts/generate-docs.py) handles a key part of this chapter's functionality:

```py


def get_source_link(obj: griffe.Object) -> str | None:
    """Get GitHub source link for an object."""
    if not hasattr(obj, "filepath") or not obj.filepath:
        return None
    try:
        raw_filepath = obj.filepath
        # Handle case where filepath might be a list (griffe edge case)
        if isinstance(raw_filepath, list):
            resolved_path: Path | None = raw_filepath[0] if raw_filepath else None
        else:
            resolved_path = raw_filepath
        if not resolved_path:
            return None
        rel_path = resolved_path.relative_to(PACKAGE_DIR)
    except ValueError:
        return None
    line = obj.lineno if hasattr(obj, "lineno") and obj.lineno else 1
    return f"{GITHUB_BASE}/{rel_path}#L{line}"


def format_type(annotation: Any) -> str:
    """Format a type annotation to readable string."""
    if annotation is None:
        return "Any"

    type_str = str(annotation)
    # Clean up common prefixes
    type_str = type_str.replace("typing.", "").replace("typing_extensions.", "")
    type_str = type_str.replace("composio.client.types.", "")
    type_str = re.sub(r"\bt\.", "", type_str)
```

This function is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[docs]
    B[to_kebab_case]
    C[escape_yaml_string]
    D[get_source_link]
    E[format_type]
    A --> B
    B --> C
    C --> D
    D --> E
```
