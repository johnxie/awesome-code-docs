---
layout: default
title: "Chapter 5: Local Integration: Claude Desktop and Inspector"
nav_order: 5
parent: Create Python Server Tutorial
---


# Chapter 5: Local Integration: Claude Desktop and Inspector

Welcome to **Chapter 5: Local Integration: Claude Desktop and Inspector**. In this part of **Create Python Server Tutorial: Scaffold and Ship MCP Servers with uvx**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains local integration and debugging workflows for generated servers.

## Learning Goals

- configure generated server commands for Claude Desktop
- use Inspector workflows for stdio debugging and validation
- test development vs published server command paths
- reduce time-to-diagnosis for integration issues

## Integration Modes

| Mode | Command Pattern |
|:-----|:----------------|
| development | `uv --directory <server-dir> run <server-name>` |
| published | `uvx <server-name>` |

## Source References

- [Template README - Claude Desktop Configuration](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2#claude-desktop)
- [Template README - Debugging](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2#debugging)

## Summary

You now have a working local integration and debugging strategy for scaffolded servers.

Next: [Chapter 6: Customization and Extension Patterns](06-customization-and-extension-patterns.md)

## Source Code Walkthrough

### `src/create_mcp_server/__init__.py`

The `has_claude_app` function in [`src/create_mcp_server/__init__.py`](https://github.com/modelcontextprotocol/create-python-server/blob/HEAD/src/create_mcp_server/__init__.py) handles a key part of this chapter's functionality:

```py


def has_claude_app() -> bool:
    return get_claude_config_path() is not None


def update_claude_config(project_name: str, project_path: Path) -> bool:
    """Add the project to the Claude config if possible"""
    config_dir = get_claude_config_path()
    if not config_dir:
        return False

    config_file = config_dir / "claude_desktop_config.json"
    if not config_file.exists():
        return False

    try:
        config = json.loads(config_file.read_text())
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        if project_name in config["mcpServers"]:
            click.echo(
                f"⚠️ Warning: {project_name} already exists in Claude.app configuration",
                err=True,
            )
            click.echo(f"Settings file location: {config_file}", err=True)
            return False

        config["mcpServers"][project_name] = {
            "command": "uv",
            "args": ["--directory", str(project_path), "run", project_name],
```

This function is important because it defines how Create Python Server Tutorial: Scaffold and Ship MCP Servers with uvx implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[has_claude_app]
```
