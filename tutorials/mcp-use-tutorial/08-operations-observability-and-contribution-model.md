---
layout: default
title: "Chapter 8: Operations, Observability, and Contribution Model"
nav_order: 8
parent: MCP Use Tutorial
---


# Chapter 8: Operations, Observability, and Contribution Model

Welcome to **Chapter 8: Operations, Observability, and Contribution Model**. In this part of **MCP Use Tutorial: Full-Stack MCP Development Across Agents, Clients, Servers, and Inspector**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Sustained mcp-use adoption requires explicit operational standards, observability paths, and contribution workflows.

## Learning Goals

- structure CI and runtime observability around tool-calling behavior
- separate Python and TypeScript release/testing responsibilities
- align contribution workflow with monorepo boundaries
- keep docs and examples synchronized with runtime behavior changes

## Operating Model

- keep package-level ownership clear (Python vs TypeScript)
- run focused integration tests per transport and primitive area
- centralize configuration examples to avoid copy drift
- enforce issue-first + small-PR contribution discipline

## Source References

- [Contributing Guide](https://github.com/mcp-use/mcp-use/blob/main/CONTRIBUTING.md)
- [Main README](https://github.com/mcp-use/mcp-use/blob/main/README.md)
- [TypeScript README](https://github.com/mcp-use/mcp-use/blob/main/libraries/typescript/README.md)
- [Python README](https://github.com/mcp-use/mcp-use/blob/main/libraries/python/README.md)

## Summary

You now have an end-to-end operational model for running and evolving mcp-use based systems.

Next: Continue with [MCP TypeScript SDK Tutorial](../mcp-typescript-sdk-tutorial/)

## Source Code Walkthrough

### `libraries/python/examples/structured_output.py`

The `main` function in [`libraries/python/examples/structured_output.py`](https://github.com/mcp-use/mcp-use/blob/HEAD/libraries/python/examples/structured_output.py) handles a key part of this chapter's functionality:

```py


async def main():
    """Research Padova using intelligent structured output."""
    load_dotenv()

    config = {
        "mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"], "env": {"DISPLAY": ":1"}}}
    }

    client = MCPClient(config=config)
    llm = ChatOpenAI(model="gpt-5")
    agent = MCPAgent(llm=llm, client=client, max_steps=50, pretty_print=True)

    result: CityInfo = await agent.run(
        """
        Research comprehensive information about the city of Padova (also known as Padua) in Italy.

        Visit multiple reliable sources like Wikipedia, official city websites, tourism sites,
        and university websites to gather detailed information including demographics, history,
        governance, education, economy, landmarks, and international relationships.
        """,
        output_schema=CityInfo,
        max_steps=50,
    )

    print(f"Name: {result.name}")
    print(f"Country: {result.country}")
    print(f"Region: {result.region}")
    print(f"Population: {result.population:,}")
    print(f"Area: {result.area_km2} km²")
    print(f"Foundation: {result.foundation_date}")
```

This function is important because it defines how MCP Use Tutorial: Full-Stack MCP Development Across Agents, Clients, Servers, and Inspector implements the patterns covered in this chapter.

### `libraries/python/examples/limited_memory_chat.py`

The `run_limited_memory_chat` function in [`libraries/python/examples/limited_memory_chat.py`](https://github.com/mcp-use/mcp-use/blob/HEAD/libraries/python/examples/limited_memory_chat.py) handles a key part of this chapter's functionality:

```py


async def run_limited_memory_chat():
    """Run a chat using MCPAgent with limited conversation memory."""
    # Load environment variables for API keys
    load_dotenv()

    config = {
        "mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"], "env": {"DISPLAY": ":1"}}}
    }
    # Create MCPClient from config file
    client = MCPClient(config=config)
    llm = ChatOpenAI(model="gpt-5")
    # Create agent with memory_enabled=False but pass external history
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,  # Disable built-in memory, use external history
        pretty_print=True,
    )

    # Configuration: Limited history mode
    MAX_HISTORY_MESSAGES = 5

    print("\n===== Interactive MCP Chat (Limited Memory) =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        # Main chat loop with limited history
```

This function is important because it defines how MCP Use Tutorial: Full-Stack MCP Development Across Agents, Clients, Servers, and Inspector implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[main]
    B[run_limited_memory_chat]
    A --> B
```
