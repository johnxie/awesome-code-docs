---
layout: default
title: "Phidata Tutorial - Chapter 4: Memory Systems"
nav_order: 4
has_children: false
parent: Phidata Tutorial
---

# Chapter 4: Memory Systems - Building Context-Aware Agents

> Implement intelligent memory systems that enable agents to maintain context, learn from interactions, and provide personalized experiences.

## Basic Memory Types

### Buffer Memory

```python
from phidata.agent import Agent
from phidata.memory import BufferMemory

# Create agent with buffer memory
buffer_agent = Agent(
    name="BufferMemoryAgent",
    instructions="You are a helpful assistant with conversation memory.",
    model="gpt-4",
    memory=BufferMemory(max_tokens=2000)  # Store up to 2000 tokens
)

# Multi-turn conversation with memory
conversation = [
    "Hello! My name is Alice and I work as a software engineer.",
    "I specialize in Python and machine learning.",
    "What's my name and what do I do?",
    "Can you recommend some Python libraries for ML?"
]

for message in conversation:
    response = buffer_agent.run(message)
    print(f"User: {message}")
    print(f"Agent: {response}")
    print("-" * 50)
```

### Conversation Summary Memory

```python
from phidata.memory import SummaryMemory

# Agent with conversation summarization
summary_agent = Agent(
    name="SummaryMemoryAgent",
    instructions="You are an assistant that maintains conversation summaries.",
    model="gpt-4",
    memory=SummaryMemory(
        summarizer_model="gpt-3.5-turbo",  # Use cheaper model for summarization
        summarize_after=5  # Summarize every 5 messages
    )
)

# Long conversation that gets summarized
long_conversation = [
    "I want to learn about machine learning.",
    "Can you explain supervised learning?",
    "What's the difference between classification and regression?",
    "Give me examples of classification algorithms.",
    "How does logistic regression work?",
    "What about decision trees?",
    "Can you compare random forests and gradient boosting?",
    "What's the best algorithm for my image recognition project?"
]

print("Starting long conversation...")
for i, message in enumerate(long_conversation, 1):
    print(f"\nTurn {i}: {message}")
    response = summary_agent.run(message)

    # Show memory summary every 3 turns
    if i % 3 == 0:
        memory_summary = summary_agent.memory.get_summary()
        print(f"Current memory summary: {memory_summary[:100]}...")

print(f"\nFinal conversation summary: {summary_agent.memory.get_summary()}")
```

## Advanced Memory Patterns

### Vector Memory for Semantic Search

```python
from phidata.memory import VectorMemory
from phidata.embedder import OpenAIEmbedder

# Create vector memory with embeddings
vector_memory = VectorMemory(
    embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY")),
    dimension=1536,  # OpenAI embedding dimension
    similarity_threshold=0.8  # Only retrieve highly relevant memories
)

vector_agent = Agent(
    name="VectorMemoryAgent",
    instructions="You are an assistant with semantic memory retrieval.",
    model="gpt-4",
    memory=vector_memory
)

# Build knowledge base through conversation
knowledge_building = [
    "I love hiking in the mountains. My favorite trail is the Appalachian Trail.",
    "I'm learning to play guitar. I've been practicing for 6 months.",
    "I work as a data scientist and enjoy analyzing sports statistics.",
    "My favorite programming language is Python because of its simplicity.",
    "I recently visited Japan and loved the food and culture.",
    "I'm interested in renewable energy, especially solar power."
]

print("Building knowledge base...")
for fact in knowledge_building:
    vector_agent.run(f"Remember this about me: {fact}")

# Test semantic retrieval
semantic_queries = [
    "What do I like to do outdoors?",
    "Tell me about my programming interests",
    "What hobbies have I mentioned?",
    "What did I say about travel?",
    "What are my professional interests?"
]

print("\nTesting semantic memory retrieval...")
for query in semantic_queries:
    response = vector_agent.run(query)
    print(f"Query: {query}")
    print(f"Response: {response}")
    print("-" * 80)
```

### Hierarchical Memory System

