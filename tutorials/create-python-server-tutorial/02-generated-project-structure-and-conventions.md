---
layout: default
title: "Chapter 2: Generated Project Structure and Conventions"
nav_order: 2
parent: Create Python Server Tutorial
---


# Chapter 2: Generated Project Structure and Conventions

Welcome to **Chapter 2: Generated Project Structure and Conventions**. In this part of **Create Python Server Tutorial: Scaffold and Ship MCP Servers with uvx**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains generated file layout and how each piece supports maintainable server development.

## Learning Goals

- navigate scaffolded project structure (`README`, `pyproject.toml`, `src/*`)
- map template files to runtime behavior
- understand naming/package conventions used by the generator
- keep customization changes isolated from generated boilerplate

## Structure Overview

| Path | Purpose |
|:-----|:--------|
| `README.md` | usage and integration instructions |
| `pyproject.toml` | packaging and dependency definition |
| `src/<package>/server.py` | MCP primitives and handler logic |

## Source References

- [Create Python Server README](https://github.com/modelcontextprotocol/create-python-server/blob/main/README.md)
- [Template README](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2)

## Summary

You now have a structural map for generated MCP Python server projects.

Next: [Chapter 3: Template Server Architecture: Resources, Prompts, and Tools](03-template-server-architecture-resources-prompts-and-tools.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `src/create_mcp_server/__init__.py`

The `check_uv_version` function in [`src/create_mcp_server/__init__.py`](https://github.com/modelcontextprotocol/create-python-server/blob/HEAD/src/create_mcp_server/__init__.py) handles a key part of this chapter's functionality:

```py


def check_uv_version(required_version: str) -> str | None:
    """Check if uv is installed and has minimum version"""
    try:
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip()
        match = re.match(r"uv (\d+\.\d+\.\d+)", version)
        if match:
            version_num = match.group(1)
            if parse(version_num) >= parse(required_version):
                return version
        return None
    except subprocess.CalledProcessError:
        click.echo("❌ Error: Failed to check uv version.", err=True)
        sys.exit(1)
    except FileNotFoundError:
        return None


def ensure_uv_installed() -> None:
    """Ensure uv is installed at minimum version"""
    if check_uv_version(MIN_UV_VERSION) is None:
        click.echo(
            f"❌ Error: uv >= {MIN_UV_VERSION} is required but not installed.", err=True
        )
        click.echo("To install, visit: https://github.com/astral-sh/uv", err=True)
        sys.exit(1)


```

This function is important because it defines how Create Python Server Tutorial: Scaffold and Ship MCP Servers with uvx implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[check_uv_version]
```
