---
layout: default
title: "Chapter 6: Customization and Extension Patterns"
nav_order: 6
parent: Create Python Server Tutorial
---


# Chapter 6: Customization and Extension Patterns

Welcome to **Chapter 6: Customization and Extension Patterns**. In this part of **Create Python Server Tutorial: Scaffold and Ship MCP Servers with uvx**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers practical ways to evolve generated scaffolds into domain-specific services.

## Learning Goals

- extend default primitive handlers with domain logic safely
- preserve protocol contracts while changing storage or workflows
- keep template-origin code maintainable over time
- avoid coupling business logic to scaffold assumptions

## Extension Strategy

1. isolate domain logic in dedicated modules/services
2. keep handler boundaries thin and protocol-focused
3. add schema validation and error mapping early
4. maintain behavior tests as templates diverge

## Source References

- [Template Server Implementation](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/server.py.jinja2)
- [Create Python Server README](https://github.com/modelcontextprotocol/create-python-server/blob/main/README.md)

## Summary

You now have an extension model for safely evolving generated MCP servers.

Next: [Chapter 7: Quality, Security, and Contribution Workflows](07-quality-security-and-contribution-workflows.md)

## Source Code Walkthrough

### `src/create_mcp_server/__init__.py`

The `update_claude_config` function in [`src/create_mcp_server/__init__.py`](https://github.com/modelcontextprotocol/create-python-server/blob/HEAD/src/create_mcp_server/__init__.py) handles a key part of this chapter's functionality:

```py


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
        }

        config_file.write_text(json.dumps(config, indent=2))
        click.echo(f"✅ Added {project_name} to Claude.app configuration")
```

This function is important because it defines how Create Python Server Tutorial: Scaffold and Ship MCP Servers with uvx implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[update_claude_config]
```
