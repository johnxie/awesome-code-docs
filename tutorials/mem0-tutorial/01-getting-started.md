---
layout: default
title: "Chapter 1: Getting Started with Mem0"
parent: "Mem0 Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Mem0

Welcome to Mem0! If you've ever built AI applications and wished they could remember user preferences, maintain context across sessions, or learn from interactions, you're in the right place. Mem0 is the memory layer that transforms stateless AI interactions into personalized, context-aware conversations.

## What Makes Mem0 Special?

Mem0 revolutionizes AI memory with:
- **+26% Accuracy** over traditional memory approaches on industry benchmarks
- **91% Faster Responses** through intelligent memory retrieval
- **90% Lower Token Usage** by avoiding full-context repetition
- **Multi-Level Memory** supporting User, Session, and Agent memories
- **Universal Compatibility** with all major LLM providers

## Installing Mem0

### Python Installation

```bash
# Install Mem0 via pip
pip install mem0ai

# Or install with optional dependencies
pip install mem0ai[all]

# For development
pip install mem0ai[dev]
```

### Node.js Installation

```bash
# Install Mem0 via npm
npm install mem0ai

# Or via yarn
yarn add mem0ai
```

### Docker Setup

```bash
# Run Mem0 with Docker
docker run -p 8000:8000 mem0ai/mem0

# Or use Docker Compose for full stack
docker-compose up -d
```

## Your First Memory-Enabled AI Agent

Let's create your first AI agent with intelligent memory:

### Step 1: Basic Setup

```python
from openai import OpenAI
from mem0 import Memory

# Initialize OpenAI client
openai_client = OpenAI(api_key="your-openai-api-key")

# Initialize Mem0 memory
memory = Memory()

print("✅ Mem0 initialized successfully!")
```

### Step 2: Create a Memory-Enabled Chat Function

```python
def chat_with_memory(message: str, user_id: str = "default_user") -> str:
    """
    Chat function that uses Mem0 for context and memory
    """
    # Retrieve relevant memories for this user
    relevant_memories = memory.search(
        query=message,
        user_id=user_id,
        limit=3
    )

    # Format memories for context
    memories_str = "\n".join(
        f"- {entry['memory']}" for entry in relevant_memories["results"]
    )

    # Create system prompt with memory context
    system_prompt = f"""You are a helpful AI assistant with access to the user's memory.

User Memories:
{memories_str}

Use this context to provide personalized, relevant responses. Reference previous conversations and preferences when appropriate."""

    # Generate AI response
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    assistant_response = response.choices[0].message.content

    # Store the conversation in memory
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response
```

### Step 3: Test Your Memory Agent

```python
def main():
    print("🤖 Memory-Enabled AI Agent")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'exit':
            print("Goodbye! 👋")
            break

        # Get AI response with memory
        response = chat_with_memory(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()
```

## Understanding Mem0's Architecture

### Memory Types

Mem0 supports three levels of memory:

```
User Memory
├── Personal preferences and traits
├── Long-term interaction patterns
└── Historical context

Session Memory
├── Current conversation context
├── Temporary preferences
└── Session-specific information

Agent Memory
├── Agent capabilities and limitations
├── Learned behaviors and patterns
└── System-level optimizations
```

### How Memory Retrieval Works

```python
# Search for relevant memories
memories = memory.search(
    query="user's favorite programming language",
    user_id="john_doe",
    limit=5,
    filters={"category": "preferences"}
)

# Results include relevance scores and metadata
for memory_item in memories["results"]:
    print(f"Memory: {memory_item['memory']}")
    print(f"Score: {memory_item['score']}")
    print(f"Timestamp: {memory_item['timestamp']}")
    print("---")
```

## Advanced Memory Operations

### Adding Custom Memories

```python
# Add specific memories with metadata
memory.add(
    messages=[
        {
            "role": "user",
            "content": "I prefer Python over JavaScript for data science projects"
        },
        {
            "role": "assistant",
            "content": "Noted! I'll remember you prefer Python for data science."
        }
    ],
    user_id="john_doe",
    metadata={
        "category": "preferences",
        "topic": "programming_languages",
        "importance": "high"
    }
)
```

### Memory Search with Filters

```python
# Advanced search with multiple filters
results = memory.search(
    query="machine learning projects",
    user_id="john_doe",
    filters={
        "category": "projects",
        "status": "completed",
        "date_range": {"start": "2024-01-01", "end": "2024-12-31"}
    },
    limit=10
)
```

### Memory Analytics

```python
# Get memory statistics
stats = memory.get_stats(user_id="john_doe")

print(f"Total memories: {stats['total_memories']}")
print(f"Categories: {stats['categories']}")
print(f"Most active topics: {stats['top_topics']}")
print(f"Memory utilization: {stats['usage_percentage']}%")
```

## Real-World Memory Patterns

### Customer Support Agent

