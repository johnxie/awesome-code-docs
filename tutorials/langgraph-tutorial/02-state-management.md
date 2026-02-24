---
layout: default
title: "Chapter 2: State Management"
parent: "LangGraph Tutorial"
nav_order: 2
---

# Chapter 2: State Management

Welcome to **Chapter 2: State Management**. In this part of **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Master state management in LangGraph! This chapter covers advanced state patterns, persistence strategies, and memory management techniques for building robust AI applications.

## Advanced State Patterns

### Hierarchical State Management

```python
from typing import TypedDict, List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: str
    preferences: Dict[str, Any]
    session_history: List[str]

class HierarchicalState(TypedDict):
    # Global application state
    app_state: Dict[str, Any]

    # User-specific context
    user_context: UserContext

    # Conversation state
    conversation: Dict[str, Any]

    # Task-specific state
    current_task: Optional[Dict[str, Any]]

    # Memory and history
    memory: Dict[str, Any]

    # Results and outputs
    results: List[Dict[str, Any]]
```

### State Validation and Type Safety

```python
from pydantic import BaseModel, validator
from typing import List, Optional

class ValidatedState(BaseModel):
    messages: List[Dict[str, str]]
    current_step: str
    user_id: Optional[str] = None
    max_steps: int = 10

    @validator('current_step')
    def validate_step(cls, v):
        valid_steps = ['start', 'processing', 'completed', 'error']
        if v not in valid_steps:
            raise ValueError(f'Step must be one of {valid_steps}')
        return v

    @validator('messages')
    def validate_messages(cls, v):
        if len(v) > 100:  # Prevent memory overflow
            raise ValueError('Too many messages')
        return v

# Usage in LangGraph
def validated_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # Validate state
    validated = ValidatedState(**state)

    # Process with validated state
    return {
        **validated.dict(),
        "processed_at": "timestamp"
    }
```

## Memory Management

### Short-term Memory

```python
class ShortTermMemory:
    def __init__(self, max_items: int = 100):
        self.memory = []
        self.max_items = max_items

    def add(self, item: Any):
        self.memory.append(item)
        if len(self.memory) > self.max_items:
            self.memory.pop(0)  # Remove oldest

    def get_recent(self, n: int = 10) -> List[Any]:
        return self.memory[-n:]

    def clear(self):
        self.memory.clear()

def update_short_term_memory(state: HierarchicalState) -> HierarchicalState:
    """Update short-term memory in state"""
    stm = ShortTermMemory()

    # Add current interaction
    stm.add({
        "timestamp": "now",
        "action": state.get("current_task", {}).get("action"),
        "result": state.get("results", [])[-1] if state.get("results") else None
    })

    return {
        **state,
        "memory": {
            **state.get("memory", {}),
            "short_term": stm.memory
        }
    }
```

### Long-term Memory

```python
class LongTermMemory:
    def __init__(self, persistence_layer=None):
        self.memories = {}
        self.persistence = persistence_layer

    def store(self, key: str, value: Any, importance: float = 0.5):
        memory_item = {
            "value": value,
            "importance": importance,
            "timestamp": "now",
            "access_count": 0
        }

        self.memories[key] = memory_item

        if self.persistence:
            self.persistence.save(key, memory_item)

    def retrieve(self, key: str) -> Optional[Any]:
        if key in self.memories:
            self.memories[key]["access_count"] += 1
            return self.memories[key]["value"]

        if self.persistence:
            return self.persistence.load(key)

        return None

    def get_important_memories(self, threshold: float = 0.7) -> Dict[str, Any]:
        return {
            k: v for k, v in self.memories.items()
            if v["importance"] >= threshold
        }
```

## State Persistence

### Checkpoint System

```python
import json
import os
from datetime import datetime

class StateCheckpoint:
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)

    def save_checkpoint(self, state: Dict[str, Any], checkpoint_id: str):
        checkpoint = {
            "id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "state": state
        }

        filename = f"{checkpoint_id}_{int(datetime.now().timestamp())}.json"
        filepath = os.path.join(self.checkpoint_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(checkpoint, f, indent=2, default=str)

        return filepath

    def load_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        # Find latest checkpoint for this ID
        files = [f for f in os.listdir(self.checkpoint_dir) if f.startswith(checkpoint_id)]
        if not files:
            return None

        latest_file = max(files, key=lambda x: os.path.getctime(
            os.path.join(self.checkpoint_dir, x)
        ))

        with open(os.path.join(self.checkpoint_dir, latest_file), 'r') as f:
            checkpoint = json.load(f)

        return checkpoint["state"]

    def list_checkpoints(self) -> List[str]:
        return os.listdir(self.checkpoint_dir)
```

### State Recovery

```python
def recover_from_checkpoint(graph, checkpoint_id: str):
    """Recover graph execution from checkpoint"""
    checkpoint_manager = StateCheckpoint()

    # Load saved state
    recovered_state = checkpoint_manager.load_checkpoint(checkpoint_id)

    if recovered_state:
        print(f"Recovered from checkpoint: {checkpoint_id}")
        return graph.invoke(recovered_state)
    else:
        print(f"No checkpoint found for: {checkpoint_id}")
        return None

def auto_save_checkpoint(state: HierarchicalState, checkpoint_id: str) -> HierarchicalState:
    """Automatically save checkpoint during execution"""
    checkpoint_manager = StateCheckpoint()

    # Save current state
    checkpoint_path = checkpoint_manager.save_checkpoint(state, checkpoint_id)

    return {
        **state,
        "last_checkpoint": checkpoint_path,
        "checkpoint_timestamp": "now"
    }
```