```python
from phidata.memory import Memory
from typing import Dict, List, Any
import json

class HierarchicalMemory(Memory):
    """Multi-level memory system with different retention periods."""

    def __init__(self):
        self.short_term = []  # Recent messages (last 10)
        self.medium_term = {}  # Important facts (last 24 hours)
        self.long_term = {}    # Core knowledge (persistent)

        # Importance scoring
        self.importance_keywords = [
            "remember", "important", "always", "never forget",
            "key point", "essential", "core", "fundamental"
        ]

    def add_message(self, role: str, content: str):
        """Add message to appropriate memory level."""

        message = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
            "importance": self._calculate_importance(content)
        }

        # Always add to short-term
        self.short_term.append(message)
        if len(self.short_term) > 10:
            self.short_term.pop(0)

        # Add important messages to medium-term
        if message["importance"] > 0.7:
            key = f"important_{len(self.medium_term)}"
            self.medium_term[key] = message

        # Add core knowledge to long-term
        if message["importance"] > 0.9:
            key = f"core_{len(self.long_term)}"
            self.long_term[key] = message

    def get_context(self, query: str = None) -> str:
        """Get contextual information based on query relevance."""

        context_parts = []

        # Always include recent context
        if self.short_term:
            recent = self._format_messages(self.short_term[-3:])  # Last 3 messages
            context_parts.append(f"Recent conversation:\n{recent}")

        # Include relevant medium-term memories
        if query and self.medium_term:
            relevant_medium = self._find_relevant_memories(query, self.medium_term)
            if relevant_medium:
                context_parts.append(f"Relevant information:\n{relevant_medium}")

        # Include core knowledge
        if self.long_term:
            core_knowledge = self._format_messages(list(self.long_term.values()))
            context_parts.append(f"Core knowledge:\n{core_knowledge}")

        return "\n\n".join(context_parts)

    def _calculate_importance(self, content: str) -> float:
        """Calculate importance score for content."""

        score = 0.5  # Base score

        content_lower = content.lower()

        # Check for importance keywords
        keyword_matches = sum(1 for keyword in self.importance_keywords
                            if keyword in content_lower)
        score += keyword_matches * 0.1

        # Length bonus (detailed information is often more important)
        if len(content.split()) > 20:
            score += 0.1

        # Question marks indicate curiosity/learning
        if "?" in content:
            score += 0.05

        return min(1.0, score)

    def _find_relevant_memories(self, query: str, memories: Dict[str, Any]) -> str:
        """Find memories relevant to the query."""

        relevant = []
        query_lower = query.lower()

        for memory in memories.values():
            content_lower = memory["content"].lower()

            # Simple keyword matching (could be enhanced with embeddings)
            if any(word in content_lower for word in query_lower.split()):
                relevant.append(memory["content"])

        return "\n".join(relevant[:3])  # Top 3 relevant memories

    def _format_messages(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages for context."""
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

# Agent with hierarchical memory
hierarchical_agent = Agent(
    name="HierarchicalMemoryAgent",
    instructions="""
    You are an assistant with sophisticated memory. You remember important details
    about users and can recall relevant information from past conversations.
    """,
    model="gpt-4",
    memory=HierarchicalMemory()
)

# Test hierarchical memory
test_interactions = [
    "Hi, I'm working on a machine learning project about image classification.",
    "Remember that I prefer Python over Java for data science work.",
    "This is an important project for my career advancement.",
    "What's my preferred programming language for data science?",
    "Can you remind me what I'm working on?"
]

print("Testing hierarchical memory...")
for interaction in test_interactions:
    response = hierarchical_agent.run(interaction)
    print(f"User: {interaction}")
    print(f"Agent: {response}")

    # Show memory state occasionally
    if "what" in interaction.lower():
        print(f"Current context: {hierarchical_agent.memory.get_context(interaction)[:200]}...")

    print("-" * 80)
```

## Memory Persistence

### File-Based Memory Storage

