---
layout: default
title: "Chapter 4: Memory & Learning"
parent: "SuperAGI Tutorial"
nav_order: 4
---

# Chapter 4: Memory & Learning

> Implement persistent memory systems and learning mechanisms for agents that improve over time.

## Overview

Memory systems enable agents to retain context, learn from experiences, and improve their performance over time. This chapter covers different memory types, implementation patterns, and learning strategies for SuperAGI agents.

## Memory Types

### Short-Term Memory

```python
from superagi.memory import ShortTermMemory
from collections import deque

class ShortTermMemory:
    """Memory for current task context."""

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.messages = deque(maxlen=capacity)
        self.context = {}

    def add_message(self, role: str, content: str, metadata: dict = None):
        """Add a message to short-term memory."""
        self.messages.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })

    def get_recent(self, n: int = 10) -> list:
        """Get n most recent messages."""
        return list(self.messages)[-n:]

    def get_context(self) -> dict:
        """Get current context."""
        return self.context

    def update_context(self, key: str, value: any):
        """Update context variable."""
        self.context[key] = value

    def clear(self):
        """Clear short-term memory."""
        self.messages.clear()
        self.context.clear()

    def to_prompt_context(self) -> str:
        """Convert to string for LLM context."""
        context_parts = []

        for msg in self.get_recent(20):
            context_parts.append(f"{msg['role']}: {msg['content']}")

        return "\n".join(context_parts)
```

### Long-Term Memory

```python
from superagi.memory import LongTermMemory
import json

class LongTermMemory:
    """Persistent memory for experiences and knowledge."""

    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.experiences = []
        self.knowledge_base = {}
        self._load()

    def store_experience(self, experience: dict):
        """Store an experience for future reference."""
        experience["stored_at"] = datetime.now().isoformat()
        experience["id"] = self._generate_id()
        self.experiences.append(experience)
        self._save()

    def store_knowledge(self, category: str, key: str, value: any):
        """Store knowledge in a category."""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        self.knowledge_base[category][key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        self._save()

    def retrieve_experiences(self, query: dict, limit: int = 10) -> list:
        """Retrieve relevant experiences."""
        # Simple filtering (can be enhanced with embeddings)
        relevant = []
        for exp in self.experiences:
            if self._matches_query(exp, query):
                relevant.append(exp)

        # Sort by relevance/recency
        relevant.sort(key=lambda x: x["stored_at"], reverse=True)
        return relevant[:limit]

    def get_knowledge(self, category: str, key: str = None) -> any:
        """Get knowledge by category and optional key."""
        if category not in self.knowledge_base:
            return None
        if key:
            return self.knowledge_base[category].get(key, {}).get("value")
        return self.knowledge_base[category]

    def _matches_query(self, experience: dict, query: dict) -> bool:
        """Check if experience matches query criteria."""
        for key, value in query.items():
            if key not in experience:
                return False
            if experience[key] != value:
                return False
        return True

    def _load(self):
        """Load memory from storage."""
        try:
            with open(f"{self.storage_path}/memory.json", "r") as f:
                data = json.load(f)
                self.experiences = data.get("experiences", [])
                self.knowledge_base = data.get("knowledge_base", {})
        except FileNotFoundError:
            pass

    def _save(self):
        """Save memory to storage."""
        os.makedirs(self.storage_path, exist_ok=True)
        with open(f"{self.storage_path}/memory.json", "w") as f:
            json.dump({
                "experiences": self.experiences,
                "knowledge_base": self.knowledge_base
            }, f, indent=2)
```

### Vector Memory

```python
from superagi.memory import VectorMemory
import numpy as np

class VectorMemory:
    """Memory with semantic search using embeddings."""

    def __init__(self, embedding_model, dimension: int = 384):
        self.embedding_model = embedding_model
        self.dimension = dimension
        self.vectors = []
        self.metadata = []

    def store(self, content: str, metadata: dict = None):
        """Store content with its embedding."""
        embedding = self.embedding_model.encode(content)
        self.vectors.append(embedding)
        self.metadata.append({
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })

    def search(self, query: str, top_k: int = 5, threshold: float = 0.5) -> list:
        """Search for similar content."""
        if not self.vectors:
            return []

        query_embedding = self.embedding_model.encode(query)

        # Calculate similarities
        similarities = []
        for i, vec in enumerate(self.vectors):
            sim = self._cosine_similarity(query_embedding, vec)
            if sim >= threshold:
                similarities.append((i, sim))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top-k results
        results = []
        for idx, sim in similarities[:top_k]:
            results.append({
                **self.metadata[idx],
                "similarity": sim
            })

        return results

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def save(self, path: str):
        """Save vector memory to disk."""
        np.savez(
            path,
            vectors=np.array(self.vectors),
            metadata=self.metadata
        )

    def load(self, path: str):
        """Load vector memory from disk."""
        data = np.load(path, allow_pickle=True)
        self.vectors = data["vectors"].tolist()
        self.metadata = data["metadata"].tolist()
```

