---
layout: default
title: "Chapter 5: Sessions and Context Management"
nav_order: 5
parent: Goose Tutorial
---


# Chapter 5: Sessions and Context Management

Welcome to **Chapter 5: Sessions and Context Management**. In this part of **Goose Tutorial: Extensible Open-Source AI Agent for Real Engineering Work**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains how Goose keeps long-running workflows productive without losing context quality.

## Learning Goals

- manage session lifecycle and naming cleanly
- use context compaction and strategies intentionally
- control runaway loops with max-turn governance
- tune session behavior for interactive vs headless usage

## Session Operations

| Action | CLI Example | Outcome |
|:-------|:------------|:--------|
| start session | `goose session` | interactive agent loop |
| start named session | `goose session -n release-hardening` | easier recovery/resume |
| web session | `goose web --open` | browser-based interaction |

## Context Management Model

Goose uses two layers:

1. auto-compaction near token thresholds
2. fallback context strategies when limits are still exceeded

Useful environment controls include:

- `GOOSE_AUTO_COMPACT_THRESHOLD`
- `GOOSE_CONTEXT_STRATEGY`
- `GOOSE_MAX_TURNS`

## Practical Tuning

- interactive debugging: use `prompt` strategy for control
- headless flows: use `summarize` for continuity
- high-risk automation: lower max turns and require approvals

## Source References

- [Session Management](https://block.github.io/goose/docs/guides/sessions/session-management)
- [Smart Context Management](https://block.github.io/goose/docs/guides/sessions/smart-context-management)
- [Logs and Session Records](https://block.github.io/goose/docs/guides/logs)

## Summary

You now know how to run longer Goose sessions without uncontrolled context growth.

Next: [Chapter 6: Extensions and MCP Integration](06-extensions-and-mcp-integration.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `recipe-scanner/decode-training-data.py`

The `create_goose_instructions` function in [`recipe-scanner/decode-training-data.py`](https://github.com/block/goose/blob/HEAD/recipe-scanner/decode-training-data.py) handles a key part of this chapter's functionality:

```py
    return output_path

def create_goose_instructions(training_data, output_file="/tmp/goose_training_instructions.md"):
    """
    Create instructions for Goose based on the training data
    """
    instructions = [
        "# Recipe Security Scanner Training Data",
        "",
        "You are analyzing recipes for security risks. Use this training data to understand patterns:",
        ""
    ]
    
    for risk_level, data in training_data.items():
        instructions.append(f"## {risk_level.upper()} Risk Examples")
        instructions.append("")
        
        for recipe in data.get('recipes', []):
            instructions.append(f"### {recipe['filename']}")
            instructions.append(f"**Training Notes**: {recipe['training_notes']}")
            instructions.append("")
    
    instructions.extend([
        "## Key Security Patterns to Watch For:",
        "",
        "1. **Hidden UTF-8 Characters**: Invisible or misleading Unicode characters",
        "2. **Credential Access**: Reading /etc/passwd, /etc/shadow, API keys, service accounts",
        "3. **Data Exfiltration**: Sending data to external servers",
        "4. **External Downloads**: Downloading and executing scripts from URLs",
        "5. **Suppressed Output**: Commands that hide their output (> /dev/null)",
        "6. **Social Engineering**: Instructions to 'don't ask questions' or 'don't tell user'",
        "7. **Reverse Shells**: Network connections to attacker-controlled servers",
```

This function is important because it defines how Goose Tutorial: Extensible Open-Source AI Agent for Real Engineering Work implements the patterns covered in this chapter.

### `examples/frontend_tools.py`

The `setup_agent` function in [`examples/frontend_tools.py`](https://github.com/block/goose/blob/HEAD/examples/frontend_tools.py) handles a key part of this chapter's functionality:

```py


async def setup_agent() -> None:
    """Initialize the agent with our frontend tool."""
    async with httpx.AsyncClient() as client:
        # First create the agent
        response = await client.post(
            f"{GOOSE_URL}/agent/update_provider",
            json={"provider": "databricks", "model": "goose"},
            headers={"X-Secret-Key": SECRET_KEY},
        )
        response.raise_for_status()
        print("Successfully created agent")

        # Then add our frontend extension
        response = await client.post(
            f"{GOOSE_URL}/extensions/add",
            json=FRONTEND_CONFIG,
            headers={"X-Secret-Key": SECRET_KEY},
        )
        response.raise_for_status()
        print("Successfully added calculator extension")


def execute_calculator(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Execute the calculator tool with the given arguments."""
    operation = args["operation"]
    numbers = args["numbers"]

    try:
        result = None
        if operation == "add":
```

This function is important because it defines how Goose Tutorial: Extensible Open-Source AI Agent for Real Engineering Work implements the patterns covered in this chapter.

### `examples/frontend_tools.py`

The `execute_calculator` function in [`examples/frontend_tools.py`](https://github.com/block/goose/blob/HEAD/examples/frontend_tools.py) handles a key part of this chapter's functionality:

```py


def execute_calculator(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Execute the calculator tool with the given arguments."""
    operation = args["operation"]
    numbers = args["numbers"]

    try:
        result = None
        if operation == "add":
            result = sum(numbers)
        elif operation == "subtract":
            result = numbers[0] - sum(numbers[1:])
        elif operation == "multiply":
            result = 1
            for n in numbers:
                result *= n
        elif operation == "divide":
            result = numbers[0]
            for n in numbers[1:]:
                result /= n

        # Return properly structured Content::Text variant
        return [
            {
                "type": "text",
                "text": str(result),
                "annotations": None,  # Required field in Rust struct
            }
        ]
    except Exception as e:
        return [
```

This function is important because it defines how Goose Tutorial: Extensible Open-Source AI Agent for Real Engineering Work implements the patterns covered in this chapter.

### `examples/frontend_tools.py`

The `get_tools` function in [`examples/frontend_tools.py`](https://github.com/block/goose/blob/HEAD/examples/frontend_tools.py) handles a key part of this chapter's functionality:

```py
        ]

def get_tools() -> Dict[str, Any]:
    with httpx.Client() as client:
        response = client.get(
            f"{GOOSE_URL}/agent/tools",
            headers={"X-Secret-Key": SECRET_KEY},
        )
        response.raise_for_status()
        return response.json()


def execute_enable_extension(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Execute the enable_extension tool.
    This function fetches available extensions, finds the one with the provided extension_name,
    and posts its configuration to the /extensions/add endpoint.
    """
    extension = args
    extension_name = extension.get("name")

    # Post the extension configuration to enable it
    with httpx.Client() as client:
        payload = {
            "type": extension.get("type"),
            "name": extension.get("name"),
            "cmd": extension.get("cmd"),
            "args": extension.get("args"),
            "envs": extension.get("envs", {}),
            "timeout": extension.get("timeout"),
            "bundled": extension.get("bundled"),
        }
```

This function is important because it defines how Goose Tutorial: Extensible Open-Source AI Agent for Real Engineering Work implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[create_goose_instructions]
    B[setup_agent]
    C[execute_calculator]
    D[get_tools]
    A --> B
    B --> C
    C --> D
```