```python
import json
import os
from datetime import datetime
from phidata.memory import Memory

class PersistentMemory(Memory):
    """Memory system that persists to disk."""

    def __init__(self, storage_path: str = "./agent_memory"):
        self.storage_path = storage_path
        self.memory_file = os.path.join(storage_path, "memory.json")

        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)

        # Load existing memory
        self.messages = self._load_memory()

    def add_message(self, role: str, content: str):
        """Add message and persist to disk."""

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        self.messages.append(message)

        # Keep only last 1000 messages to prevent file bloat
        if len(self.messages) > 1000:
            self.messages = self.messages[-1000:]

        self._save_memory()

    def get_context(self, query: str = None) -> str:
        """Get context from persisted memory."""

        if not self.messages:
            return "No conversation history available."

        # Return last 10 messages as context
        recent_messages = self.messages[-10:]
        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in recent_messages
        ])

        return context

    def _load_memory(self) -> List[Dict[str, Any]]:
        """Load memory from disk."""

        if not os.path.exists(self.memory_file):
            return []

        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Warning: Could not load memory from {self.memory_file}")
            return []

    def _save_memory(self):
        """Save memory to disk."""

        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.messages, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def clear_memory(self):
        """Clear all memory."""
        self.messages = []
        self._save_memory()

# Agent with persistent memory
persistent_agent = Agent(
    name="PersistentMemoryAgent",
    instructions="You are an assistant that remembers conversations across sessions.",
    model="gpt-4",
    memory=PersistentMemory("./persistent_memory")
)

# Simulate multiple sessions
print("Session 1:")
persistent_agent.run("Hello! I'm Alice, a software developer.")
persistent_agent.run("I love working with Python and React.")

print("Session 2 (simulated restart):")
# In a real scenario, the agent would be recreated
persistent_agent2 = Agent(
    name="PersistentMemoryAgent",
    instructions="You are an assistant that remembers conversations across sessions.",
    model="gpt-4",
    memory=PersistentMemory("./persistent_memory")
)

response = persistent_agent2.run("What's my name and what do I do?")
print(f"Agent remembers: {response}")
```

### Database-Backed Memory

```python
import sqlite3
from contextlib import contextmanager
from phidata.memory import Memory

class DatabaseMemory(Memory):
    """Memory system backed by SQLite database."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""

        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    session_id TEXT,
                    importance REAL DEFAULT 0.5
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    start_time REAL NOT NULL,
                    end_time REAL,
                    summary TEXT
                )
            """)

            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id)")

    @contextmanager
    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def add_message(self, role: str, content: str, session_id: str = "default"):
        """Add message to database."""

        importance = self._calculate_importance(content)

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO messages (role, content, timestamp, session_id, importance)
                VALUES (?, ?, ?, ?, ?)
            """, (role, content, time.time(), session_id, importance))

    def get_context(self, query: str = None, session_id: str = "default",
                   limit: int = 10) -> str:
        """Get context from database."""

        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT role, content
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (session_id, limit))

            messages = cursor.fetchall()

        # Reverse to get chronological order
        messages.reverse()

        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in messages
        ])

        return context or "No conversation history available."

    def search_messages(self, query: str, session_id: str = "default") -> List[Dict[str, Any]]:
        """Search messages containing query."""

        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT role, content, timestamp, importance
                FROM messages
                WHERE session_id = ?
                AND content LIKE ?
                ORDER BY timestamp DESC
                LIMIT 20
            """, (session_id, f"%{query}%"))

            return [dict(row) for row in cursor.fetchall()]

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary statistics for a session."""

        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) as message_count,
                       AVG(importance) as avg_importance,
                       MIN(timestamp) as start_time,
                       MAX(timestamp) as end_time
                FROM messages
                WHERE session_id = ?
            """, (session_id,))

            row = cursor.fetchone()

            return dict(row) if row else {}

    def start_session(self, session_id: str):
        """Start a new conversation session."""

        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO sessions (id, start_time)
                VALUES (?, ?)
            """, (session_id, time.time()))

    def end_session(self, session_id: str, summary: str = None):
        """End a conversation session."""

        with self._get_connection() as conn:
            conn.execute("""
                UPDATE sessions
                SET end_time = ?, summary = ?
                WHERE id = ?
            """, (time.time(), summary, session_id))

    def _calculate_importance(self, content: str) -> float:
        """Calculate message importance (simplified)."""

        importance_keywords = ["important", "remember", "key", "critical", "essential"]
        content_lower = content.lower()

        score = 0.5
        for keyword in importance_keywords:
            if keyword in content_lower:
                score += 0.1

        return min(1.0, score)

# Agent with database memory
db_memory_agent = Agent(
    name="DatabaseMemoryAgent",
    instructions="You are an assistant with persistent database-backed memory.",
    model="gpt-4",
    memory=DatabaseMemory("./agent_memory.db")
)

# Start a session
session_id = "user_session_123"
db_memory_agent.memory.start_session(session_id)

# Conversation with persistence
conversation = [
    "Hello! I'm working on a Python project.",
    "I need help with database design.",
    "Can you remember that I prefer PostgreSQL over MySQL?",
    "What database do I prefer and what am I working on?"
]

print("Database-backed conversation:")
for message in conversation:
    # Add session context to memory operations
    response = db_memory_agent.run(message)
    print(f"User: {message}")
    print(f"Agent: {response}")
    print("-" * 50)

# End session with summary
db_memory_agent.memory.end_session(session_id, "Completed database advice conversation")

# Show session statistics
stats = db_memory_agent.memory.get_session_summary(session_id)
print(f"Session statistics: {stats}")
```