### Episodic Memory

```python
class EpisodicMemory:
    """Memory for storing complete episodes/sessions."""

    def __init__(self, max_episodes: int = 100):
        self.max_episodes = max_episodes
        self.episodes = []
        self.current_episode = None

    def start_episode(self, task: dict):
        """Start a new episode."""
        self.current_episode = {
            "id": self._generate_id(),
            "task": task,
            "started_at": datetime.now().isoformat(),
            "events": [],
            "outcome": None
        }

    def record_event(self, event_type: str, data: dict):
        """Record an event in the current episode."""
        if not self.current_episode:
            return

        self.current_episode["events"].append({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

    def end_episode(self, outcome: dict):
        """End the current episode with outcome."""
        if not self.current_episode:
            return

        self.current_episode["ended_at"] = datetime.now().isoformat()
        self.current_episode["outcome"] = outcome

        # Add to episodes list
        self.episodes.append(self.current_episode)

        # Trim if exceeds max
        if len(self.episodes) > self.max_episodes:
            self.episodes = self.episodes[-self.max_episodes:]

        self.current_episode = None

    def get_similar_episodes(self, task: dict, limit: int = 5) -> list:
        """Find episodes with similar tasks."""
        similar = []
        for episode in self.episodes:
            if self._is_similar_task(task, episode["task"]):
                similar.append(episode)

        similar.sort(key=lambda x: x["started_at"], reverse=True)
        return similar[:limit]

    def get_successful_strategies(self, task_type: str) -> list:
        """Get strategies that led to successful outcomes."""
        strategies = []
        for episode in self.episodes:
            if (episode["task"].get("type") == task_type and
                episode["outcome"] and
                episode["outcome"].get("success")):
                strategies.append({
                    "task": episode["task"],
                    "events": episode["events"],
                    "outcome": episode["outcome"]
                })
        return strategies
```

## Integrated Memory System

```python
class IntegratedMemorySystem:
    """Combined memory system for agents."""

    def __init__(self, config: dict):
        self.short_term = ShortTermMemory(
            capacity=config.get("short_term_capacity", 100)
        )
        self.long_term = LongTermMemory(
            storage_path=config.get("storage_path", "./memory")
        )
        self.vector = VectorMemory(
            embedding_model=config.get("embedding_model"),
            dimension=config.get("embedding_dimension", 384)
        )
        self.episodic = EpisodicMemory(
            max_episodes=config.get("max_episodes", 100)
        )

    def remember(self, content: str, memory_type: str = "auto", **kwargs):
        """Store content in appropriate memory."""
        if memory_type == "auto":
            memory_type = self._determine_memory_type(content, kwargs)

        if memory_type == "short_term":
            self.short_term.add_message(
                role=kwargs.get("role", "system"),
                content=content,
                metadata=kwargs.get("metadata")
            )
        elif memory_type == "long_term":
            self.long_term.store_experience({
                "content": content,
                **kwargs
            })
        elif memory_type == "vector":
            self.vector.store(content, metadata=kwargs.get("metadata"))

    def recall(self, query: str, memory_types: list = None, limit: int = 10) -> dict:
        """Recall relevant information from memories."""
        memory_types = memory_types or ["short_term", "vector", "episodic"]
        results = {}

        if "short_term" in memory_types:
            results["short_term"] = self.short_term.get_recent(limit)

        if "vector" in memory_types:
            results["vector"] = self.vector.search(query, top_k=limit)

        if "episodic" in memory_types:
            results["episodic"] = self.episodic.get_similar_episodes(
                {"description": query}, limit=limit
            )

        if "long_term" in memory_types:
            results["long_term"] = self.long_term.retrieve_experiences(
                {"content_contains": query}, limit=limit
            )

        return results

    def get_context_for_task(self, task: dict) -> str:
        """Build context string for a task from all memory types."""
        context_parts = []

        # Recent conversation
        recent = self.short_term.to_prompt_context()
        if recent:
            context_parts.append(f"Recent conversation:\n{recent}")

        # Relevant knowledge
        relevant = self.vector.search(task.get("description", ""), top_k=3)
        if relevant:
            knowledge = "\n".join([r["content"] for r in relevant])
            context_parts.append(f"Relevant knowledge:\n{knowledge}")

        # Past successful approaches
        strategies = self.episodic.get_successful_strategies(task.get("type"))
        if strategies:
            strategy_text = self._summarize_strategies(strategies[:2])
            context_parts.append(f"Past successful approaches:\n{strategy_text}")

        return "\n\n---\n\n".join(context_parts)
```

