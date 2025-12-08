---
layout: default
title: "Chapter 1: Getting Started with AG2"
parent: "AG2 Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with AG2

Set up AG2, create your first assistant+user agents, and run a minimal conversation.

## Objectives
- Install AG2 and dependencies
- Configure API keys and environment
- Run a two-agent conversation

## Prerequisites
- Python 3.10+
- OpenAI-compatible API key

## Install
```bash
pip install ag2 openai tiktoken
```

## Minimal Conversation
```python
from ag2 import AssistantAgent, UserProxyAgent, run_chat

assistant = AssistantAgent(name="Helper")
user = UserProxyAgent(name="User")

messages = [
    {"role": "user", "content": "Summarize AG2 in one sentence."}
]

result = run_chat(assistant=assistant, user_proxy=user, messages=messages)
print(result)
```

## Configure Keys
- Set `OPENAI_API_KEY` in your environment.
- For Azure/OpenRouter, configure provider in AG2 settings.

## Troubleshooting
- Missing key: ensure env var is set in shell/terminal.
- Import errors: upgrade `ag2` and reinstall dependencies.

## Next Steps
Proceed to Chapter 2 to explore agent types and role design.