## Memory Optimization Techniques

### Memory Compression

```python
import zlib
import base64

class CompressedMemory(Memory):
    """Memory system with automatic compression."""

    def __init__(self, max_memory_mb: float = 50.0):
        self.messages = []
        self.compressed_messages = []
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.compression_threshold = 100  # Compress after this many messages

    def add_message(self, role: str, content: str):
        """Add message with compression."""

        message = {
            "role": role,
            "content": content,
            "timestamp": time.time()
        }

        self.messages.append(message)

        # Compress old messages when threshold is reached
        if len(self.messages) >= self.compression_threshold:
            self._compress_old_messages()

        # Check memory usage and compress if needed
        if self._get_memory_usage() > self.max_memory_bytes:
            self._aggressive_compression()

    def get_context(self, query: str = None) -> str:
        """Get context from possibly compressed memory."""

        # Decompress recent messages
        recent_messages = self.messages[-20:]  # Last 20 messages

        # Decompress older messages if needed
        older_messages = []
        if len(self.messages) > 20:
            compressed_count = min(10, len(self.compressed_messages))  # Last 10 compressed
            for compressed in self.compressed_messages[-compressed_count:]:
                older_messages.extend(self._decompress_messages(compressed))

        all_messages = older_messages + recent_messages

        # Format for context
        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in all_messages[-30:]  # Last 30 messages total
        ])

        return context

    def _compress_old_messages(self):
        """Compress older messages to save memory."""

        if len(self.messages) < 50:  # Don't compress if we don't have many messages
            return

        # Keep last 20 messages uncompressed, compress the rest
        recent = self.messages[-20:]
        to_compress = self.messages[:-20]

        if to_compress:
            # Compress as JSON string
            messages_json = json.dumps(to_compress)
            compressed = zlib.compress(messages_json.encode())

            # Store compressed data with metadata
            self.compressed_messages.append({
                "data": compressed,
                "count": len(to_compress),
                "timestamp": time.time()
            })

            # Remove uncompressed versions
            self.messages = recent

    def _aggressive_compression(self):
        """Aggressively compress to meet memory limits."""

        # Compress all but the most recent 5 messages
        if len(self.messages) > 5:
            recent = self.messages[-5:]
            to_compress = self.messages[:-5]

            messages_json = json.dumps(to_compress)
            compressed = zlib.compress(messages_json.encode())

            self.compressed_messages.append({
                "data": compressed,
                "count": len(to_compress),
                "timestamp": time.time()
            })

            self.messages = recent

    def _decompress_messages(self, compressed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompress messages."""

        try:
            decompressed = zlib.decompress(compressed_data["data"])
            messages = json.loads(decompressed.decode())
            return messages
        except Exception as e:
            print(f"Error decompressing messages: {e}")
            return []

    def _get_memory_usage(self) -> int:
        """Get current memory usage in bytes."""

        # Estimate memory usage
        message_memory = len(json.dumps(self.messages).encode())

        compressed_memory = sum(
            len(compressed["data"]) for compressed in self.compressed_messages
        )

        return message_memory + compressed_memory

# Agent with compressed memory
compressed_agent = Agent(
    name="CompressedMemoryAgent",
    instructions="You are an assistant that can maintain long conversations efficiently.",
    model="gpt-4",
    memory=CompressedMemory(max_memory_mb=10.0)  # 10MB limit
)

# Test with many messages
print("Testing memory compression...")
for i in range(100):
    message = f"This is message number {i+1}. It contains some information that might be useful later."
    response = compressed_agent.run(message)

    if (i + 1) % 20 == 0:
        memory_usage = compressed_agent.memory._get_memory_usage()
        print(f"After {i+1} messages: {memory_usage/1024:.1f}KB memory usage")

print(f"Final memory usage: {compressed_agent.memory._get_memory_usage()/1024:.1f}KB")
```