## State Synchronization

### Multi-Agent State Sharing

```python
class SharedStateManager:
    def __init__(self):
        self.shared_state = {}
        self.agent_states = {}
        self.lock = threading.Lock()

    def update_shared_state(self, agent_id: str, updates: Dict[str, Any]):
        with self.lock:
            if agent_id not in self.agent_states:
                self.agent_states[agent_id] = {}

            # Update agent-specific state
            self.agent_states[agent_id].update(updates)

            # Update shared state with relevant information
            shared_updates = {
                k: v for k, v in updates.items()
                if k.startswith("shared_") or k in ["results", "status"]
            }

            self.shared_state.update(shared_updates)

    def get_agent_state(self, agent_id: str) -> Dict[str, Any]:
        return self.agent_states.get(agent_id, {})

    def get_shared_state(self) -> Dict[str, Any]:
        with self.lock:
            return self.shared_state.copy()

    def synchronize_states(self):
        """Synchronize all agent states with shared state"""
        with self.lock:
            for agent_id in self.agent_states:
                # Merge shared state into agent state
                self.agent_states[agent_id].update({
                    k: v for k, v in self.shared_state.items()
                    if k not in self.agent_states[agent_id]
                })
```

## Advanced State Patterns

### State Composition

```python
class StateComposer:
    @staticmethod
    def compose_states(*states: Dict[str, Any]) -> Dict[str, Any]:
        """Compose multiple states into one"""
        composed = {}

        for state in states:
            for key, value in state.items():
                if key not in composed:
                    composed[key] = value
                elif isinstance(composed[key], list) and isinstance(value, list):
                    composed[key].extend(value)
                elif isinstance(composed[key], dict) and isinstance(value, dict):
                    composed[key].update(value)
                else:
                    # Handle conflicts (keep latest)
                    composed[key] = value

        return composed

    @staticmethod
    def decompose_state(state: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
        """Extract specific keys from state"""
        return {k: v for k, v in state.items() if k in keys}
```

### State Versioning

```python
class StateVersionManager:
    def __init__(self):
        self.versions = {}
        self.current_version = 0

    def save_version(self, state: Dict[str, Any]) -> int:
        self.current_version += 1
        self.versions[self.current_version] = {
            "state": state.copy(),
            "timestamp": datetime.now().isoformat(),
            "version": self.current_version
        }
        return self.current_version

    def get_version(self, version: int) -> Optional[Dict[str, Any]]:
        return self.versions.get(version, {}).get("state")

    def rollback_to_version(self, version: int) -> Optional[Dict[str, Any]]:
        if version in self.versions:
            # Create rollback state
            rollback_state = self.versions[version]["state"].copy()
            rollback_state["_rolled_back_from"] = self.current_version
            rollback_state["_rolled_back_to"] = version
            return rollback_state
        return None

    def get_version_history(self) -> List[Dict[str, Any]]:
        return list(self.versions.values())
```

## Performance Optimization

### State Compression

```python
import zlib
import pickle

class StateCompressor:
    @staticmethod
    def compress_state(state: Dict[str, Any]) -> bytes:
        """Compress state for storage"""
        state_bytes = pickle.dumps(state)
        return zlib.compress(state_bytes)

    @staticmethod
    def decompress_state(compressed_state: bytes) -> Dict[str, Any]:
        """Decompress state from storage"""
        state_bytes = zlib.decompress(compressed_state)
        return pickle.loads(state_bytes)

    @staticmethod
    def compress_text_fields(state: Dict[str, Any]) -> Dict[str, Any]:
        """Compress large text fields in state"""
        compressed = state.copy()

        for key, value in compressed.items():
            if isinstance(value, str) and len(value) > 1000:
                compressed[key] = {
                    "_compressed": True,
                    "data": StateCompressor.compress_state({"text": value})
                }

        return compressed

    @staticmethod
    def decompress_text_fields(state: Dict[str, Any]) -> Dict[str, Any]:
        """Decompress text fields in state"""
        decompressed = state.copy()

        for key, value in decompressed.items():
            if isinstance(value, dict) and value.get("_compressed"):
                decompressed_data = StateCompressor.decompress_state(value["data"])
                decompressed[key] = decompressed_data["text"]

        return decompressed
```

## What We've Accomplished

This chapter covered advanced state management techniques including hierarchical state, validation, memory management, persistence, synchronization, composition, versioning, and performance optimization.

## Next Steps

Ready to build complex graphs? In [Chapter 3: Nodes and Edges](03-nodes-edges.md), we'll explore building graph components and managing complex connections between them.

---

**Practice what you've learned:**
1. Implement hierarchical state management for a multi-agent system
2. Build a checkpoint and recovery system
3. Create state validation and type safety
4. Implement memory management with different retention policies
5. Build state synchronization for distributed agents

*How will you manage state in your AI applications?* 🧠

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `state`, `Dict` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: State Management` as an operating subsystem inside **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `memory`, `checkpoint_id`, `List` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: State Management` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `state` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Dict`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langgraph)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `state` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with LangGraph](01-getting-started.md)
- [Next Chapter: Chapter 3: Nodes and Edges](03-nodes-edges.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
