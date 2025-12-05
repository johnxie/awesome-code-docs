---
layout: default
title: "Langfuse Tutorial - Chapter 7: Integrations"
nav_order: 7
has_children: false
parent: Langfuse Tutorial
---

# Chapter 7: Integrations

> Connect Langfuse with LangChain, LlamaIndex, OpenAI SDK, and other frameworks.

## Overview

Langfuse integrates seamlessly with popular LLM frameworks, providing automatic tracing with minimal code changes.

## LangChain Integration

One-line integration for full observability:

```python
from langchain_openai import ChatOpenAI
from langchain.callbacks import LangfuseCallbackHandler
from langfuse import Langfuse

# Initialize Langfuse
langfuse = Langfuse(public_key="pk-...", secret_key="sk-...", host="https://cloud.langfuse.com")

# Create callback handler
callback = LangfuseCallbackHandler(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"
)

# Use with any LangChain chain
llm = ChatOpenAI(model="gpt-4o-mini", callbacks=[callback])
chain = prompt | llm | output_parser

result = chain.invoke({"input": "Hello"})
# Traces automatically captured
```

## LlamaIndex Integration

```python
from llama_index.llms import OpenAI
from llama_index.callbacks import CallbackManager, LangfuseCallbackHandler

# Setup callback
callback_manager = CallbackManager([
    LangfuseCallbackHandler(
        public_key="pk-...",
        secret_key="sk-...",
        host="https://cloud.langfuse.com"
    )
])

# Use with LlamaIndex
llm = OpenAI(model="gpt-4o-mini", callback_manager=callback_manager)
index = VectorStoreIndex.from_documents(documents, callback_manager=callback_manager)

query_engine = index.as_query_engine()
response = query_engine.query("What is Langfuse?")
```

## OpenAI SDK Integration

Enhanced tracing for direct OpenAI usage:

```python
from langfuse.openai import openai
from langfuse import Langfuse

# Patch OpenAI client
langfuse = Langfuse(public_key="pk-...", secret_key="sk-...", host="https://cloud.langfuse.com")
client = langfuse.wrap_openai(openai.OpenAI())

# All calls now traced
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    langfuse_prompt="greeting",  # Link to prompt management
)
```

## Anthropic Integration

```python
from langfuse.anthropic import anthropic
import anthropic

# Patch Anthropic client
client = langfuse.wrap_anthropic(anthropic.Anthropic())

response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Explain quantum computing"}],
)
```

## Custom Integration

For unsupported frameworks:

```python
from langfuse import Langfuse

langfuse = Langfuse(public_key="pk-...", secret_key="sk-...", host="https://cloud.langfuse.com")

# Manual tracing
trace = langfuse.trace(name="custom-workflow", user_id="user123")

# Your custom logic
input_data = {"query": "What is AI?"}
trace.span(name="preprocessing", input=input_data)

# Call your LLM/framework
result = your_llm_call(input_data)

trace.span(name="llm", input=input_data, output=result, usage={"tokens": 150})
trace.end()

langfuse.flush()
```

## Vercel AI SDK

```typescript
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';
import { observe } from '@langfuse/vercel-ai';

const model = observe(openai('gpt-4o-mini'));

const result = await generateText({
  model,
  prompt: 'What is the capital of France?',
});
```

## CrewAI Integration

```python
from crewai import Agent, Task, Crew
from langfuse.crewai import CrewAICallbackHandler

# Add callback to crew
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    callbacks=[CrewAICallbackHandler(
        public_key="pk-...",
        secret_key="sk-...",
        host="https://cloud.langfuse.com"
    )]
)

result = crew.kickoff()
```

## Multi-Framework Applications

Combine frameworks in one trace:

```python
trace = langfuse.trace(name="hybrid-rag")

# LangChain retrieval
retriever = vectorstore.as_retriever(callbacks=[langchain_callback])
docs = retriever.get_relevant_documents("query")

# LlamaIndex synthesis
llm = OpenAI(callback_manager=llamaindex_callback)
response = llm.complete(f"Answer using: {docs}")

trace.end()
```

## Tips

- Use framework-specific handlers when available for automatic instrumentation.
- Set consistent `user_id` and `session_id` across frameworks.
- Tag spans by framework for filtering: `tags=["langchain", "retrieval"]`.
- Combine manual and automatic tracing for custom logic.

Next: deploy Langfuse to production. 