### Memory Indexing and Search

```python
from collections import defaultdict
import re

class IndexedMemory(Memory):
    """Memory system with full-text indexing for fast search."""

    def __init__(self):
        self.messages = []
        self.word_index = defaultdict(list)  # word -> [message_indices]
        self.topic_index = defaultdict(list)  # topic -> [message_indices]

    def add_message(self, role: str, content: str):
        """Add message and update indexes."""

        message_idx = len(self.messages)
        message = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
            "index": message_idx
        }

        self.messages.append(message)

        # Update word index
        self._index_words(content, message_idx)

        # Update topic index
        self._index_topics(content, message_idx)

    def search_messages(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search messages using indexes."""

        query_lower = query.lower()
        query_words = set(query_lower.split())

        # Find messages containing query words
        candidate_indices = set()

        for word in query_words:
            if word in self.word_index:
                candidate_indices.update(self.word_index[word])

        # Score candidates by relevance
        scored_candidates = []

        for idx in candidate_indices:
            message = self.messages[idx]
            score = self._calculate_relevance_score(query_lower, message["content"])
            scored_candidates.append((score, message))

        # Sort by score and return top results
        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        return [msg for score, msg in scored_candidates[:limit]]

    def get_context(self, query: str = None) -> str:
        """Get context with optional query-based retrieval."""

        if query:
            # Use search to find relevant messages
            relevant_messages = self.search_messages(query, limit=10)
        else:
            # Return recent messages
            relevant_messages = self.messages[-10:]

        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in relevant_messages
        ])

        return context

    def _index_words(self, content: str, message_idx: int):
        """Index individual words."""

        # Simple word tokenization (could be enhanced)
        words = re.findall(r'\b\w+\b', content.lower())

        for word in set(words):  # Unique words only
            self.word_index[word].append(message_idx)

    def _index_topics(self, content: str, message_idx: int):
        """Index topics/themes."""

        content_lower = content.lower()

        # Simple topic detection (could use NLP)
        topics = []

        if any(word in content_lower for word in ["python", "code", "programming"]):
            topics.append("programming")

        if any(word in content_lower for word in ["machine learning", "ai", "model"]):
            topics.append("ai_ml")

        if any(word in content_lower for word in ["database", "sql", "data"]):
            topics.append("database")

        if any(word in content_lower for word in ["web", "http", "api"]):
            topics.append("web")

        for topic in topics:
            self.topic_index[topic].append(message_idx)

    def _calculate_relevance_score(self, query: str, content: str) -> float:
        """Calculate relevance score between query and content."""

        query_words = set(query.lower().split())
        content_words = set(re.findall(r'\b\w+\b', content.lower()))

        # Jaccard similarity
        intersection = len(query_words & content_words)
        union = len(query_words | content_words)

        if union == 0:
            return 0.0

        return intersection / union

# Agent with indexed memory
indexed_agent = Agent(
    name="IndexedMemoryAgent",
    instructions="You can recall specific information from our conversation history.",
    model="gpt-4",
    memory=IndexedMemory()
)

# Build conversation with searchable content
conversation_topics = [
    "I love programming in Python. It's my favorite language.",
    "Machine learning is fascinating. I'm studying neural networks.",
    "I work with databases every day. SQL is powerful.",
    "Web development with React and Node.js is exciting.",
    "Python programming involves writing clean, readable code.",
    "Database design requires careful planning of relationships.",
    "Neural networks can learn complex patterns from data."
]

print("Building searchable conversation...")
for topic in conversation_topics:
    indexed_agent.run(f"Tell me about: {topic}")

# Test search capabilities
search_queries = [
    "programming languages",
    "machine learning",
    "database work",
    "Python",
    "neural networks"
]

print("\nTesting memory search...")
for query in search_queries:
    results = indexed_agent.memory.search_messages(query, limit=2)
    print(f"Search: '{query}'")
    print(f"Found {len(results)} relevant messages:")
    for result in results:
        print(f"  - {result['content'][:60]}...")
    print("-" * 50)

# Use search in conversation
search_response = indexed_agent.run("What have I said about programming?")
print(f"Search-based response: {search_response}")
```

This comprehensive memory systems chapter demonstrates how to build sophisticated context-aware agents with various memory architectures, from simple buffers to advanced indexed and compressed systems. The modular design allows for easy customization and extension based on specific use cases. 🚀