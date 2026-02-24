---
layout: default
title: "Chapter 3: Memory Systems"
parent: "LangChain Tutorial"
nav_order: 3
---

# Chapter 3: Memory Systems

Welcome to one of the most exciting parts of building AI applications: **memory**! Up until now, our AI interactions have been stateless - each conversation starts fresh. But real conversations build on previous context. In this chapter, we'll add memory to make your applications truly conversational.

## What Problem Does Memory Solve?

Imagine chatting with a friend who forgets everything you just said:

```
You: I'm learning about Python and need help with loops.
AI: Great! Loops are fundamental in programming.

You: Can you show me a for loop example?
AI: Sure! Here's how you write a for loop in Python...
```

Now imagine the same conversation with memory:

```
You: I'm learning about Python and need help with loops.
AI: Great! Loops are fundamental in programming.

You: Can you show me a for loop example?
AI: Absolutely! Since you mentioned you're learning Python, here's a simple for loop...
```

The second version feels much more natural because the AI remembers your context!

## Types of Memory in LangChain

LangChain provides several types of memory for different use cases:

### 1. Conversation Buffer Memory
Stores the entire conversation history:

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

# Create memory
memory = ConversationBufferMemory()

# Create chain with memory
chain = ConversationChain(
    llm=ChatOpenAI(),
    memory=memory,
    verbose=True
)

# Have a conversation
chain.predict(input="Hi, I'm learning about AI!")
chain.predict(input="What's the most important concept I should know?")
```

### 2. Conversation Summary Memory
Summarizes the conversation to save space:

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(
    llm=ChatOpenAI(),
    return_messages=True
)

# This will keep a summary instead of full messages
```

### 3. Conversation Window Memory
Keeps only the most recent K interactions:

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=2)  # Keep last 2 interactions

# Only remembers the most recent exchanges
```

## How Memory Works Under the Hood

Memory systems in LangChain work by:

1. **Storing conversation history** between interactions
2. **Injecting relevant context** into new prompts
3. **Managing memory size** to avoid token limits
4. **Providing memory utilities** for different use cases

Let's look at a practical example:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

# Create a template that includes memory
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the conversation history to provide relevant responses."),
    ("system", "Conversation history: {history}"),
    ("human", "{input}")
])

# Create memory
memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)

# Create chain
chain = LLMChain(
    llm=ChatOpenAI(),
    prompt=template,
    memory=memory
)

# Test the conversation
response1 = chain.predict(input="My name is Alice and I love Python programming.")
print(f"Response 1: {response1}")

response2 = chain.predict(input="What's my name and what do I love?")
print(f"Response 2: {response2}")

# Check what's in memory
print(f"Memory contents: {memory.chat_memory.messages}")
```

## Advanced Memory Patterns

### Custom Memory Classes

You can create custom memory systems for specific needs:

```python
from langchain.memory import BaseMemory
from langchain.schema import BaseMessage
from typing import List, Dict, Any

class SelectiveMemory(BaseMemory):
    """Memory that only remembers important information"""

    memories: List[str] = []

    @property
    def memory_key(self) -> str:
        return "important_facts"

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Save only important information"""
        user_input = inputs.get("input", "")
        ai_response = outputs.get("output", "")

        # Only save if input contains keywords
        important_keywords = ["remember", "important", "key", "essential"]

        if any(keyword in user_input.lower() for keyword in important_keywords):
            self.memories.append(f"User: {user_input}")
            self.memories.append(f"AI: {ai_response}")

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Load relevant memories"""
        return {"important_facts": "\n".join(self.memories[-5:])}  # Last 5 memories

    def clear(self) -> None:
        """Clear all memories"""
        self.memories = []
```

### Memory with Multiple Variables

```python
from langchain.memory import ConversationBufferMemory

# Memory with multiple variables
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="input",
    output_key="output"
)

# You can also store custom variables
memory.save_context(
    inputs={"input": "Hello", "user_name": "Alice"},
    outputs={"output": "Hi Alice!", "sentiment": "positive"}
)
```

## Memory in Runnable Chains (LCEL)

With the newer Runnable interface, memory works differently:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

# Create memory
memory = ConversationBufferMemory(return_messages=True)

# Function to load memory
def load_memory(input_dict):
    return memory.load_memory_variables({})["history"]