## Learning Mechanisms

### Experience-Based Learning

```python
class ExperienceLearner:
    """Learn from past experiences to improve performance."""

    def __init__(self, memory: IntegratedMemorySystem):
        self.memory = memory
        self.learned_patterns = []

    def learn_from_episode(self, episode: dict):
        """Extract learnings from a completed episode."""
        if not episode.get("outcome"):
            return

        # Analyze what worked or didn't work
        analysis = self._analyze_episode(episode)

        # Extract patterns
        if episode["outcome"].get("success"):
            self._extract_success_pattern(episode, analysis)
        else:
            self._extract_failure_pattern(episode, analysis)

    def _analyze_episode(self, episode: dict) -> dict:
        """Analyze an episode for learnings."""
        events = episode["events"]

        return {
            "total_steps": len(events),
            "tool_usage": self._analyze_tool_usage(events),
            "decision_points": self._find_decision_points(events),
            "bottlenecks": self._identify_bottlenecks(events)
        }

    def _extract_success_pattern(self, episode: dict, analysis: dict):
        """Extract pattern from successful episode."""
        pattern = {
            "type": "success",
            "task_type": episode["task"].get("type"),
            "effective_tools": analysis["tool_usage"]["most_effective"],
            "key_decisions": analysis["decision_points"],
            "approach": self._summarize_approach(episode)
        }
        self.learned_patterns.append(pattern)
        self.memory.long_term.store_knowledge(
            category="success_patterns",
            key=f"{episode['task'].get('type')}_{len(self.learned_patterns)}",
            value=pattern
        )

    def get_recommendations(self, task: dict) -> list:
        """Get recommendations based on learned patterns."""
        task_type = task.get("type")
        relevant_patterns = [
            p for p in self.learned_patterns
            if p["task_type"] == task_type and p["type"] == "success"
        ]

        recommendations = []
        for pattern in relevant_patterns:
            recommendations.append({
                "tools": pattern["effective_tools"],
                "approach": pattern["approach"],
                "confidence": self._calculate_confidence(pattern)
            })

        return recommendations
```

### Feedback Learning

```python
class FeedbackLearner:
    """Learn from explicit feedback."""

    def __init__(self, memory: IntegratedMemorySystem):
        self.memory = memory
        self.feedback_history = []

    def record_feedback(self, action: dict, feedback: dict):
        """Record feedback for an action."""
        record = {
            "action": action,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        self.feedback_history.append(record)

        # Learn from feedback
        self._process_feedback(record)

    def _process_feedback(self, record: dict):
        """Process feedback to update learning."""
        feedback = record["feedback"]

        if feedback.get("rating", 0) >= 4:
            # Positive feedback - reinforce behavior
            self.memory.long_term.store_knowledge(
                category="positive_actions",
                key=record["action"].get("type"),
                value={
                    "action": record["action"],
                    "feedback": feedback,
                    "reinforcement_count": self._get_reinforcement_count(record["action"])
                }
            )
        elif feedback.get("rating", 0) <= 2:
            # Negative feedback - learn to avoid
            self.memory.long_term.store_knowledge(
                category="negative_actions",
                key=record["action"].get("type"),
                value={
                    "action": record["action"],
                    "feedback": feedback,
                    "correction": feedback.get("correction")
                }
            )

    def should_avoid_action(self, proposed_action: dict) -> tuple:
        """Check if similar action received negative feedback."""
        negative = self.memory.long_term.get_knowledge("negative_actions")
        if not negative:
            return False, None

        for key, record in negative.items():
            if self._is_similar_action(proposed_action, record["value"]["action"]):
                return True, record["value"].get("correction")

        return False, None
```

