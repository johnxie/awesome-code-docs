---
layout: default
title: "Chapter 3: Tooling and Approval Workflow"
nav_order: 3
parent: Mistral Vibe Tutorial
---


# Chapter 3: Tooling and Approval Workflow

Welcome to **Chapter 3: Tooling and Approval Workflow**. In this part of **Mistral Vibe Tutorial: Minimal CLI Coding Agent by Mistral**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Vibe uses a tool-driven workflow for file operations, search, shell execution, and user interaction.

## Core Tool Classes

| Tool Class | Example Capabilities |
|:-----------|:---------------------|
| file tools | read/write/patch files |
| shell tools | command execution in terminal context |
| search tools | grep and project search |
| coordination tools | todo tracking and user questions |

## Approval Model

Default interactive mode is approval-aware, while auto-approve settings should be constrained to trusted contexts.

## Source References

- [Mistral Vibe README: toolset overview](https://github.com/mistralai/mistral-vibe/blob/main/README.md)

## Summary

You now understand how Vibe turns prompts into controlled tool execution loops.

Next: [Chapter 4: Skills and Slash Command Extensions](04-skills-and-slash-command-extensions.md)

## Source Code Walkthrough

### `vibe/core/types.py`

The `AgentStats` class in [`vibe/core/types.py`](https://github.com/mistralai/mistral-vibe/blob/HEAD/vibe/core/types.py) handles a key part of this chapter's functionality:

```py


class AgentStats(BaseModel):
    steps: int = 0
    session_prompt_tokens: int = 0
    session_completion_tokens: int = 0
    tool_calls_agreed: int = 0
    tool_calls_rejected: int = 0
    tool_calls_failed: int = 0
    tool_calls_succeeded: int = 0

    context_tokens: int = 0

    last_turn_prompt_tokens: int = 0
    last_turn_completion_tokens: int = 0
    last_turn_duration: float = 0.0
    tokens_per_second: float = 0.0

    input_price_per_million: float = 0.0
    output_price_per_million: float = 0.0

    _listeners: dict[str, Callable[[AgentStats], None]] = PrivateAttr(
        default_factory=dict
    )

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name in self._listeners:
            self._listeners[name](self)

    def trigger_listeners(self) -> None:
        for listener in self._listeners.values():
```

This class is important because it defines how Mistral Vibe Tutorial: Minimal CLI Coding Agent by Mistral implements the patterns covered in this chapter.

### `vibe/core/types.py`

The `SessionInfo` class in [`vibe/core/types.py`](https://github.com/mistralai/mistral-vibe/blob/HEAD/vibe/core/types.py) handles a key part of this chapter's functionality:

```py


class SessionInfo(BaseModel):
    session_id: str
    start_time: str
    message_count: int
    stats: AgentStats
    save_dir: str


class SessionMetadata(BaseModel):
    session_id: str
    start_time: str
    end_time: str | None
    git_commit: str | None
    git_branch: str | None
    environment: dict[str, str | None]
    username: str


class ClientMetadata(BaseModel):
    name: str
    version: str


class EntrypointMetadata(BaseModel):
    agent_entrypoint: Literal["cli", "acp", "programmatic"]
    agent_version: str
    client_name: str
    client_version: str


```

This class is important because it defines how Mistral Vibe Tutorial: Minimal CLI Coding Agent by Mistral implements the patterns covered in this chapter.

### `vibe/core/types.py`

The `SessionMetadata` class in [`vibe/core/types.py`](https://github.com/mistralai/mistral-vibe/blob/HEAD/vibe/core/types.py) handles a key part of this chapter's functionality:

```py


class SessionMetadata(BaseModel):
    session_id: str
    start_time: str
    end_time: str | None
    git_commit: str | None
    git_branch: str | None
    environment: dict[str, str | None]
    username: str


class ClientMetadata(BaseModel):
    name: str
    version: str


class EntrypointMetadata(BaseModel):
    agent_entrypoint: Literal["cli", "acp", "programmatic"]
    agent_version: str
    client_name: str
    client_version: str


StrToolChoice = Literal["auto", "none", "any", "required"]


class AvailableFunction(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]

```

This class is important because it defines how Mistral Vibe Tutorial: Minimal CLI Coding Agent by Mistral implements the patterns covered in this chapter.

### `vibe/core/types.py`

The `ClientMetadata` class in [`vibe/core/types.py`](https://github.com/mistralai/mistral-vibe/blob/HEAD/vibe/core/types.py) handles a key part of this chapter's functionality:

```py


class ClientMetadata(BaseModel):
    name: str
    version: str


class EntrypointMetadata(BaseModel):
    agent_entrypoint: Literal["cli", "acp", "programmatic"]
    agent_version: str
    client_name: str
    client_version: str


StrToolChoice = Literal["auto", "none", "any", "required"]


class AvailableFunction(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]


class AvailableTool(BaseModel):
    type: Literal["function"] = "function"
    function: AvailableFunction


class FunctionCall(BaseModel):
    name: str | None = None
    arguments: str | None = None

```

This class is important because it defines how Mistral Vibe Tutorial: Minimal CLI Coding Agent by Mistral implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[AgentStats]
    B[SessionInfo]
    C[SessionMetadata]
    D[ClientMetadata]
    E[EntrypointMetadata]
    A --> B
    B --> C
    C --> D
    D --> E
```
