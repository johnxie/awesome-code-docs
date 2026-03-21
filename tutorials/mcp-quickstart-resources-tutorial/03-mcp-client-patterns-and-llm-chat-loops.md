---
layout: default
title: "Chapter 3: MCP Client Patterns and LLM Chat Loops"
nav_order: 3
parent: MCP Quickstart Resources Tutorial
---


# Chapter 3: MCP Client Patterns and LLM Chat Loops

Welcome to **Chapter 3: MCP Client Patterns and LLM Chat Loops**. In this part of **MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers client-side flows for connecting to MCP servers and exposing tool calls in chat UX.

## Learning Goals

- compare client behavior across Go/Python/TypeScript examples
- map MCP tool discovery to conversational interaction loops
- handle absent credentials and fallback behavior safely
- design adapter layers for provider-specific LLM APIs

## Client Design Guardrails

- isolate MCP transport logic from model-provider wrappers.
- keep tool call schemas strict and explicit.
- fail gracefully when API keys or external services are unavailable.

## Source References

- [MCP Client (Go)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/mcp-client-go/README.md)
- [MCP Client (Python)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/mcp-client-python/README.md)
- [MCP Client (TypeScript)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/mcp-client-typescript/README.md)

## Summary

You now have a practical MCP client loop model for chatbot-oriented integrations.

Next: [Chapter 4: Protocol Flow and stdio Transport Behavior](04-protocol-flow-and-stdio-transport-behavior.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `mcp-client-go/main.go`

The `ProcessQuery` function in [`mcp-client-go/main.go`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/mcp-client-go/main.go) handles a key part of this chapter's functionality:

```go
}

func (c *MCPClient) ProcessQuery(ctx context.Context, query string) (string, error) {
	if c.session == nil {
		return "", fmt.Errorf("client is not connected to any server")
	}

	messages := []anthropic.MessageParam{
		anthropic.NewUserMessage(anthropic.NewTextBlock(query)),
	}

	// Initial Claude API call with tools
	response, err := c.anthropic.Messages.New(ctx, anthropic.MessageNewParams{
		Model:     model,
		MaxTokens: 1024,
		Messages:  messages,
		Tools:     c.tools,
	})
	if err != nil {
		return "", fmt.Errorf("anthropic API request failed: %w", err)
	}

	var toolUseBlocks []anthropic.ToolUseBlock
	var finalText []string
	for _, block := range response.Content {
		switch b := block.AsAny().(type) {
		case anthropic.TextBlock:
			finalText = append(finalText, b.Text)
		case anthropic.ToolUseBlock:
			toolUseBlocks = append(toolUseBlocks, b)
		}
	}
```

This function is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.

### `mcp-client-go/main.go`

The `ChatLoop` function in [`mcp-client-go/main.go`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/mcp-client-go/main.go) handles a key part of this chapter's functionality:

```go
}

func (c *MCPClient) ChatLoop(ctx context.Context) error {
	fmt.Println("\nMCP Client Started!")
	fmt.Println("Type your queries or 'quit' to exit.")

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("\nQuery: ")
		if !scanner.Scan() {
			break // EOF
		}

		query := strings.TrimSpace(scanner.Text())
		if strings.EqualFold(query, "quit") {
			break
		}
		if query == "" {
			continue
		}

		response, err := c.ProcessQuery(ctx, query)
		if err != nil {
			fmt.Printf("\nError: %v\n", err)
			continue
		}

		fmt.Printf("\n%s\n", response)
	}

	return scanner.Err()
```

This function is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.

### `mcp-client-go/main.go`

The `Cleanup` function in [`mcp-client-go/main.go`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/mcp-client-go/main.go) handles a key part of this chapter's functionality:

```go
}

func (c *MCPClient) Cleanup() error {
	if c.session != nil {
		if err := c.session.Close(); err != nil {
			return fmt.Errorf("failed to close session: %w", err)
		}
		c.session = nil
	}
	return nil
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: go run main.go <server_script_or_binary> [args...]")
		os.Exit(1)
	}

	serverArgs := os.Args[1:]

	client, err := NewMCPClient()
	if err != nil {
		log.Fatalf("Failed to create MCP client: %v", err)
	}

	ctx := context.Background()

	if err := client.ConnectToServer(ctx, serverArgs); err != nil {
		log.Fatalf("Failed to connect to MCP server: %v", err)
	}

	if err := client.ChatLoop(ctx); err != nil {
```

This function is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.

### `mcp-client-go/main.go`

The `main` function in [`mcp-client-go/main.go`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/mcp-client-go/main.go) handles a key part of this chapter's functionality:

```go
package main

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
	"github.com/joho/godotenv"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

var model anthropic.Model = anthropic.ModelClaudeSonnet4_5_20250929

type MCPClient struct {
	anthropic *anthropic.Client
	session   *mcp.ClientSession
	tools     []anthropic.ToolUnionParam
}

func NewMCPClient() (*MCPClient, error) {
	// Load .env file
	if err := godotenv.Load(); err != nil {
		return nil, fmt.Errorf("failed to load .env file: %w", err)
```

This function is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[ProcessQuery]
    B[ChatLoop]
    C[Cleanup]
    D[main]
    E[formatAlert]
    A --> B
    B --> C
    C --> D
    D --> E
```