```python
class CustomerSupportAgent:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.openai_client = OpenAI()

    def handle_customer_query(self, query: str, customer_id: str):
        # Retrieve customer history
        customer_history = self.memory.search(
            query=query,
            user_id=customer_id,
            filters={"type": "support_interaction"},
            limit=5
        )

        # Build context
        context = "\n".join([
            f"Previous interaction: {mem['memory']}"
            for mem in customer_history["results"]
        ])

        # Generate personalized response
        prompt = f"""
        Customer Support Context:
        {context}

        Current Query: {query}

        Provide a helpful, personalized response that references the customer's history when relevant.
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # Store interaction
        self.memory.add([
            {"role": "user", "content": query},
            {"role": "assistant", "content": response.choices[0].message.content}
        ], user_id=customer_id, metadata={"type": "support_interaction"})

        return response.choices[0].message.content
```

### Personal AI Assistant

```python
class PersonalAssistant:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.user_preferences = {}

    def learn_user_preference(self, category: str, preference: str, user_id: str):
        """Learn and store user preferences"""
        self.memory.add(
            messages=[{
                "role": "system",
                "content": f"User preference: {category} = {preference}"
            }],
            user_id=user_id,
            metadata={
                "type": "preference",
                "category": category,
                "confidence": 0.9
            }
        )

    def get_personalized_response(self, query: str, user_id: str):
        """Generate response using user preferences"""
        # Get user preferences
        preferences = self.memory.search(
            query="user preferences",
            user_id=user_id,
            filters={"type": "preference"}
        )

        # Build personalized prompt
        pref_context = "\n".join([
            f"- {mem['memory']}" for mem in preferences["results"]
        ])

        prompt = f"""
        User Preferences:
        {pref_context}

        Query: {query}

        Provide a response that considers the user's preferences and past interactions.
        """

        # Generate and store response
        response = self.generate_response(prompt)
        self.store_interaction(query, response, user_id)

        return response
```

## Configuration and Customization

### Basic Configuration

```python
from mem0 import Memory

# Initialize with custom configuration
memory = Memory(
    # Storage backend
    storage_backend="qdrant",  # Options: chroma, qdrant, pinecone, redis

    # Embedding model
    embedding_model="text-embedding-3-small",

    # Memory settings
    max_memory_instances=1000,
    similarity_threshold=0.7,

    # Vector database settings
    vector_store={
        "host": "localhost",
        "port": 6333,
        "collection_name": "mem0_memories"
    }
)
```

### Environment Configuration

```bash
# .env file
MEM0_STORAGE_BACKEND=qdrant
MEM0_EMBEDDING_MODEL=text-embedding-3-small
MEM0_OPENAI_API_KEY=your-openai-key
MEM0_QDRANT_URL=http://localhost:6333
MEM0_REDIS_URL=redis://localhost:6379
```

### Advanced Configuration

```python
# Multi-tenant configuration
memory_config = {
    "tenants": {
        "tenant_1": {
            "storage_backend": "qdrant",
            "collection_name": "tenant_1_memories"
        },
        "tenant_2": {
            "storage_backend": "pinecone",
            "index_name": "tenant-2-memories"
        }
    },
    "default_tenant": "tenant_1"
}

memory = Memory.from_config(memory_config)
```

## Memory Performance Optimization

### Indexing Strategy

```python
# Create optimized indexes for better search performance
memory.create_index(
    user_id="john_doe",
    index_type="semantic",  # semantic, keyword, hybrid
    fields=["content", "metadata.category", "metadata.timestamp"]
)
```

### Batch Operations

```python
# Batch add memories for better performance
memories_batch = [
    {"role": "user", "content": "Memory 1", "metadata": {"batch": "1"}},
    {"role": "user", "content": "Memory 2", "metadata": {"batch": "1"}},
    {"role": "user", "content": "Memory 3", "metadata": {"batch": "1"}}
]

memory.add_batch(memories_batch, user_id="john_doe")
```

### Memory Cleanup

```python
# Remove old or irrelevant memories
memory.cleanup(
    user_id="john_doe",
    criteria={
        "older_than_days": 90,
        "relevance_threshold": 0.3,
        "categories_to_keep": ["preferences", "important_events"]
    }
)
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed Mem0** and set up your development environment
2. **Created your first memory-enabled AI agent** with context awareness
3. **Understood the core architecture** of multi-level memory systems
4. **Implemented advanced memory operations** including search and filtering
5. **Built real-world applications** like customer support and personal assistants
6. **Optimized memory performance** with indexing and batch operations
7. **Configured Mem0** for different storage backends and use cases

## Next Steps

Now that you have a working memory system, let's explore the different types of memory and how they work together. In [Chapter 2: Memory Architecture & Types](02-memory-architecture.md), we'll dive into the technical details of how Mem0 organizes and manages different levels of memory.

---

**Practice what you've learned:**
1. Create a memory-enabled chatbot that remembers user preferences
2. Build a customer support system that references past interactions
3. Implement a personal assistant that learns from user behavior
4. Experiment with different memory search and filtering options

*What kind of AI application would benefit most from intelligent memory?* 🧠

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `memory`, `user_id`, `response` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Mem0` as an operating subsystem inside **Mem0 Tutorial: Building Production-Ready AI Agents with Scalable Long-Term Memory**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `self`, `Memory` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Mem0` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `memory`.
2. **Input normalization**: shape incoming data so `user_id` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `response`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/mem0ai/mem0)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `memory` and `user_id` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Memory Architecture & Types](02-memory-architecture.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
