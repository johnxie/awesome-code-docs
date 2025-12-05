---
layout: default
title: "Letta Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Letta Tutorial
---

# Chapter 1: Getting Started with Letta

> Install Letta, create your first agent, and start a conversation with persistent memory.

## Overview

Letta (formerly MemGPT) enables AI agents with persistent memory. This chapter covers installation, basic setup, and your first conversation with an agent that remembers.

## Prerequisites

- Python 3.9+
- OpenAI API key or compatible LLM provider
- Basic command line knowledge

## Installation

Install Letta via pip:

```bash
pip install letta
```

Or for development:

```bash
git clone https://github.com/letta-ai/letta.git
cd letta
pip install -e .
```

## Quick Start

Create your first agent with one command:

```bash
letta create --name sam --persona "You are Sam, a helpful AI assistant."
```

This creates an agent with default settings and starts a chat session.

## Configuration

Set up your API keys and configuration:

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-your-key-here"

# Or configure via letta config
letta configure
```

Choose your LLM provider and model:

```bash
letta config set default_model gpt-4o-mini
letta config set default_embedding_model text-embedding-ada-002
```

## Your First Conversation

Start chatting with your agent:

```bash
letta chat --name sam
```

In the chat interface:

```
Human: Hi, I'm John and I work as a software developer.

Assistant: Hello John! I'm Sam, your helpful AI assistant. I see you're a software developer. I'll remember that for our future conversations.

Human: What's my name and profession?

Assistant: Your name is John and you're a software developer. I remember that from our conversation just now!
```

The agent remembers your introduction across the session!

## Understanding Agent State

Check what your agent knows:

```bash
letta get-agent --name sam
```

This shows the agent's core memory, including facts about you.

## Creating Multiple Agents

Create agents with different personalities:

```bash
# A creative writing assistant
letta create --name writer --persona "You are a creative writing coach who helps with stories and characters."

# A coding assistant
letta create --name coder --persona "You are an expert software engineer who writes clean, efficient code."
```

## Switching Between Agents

Chat with different agents:

```bash
letta chat --name writer
letta chat --name coder
```

Each agent maintains its own memory and personality.

## Basic Memory Inspection

View an agent's memory:

```bash
# See all agents
letta list-agents

# Get detailed info about an agent
letta get-agent --name sam --json
```

## Troubleshooting

Common issues:

- **API Key Not Set**: Make sure `OPENAI_API_KEY` is exported
- **Model Not Available**: Check if your API key has access to the specified model
- **Memory Issues**: Ensure you have enough disk space for the local database

## Next Steps

Now that you have agents running, let's explore how their memory actually works in the next chapter.

## Example Session

```bash
$ letta create --name sam --persona "You are Sam, a helpful AI assistant."
Created agent 'sam' with ID: agent_123

$ letta chat --name sam
Starting chat with agent 'sam'...

Human: Hello! I'm Alex, a data scientist from New York.

Assistant: Hi Alex! I'm Sam. It's great to meet you. I'll remember you're a data scientist from New York for our future conversations.

Human: What do you know about me?

Assistant: I know that your name is Alex, you're a data scientist, and you're from New York. Is there anything else you'd like me to know or any questions you have?
```

The agent automatically stored and retrieved your personal information! This is the foundation of Letta's persistent memory system. 