# Create chain with memory
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("system", "Chat history: {history}"),
    ("human", "{input}")
])

chain = (
    RunnablePassthrough.assign(history=load_memory)
    | template
    | ChatOpenAI()
)

# Function to save to memory
def save_to_memory(result):
    memory.save_context(
        inputs={"input": result["input"]},
        outputs={"output": result["output"]}
    )
    return result

# Add memory saving
chain_with_memory = chain | save_to_memory

# Use the chain
result = chain_with_memory.invoke({"input": "Remember that I love pizza"})
result = chain_with_memory.invoke({"input": "What do I love?"})
```

## Memory Best Practices

### 1. Choose the Right Memory Type

```python
# For short conversations
memory = ConversationBufferWindowMemory(k=5)

# For long conversations with limited context
memory = ConversationSummaryMemory(llm=ChatOpenAI())

# For remembering specific facts
memory = ConversationBufferMemory()

# For very long conversations
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(),
    max_token_limit=2000
)
```

### 2. Handle Memory Limits

```python
from langchain.memory import ConversationSummaryBufferMemory

# Automatically summarizes when token limit is reached
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(),
    max_token_limit=2000,  # Summarize when approaching this limit
    return_messages=True
)
```

### 3. Memory with Custom Filtering

```python
class FilteredMemory(ConversationBufferMemory):
    """Memory that filters out certain types of messages"""

    def save_context(self, inputs, outputs):
        # Don't save if input contains sensitive information
        user_input = inputs.get("input", "")
        if "password" in user_input.lower():
            return  # Don't save this

        super().save_context(inputs, outputs)
```

## Real-World Memory Use Cases

### Customer Support Bot

```python
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain

# Memory that summarizes customer interactions
memory = ConversationSummaryMemory(llm=ChatOpenAI())

support_chain = ConversationChain(
    llm=ChatOpenAI(),
    memory=memory,
    verbose=True
)

# The bot will remember customer issues and solutions
support_chain.predict(input="My order #12345 hasn't arrived yet")
support_chain.predict(input="When can I expect delivery?")
```

### Learning Assistant

```python
from langchain.memory import ConversationBufferMemory

# Remember student's progress and preferences
memory = ConversationBufferMemory()

learning_chain = ConversationChain(
    llm=ChatOpenAI(),
    memory=memory
)

# Bot adapts to student's learning style over time
learning_chain.predict(input="I'm a visual learner who struggles with math")
learning_chain.predict(input="Can you explain algebra with diagrams?")
```

## Debugging Memory Issues

```python
# Check what's in memory
print("Memory contents:")
print(memory.chat_memory.messages)

# Clear memory if needed
memory.clear()

# Check memory variables
variables = memory.load_memory_variables({})
print("Memory variables:", variables)
```

## What We've Accomplished

Excellent work! 🎉 You've now learned:

1. **Different Memory Types** - Buffer, summary, and window memory
2. **How Memory Works** - Storing and retrieving conversation context
3. **Custom Memory Classes** - Building memory systems for specific needs
4. **Memory Best Practices** - Choosing the right memory for your use case
5. **Real-World Applications** - Customer support and learning assistants

## Memory Performance Considerations

- **Token Limits**: Memory consumes tokens, affecting costs and performance
- **Context Length**: Different models have different context limits
- **Summarization**: Use summary memory for long conversations
- **Selective Memory**: Only store important information

## Next Steps

Now that your applications can remember conversations, let's learn about working with external data sources. In [Chapter 4: Document Loading & Processing](04-document-processing.md), we'll explore how to connect LangChain to PDFs, websites, and other data sources.

---

**Try this exercise:**
Create a memory-enabled chatbot that remembers user preferences (like favorite color, programming language, etc.) and uses that information in future conversations.

*What kind of memory would you use for a personal assistant that needs to remember appointments, preferences, and ongoing tasks?* 🤔

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `memory`, `input`, `langchain` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Memory Systems` as an operating subsystem inside **LangChain Tutorial: Building AI Applications with Large Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `ChatOpenAI`, `ConversationBufferMemory`, `chain` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Memory Systems` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `memory`.
2. **Input normalization**: shape incoming data so `input` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `langchain`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langchain)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `memory` and `input` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Prompt Templates & Chains](02-prompt-templates.md)
- [Next Chapter: Chapter 4: Document Loading & Processing](04-document-processing.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