### Self-Improvement

```python
class SelfImprovementModule:
    """Module for agent self-improvement."""

    def __init__(self, agent, memory: IntegratedMemorySystem):
        self.agent = agent
        self.memory = memory
        self.performance_metrics = []

    def evaluate_performance(self, task_result: dict) -> dict:
        """Evaluate performance on a task."""
        metrics = {
            "task_id": task_result.get("task_id"),
            "success": task_result.get("success", False),
            "duration": task_result.get("duration"),
            "steps_taken": task_result.get("steps_taken"),
            "errors": task_result.get("errors", 0),
            "timestamp": datetime.now().isoformat()
        }
        self.performance_metrics.append(metrics)
        return metrics

    def identify_improvement_areas(self) -> list:
        """Identify areas needing improvement."""
        if len(self.performance_metrics) < 10:
            return []

        recent = self.performance_metrics[-50:]

        areas = []

        # Check success rate
        success_rate = sum(1 for m in recent if m["success"]) / len(recent)
        if success_rate < 0.8:
            areas.append({
                "area": "success_rate",
                "current": success_rate,
                "target": 0.8,
                "suggestion": "Review failed tasks and learn from errors"
            })

        # Check error rate
        avg_errors = sum(m.get("errors", 0) for m in recent) / len(recent)
        if avg_errors > 1:
            areas.append({
                "area": "error_rate",
                "current": avg_errors,
                "target": 0.5,
                "suggestion": "Add more validation before actions"
            })

        return areas

    def generate_improvement_plan(self) -> dict:
        """Generate a plan for self-improvement."""
        areas = self.identify_improvement_areas()

        plan = {
            "areas": areas,
            "actions": [],
            "generated_at": datetime.now().isoformat()
        }

        for area in areas:
            if area["area"] == "success_rate":
                plan["actions"].append({
                    "type": "analyze_failures",
                    "description": "Analyze recent failures to identify patterns"
                })
            elif area["area"] == "error_rate":
                plan["actions"].append({
                    "type": "improve_validation",
                    "description": "Enhance input validation before tool execution"
                })

        return plan
```

## Memory Optimization

### Memory Consolidation

```python
class MemoryConsolidator:
    """Consolidate and optimize memory storage."""

    def __init__(self, memory: IntegratedMemorySystem):
        self.memory = memory

    def consolidate(self):
        """Run memory consolidation."""
        self._consolidate_short_to_long()
        self._deduplicate_vectors()
        self._summarize_episodes()

    def _consolidate_short_to_long(self):
        """Move important short-term memories to long-term."""
        short_term_messages = self.memory.short_term.messages

        important = [
            msg for msg in short_term_messages
            if self._is_important(msg)
        ]

        for msg in important:
            self.memory.long_term.store_experience({
                "type": "consolidated_memory",
                "content": msg["content"],
                "original_timestamp": msg["timestamp"]
            })

    def _deduplicate_vectors(self):
        """Remove duplicate or highly similar vectors."""
        # Implementation for vector deduplication
        pass

    def _summarize_episodes(self):
        """Create summaries of old episodes to save space."""
        old_episodes = [
            ep for ep in self.memory.episodic.episodes
            if self._is_old(ep)
        ]

        for episode in old_episodes:
            summary = self._create_episode_summary(episode)
            self.memory.long_term.store_knowledge(
                category="episode_summaries",
                key=episode["id"],
                value=summary
            )
```

## Summary

In this chapter, you've learned:

- **Memory Types**: Short-term, long-term, vector, and episodic memory
- **Integrated System**: Combining memory types for comprehensive recall
- **Learning Mechanisms**: Experience-based, feedback, and self-improvement
- **Optimization**: Memory consolidation and management

## Key Takeaways

1. **Multiple Memory Types**: Different memories for different purposes
2. **Semantic Search**: Vector memory enables finding similar content
3. **Learning from Experience**: Agents improve through past experiences
4. **Feedback Integration**: Explicit feedback guides agent behavior
5. **Self-Improvement**: Agents can identify and address weaknesses

## Next Steps

Now that you understand memory and learning, let's explore Task Planning in Chapter 5 for advanced goal decomposition and execution strategies.

---

**Ready for Chapter 5?** [Task Planning](05-task-planning.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
