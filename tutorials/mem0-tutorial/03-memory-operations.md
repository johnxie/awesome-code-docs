---
layout: default
title: "Chapter 3: Core Memory Operations"
parent: "Mem0 Tutorial"
nav_order: 3
---

# Chapter 3: Core Memory Operations

> Master the fundamental operations for adding, retrieving, and managing memories in Mem0.

## 🎯 Overview

This chapter covers the core operations you can perform with Mem0 memories, including creating, retrieving, updating, and deleting memories. You'll learn how to effectively manage memory content and metadata for optimal AI agent performance.

## ➕ Adding Memories

### Basic Memory Creation

```python
from mem0 import Memory
import json

def basic_memory_operations():
    """Demonstrate basic memory creation operations"""

    # Initialize memory
    memory = Memory()

    # Add simple memories
    memory.add("User prefers concise responses")
    memory.add("User is a software developer")
    memory.add("User works with Python and machine learning")

    # Add memories with metadata
    memory.add(
        "User has experience with TensorFlow and PyTorch",
        metadata={
            "category": "technical_skills",
            "confidence": 0.9,
            "verified": True
        }
    )

    # Add memories for specific users
    memory.add(
        "Alice prefers morning meetings",
        user_id="alice_123",
        metadata={"preference_type": "scheduling"}
    )

    memory.add(
        "Bob is allergic to peanuts",
        user_id="bob_456",
        metadata={"category": "health", "severity": "critical"}
    )

    print("Basic memories added successfully")

def advanced_memory_creation():
    """Advanced memory creation with rich metadata"""

    memory = Memory()

    # Memory with temporal context
    memory.add(
        "User completed the machine learning certification course",
        metadata={
            "event_type": "achievement",
            "timestamp": "2024-01-15T10:30:00Z",
            "category": "education",
            "skill_level": "intermediate",
            "completion_status": "completed"
        }
    )

    # Memory with relationships
    memory.add(
        "User collaborated with team lead on AI project",
        metadata={
            "event_type": "collaboration",
            "participants": ["user", "team_lead"],
            "project": "ai_chatbot",
            "outcome": "successful_deployment",
            "duration_hours": 40
        }
    )

    # Memory with sentiment and emotion
    memory.add(
        "User was frustrated with the slow API response times",
        metadata={
            "sentiment": "negative",
            "emotion": "frustration",
            "context": "performance_issue",
            "impact": "productivity",
            "resolution_needed": True
        }
    )

    # Memory with location context
    memory.add(
        "User attended the AI conference in San Francisco",
        metadata={
            "event_type": "conference",
            "location": "San Francisco, CA",
            "topic": "artificial_intelligence",
            "duration_days": 3,
            "networking_opportunities": True
        }
    )

    print("Advanced memories with rich metadata added")

def batch_memory_operations():
    """Add multiple memories efficiently"""

    memory = Memory()

    # Prepare batch of memories
    memory_batch = [
        {
            "content": "User prefers email notifications over SMS",
            "metadata": {"communication_preference": "email"}
        },
        {
            "content": "User's favorite programming language is Python",
            "metadata": {"technical_preference": "python", "experience_years": 5}
        },
        {
            "content": "User has a meeting every Monday at 9 AM",
            "metadata": {"schedule_type": "recurring", "day": "monday", "time": "09:00"}
        },
        {
            "content": "User is interested in renewable energy technologies",
            "metadata": {"interest_area": "sustainability", "subtopic": "renewable_energy"}
        },
        {
            "content": "User prefers dark mode in applications",
            "metadata": {"ui_preference": "dark_mode", "accessibility": "improved"}
        }
    ]

    # Add memories in batch
    memory_ids = []
    for mem_data in memory_batch:
        memory_id = memory.add(
            mem_data["content"],
            metadata=mem_data["metadata"]
        )
        memory_ids.append(memory_id)

    print(f"Added {len(memory_ids)} memories in batch")
    return memory_ids

# Usage
basic_memory_operations()
advanced_memory_creation()
batch_memory_ids = batch_memory_operations()
```

## 🔍 Retrieving Memories

### Basic Memory Search

```python
def basic_memory_retrieval():
    """Demonstrate basic memory retrieval operations"""

    memory = Memory()

    # Add some test memories
    test_memories = [
        "User likes coffee in the morning",
        "User prefers working from home",
        "User is learning about machine learning",
        "User has a cat named Whiskers",
        "User enjoys reading science fiction books"
    ]

    for mem in test_memories:
        memory.add(mem)

    # Basic search
    results = memory.search("User likes")
    print(f"Found {len(results)} memories containing 'User likes'")

    for result in results:
        print(f"  - {result['content']}")

    # Search with different queries
    search_queries = [
        "coffee",
        "work",
        "machine learning",
        "cat",
        "books"
    ]

    for query in search_queries:
        results = memory.search(query)
        print(f"Search '{query}': {len(results)} results")

def user_specific_retrieval():
    """Retrieve memories for specific users"""

    memory = Memory()

    # Add memories for different users
    users_memories = {
        "alice": [
            "Alice prefers tea over coffee",
            "Alice is a morning person",
            "Alice works as a data scientist"
        ],
        "bob": [
            "Bob likes to work late at night",
            "Bob prefers coffee over tea",
            "Bob is a software engineer"
        ],
        "charlie": [
            "Charlie enjoys afternoon meetings",
            "Charlie prefers energy drinks",
            "Charlie works as a product manager"
        ]
    }

    # Add memories with user IDs
    for user_id, memories in users_memories.items():
        for mem_content in memories:
            memory.add(mem_content, user_id=user_id)

    # Retrieve memories for specific users
    for user_id in users_memories.keys():
        user_memories = memory.search("", user_id=user_id)  # Empty query gets all
        print(f"\n{user_id.upper()}'s memories ({len(user_memories)} total):")
        for mem in user_memories:
            print(f"  - {mem['content']}")

    # Cross-user search (should not return results from other users)
    alice_results = memory.search("coffee", user_id="alice")
    bob_results = memory.search("coffee", user_id="bob")

    print(f"\nUser-specific search results:")
    print(f"Alice searching 'coffee': {len(alice_results)} results")
    print(f"Bob searching 'coffee': {len(bob_results)} results")

def metadata_based_retrieval():
    """Retrieve memories based on metadata filters"""

    memory = Memory()

    # Add memories with different metadata
    memories_with_metadata = [
        {
            "content": "User completed advanced Python course",
            "metadata": {"category": "education", "skill_level": "advanced", "subject": "python"}
        },
        {
            "content": "User attended machine learning workshop",
            "metadata": {"category": "education", "skill_level": "intermediate", "subject": "ml"}
        },
        {
            "content": "User prefers dark theme in code editors",
            "metadata": {"category": "preference", "type": "ui", "tool": "editor"}
        },
        {
            "content": "User likes working in quiet environments",
            "metadata": {"category": "preference", "type": "environment", "noise_level": "quiet"}
        },
        {
            "content": "User has 5 years of experience in software development",
            "metadata": {"category": "experience", "years": 5, "field": "software"}
        }
    ]

    for mem_data in memories_with_metadata:
        memory.add(mem_data["content"], metadata=mem_data["metadata"])

    # Search with metadata filters (conceptual - actual implementation may vary)
    print("Memories by category:")

    # In practice, you would use the search API with filters
    all_memories = memory.search("")  # Get all memories

    # Manual filtering by metadata
    categories = {}
    for mem in all_memories:
        category = mem.get("metadata", {}).get("category", "uncategorized")
        if category not in categories:
            categories[category] = []
        categories[category].append(mem)

    for category, mems in categories.items():
        print(f"  {category}: {len(mems)} memories")

# Usage
basic_memory_retrieval()
user_specific_retrieval()
metadata_based_retrieval()
```

### Advanced Retrieval Patterns

```python
import time
from typing import List, Dict, Any

class AdvancedMemoryRetriever:
    """Advanced memory retrieval with sophisticated patterns"""

    def __init__(self):
        self.memory = Memory()

    def contextual_retrieval(self, query: str, context_window: int = 3) -> List[Dict[str, Any]]:
        """Retrieve memories with surrounding context"""

        # Get initial results
        initial_results = self.memory.search(query, limit=context_window * 2)

        # For each result, get temporally nearby memories
        contextual_results = []

        for result in initial_results:
            result_time = result.get("metadata", {}).get("timestamp", time.time())

            # Get memories before and after this one
            before_memories = self._get_temporal_context(
                result_time, direction="before", limit=context_window//2
            )
            after_memories = self._get_temporal_context(
                result_time, direction="after", limit=context_window//2
            )

            # Combine into contextual group
            context_group = {
                "main_memory": result,
                "before_context": before_memories,
                "after_context": after_memories,
                "temporal_span": len(before_memories) + len(after_memories) + 1
            }

            contextual_results.append(context_group)

        return contextual_results

    def _get_temporal_context(self, reference_time: float, direction: str = "before",
                            limit: int = 2) -> List[Dict[str, Any]]:
        """Get memories in temporal context"""

        # This is a conceptual implementation
        # In practice, you would query the memory store with time filters

        all_memories = self.memory.search("", limit=100)  # Get many memories

        # Filter by time
        contextual_memories = []
        for mem in all_memories:
            mem_time = mem.get("metadata", {}).get("timestamp", time.time())

            if direction == "before" and mem_time < reference_time:
                contextual_memories.append(mem)
            elif direction == "after" and mem_time > reference_time:
                contextual_memories.append(mem)

            if len(contextual_memories) >= limit:
                break

        # Sort by time
        contextual_memories.sort(key=lambda x: x.get("metadata", {}).get("timestamp", 0))

        return contextual_memories

    def semantic_similarity_search(self, query: str, similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search memories based on semantic similarity"""

        # Get initial results
        initial_results = self.memory.search(query, limit=20)

        # Calculate semantic similarity scores
        similar_memories = []

        for result in initial_results:
            # In practice, you would calculate embedding similarity
            # This is a simplified version
            content_similarity = self._calculate_content_similarity(query, result["content"])

            if content_similarity >= similarity_threshold:
                result["similarity_score"] = content_similarity
                similar_memories.append(result)

        # Sort by similarity
        similar_memories.sort(key=lambda x: x["similarity_score"], reverse=True)

        return similar_memories

    def _calculate_content_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""

        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0

    def hybrid_search(self, query: str, keyword_weight: float = 0.4,
                     semantic_weight: float = 0.6) -> List[Dict[str, Any]]:
        """Combine keyword and semantic search"""

        # Keyword-based search
        keyword_results = self.memory.search(query, limit=15)

        # Semantic search (simplified)
        semantic_results = self.semantic_similarity_search(query, similarity_threshold=0.5)

        # Combine results
        combined_scores = {}

        # Process keyword results
        for result in keyword_results:
            mem_id = result.get("id", result["content"])
            combined_scores[mem_id] = {
                "memory": result,
                "keyword_score": 1.0,  # All keyword results have full score
                "semantic_score": 0.0,
                "final_score": 0.0
            }

        # Process semantic results
        for result in semantic_results:
            mem_id = result.get("id", result["content"])
            semantic_score = result.get("similarity_score", 0.5)

            if mem_id in combined_scores:
                combined_scores[mem_id]["semantic_score"] = semantic_score
            else:
                combined_scores[mem_id] = {
                    "memory": result,
                    "keyword_score": 0.0,
                    "semantic_score": semantic_score,
                    "final_score": 0.0
                }

        # Calculate final scores
        for mem_id, scores in combined_scores.items():
            final_score = (
                keyword_weight * scores["keyword_score"] +
                semantic_weight * scores["semantic_score"]
            )
            scores["final_score"] = final_score

        # Sort and return top results
        sorted_results = sorted(
            combined_scores.values(),
            key=lambda x: x["final_score"],
            reverse=True
        )

        return [item["memory"] for item in sorted_results[:10]]

    def memory_chain_retrieval(self, initial_query: str, chain_depth: int = 2) -> List[Dict[str, Any]]:
        """Retrieve memories through chaining related concepts"""

        all_retrieved = []
        current_query = initial_query

        for depth in range(chain_depth + 1):
            # Search with current query
            results = self.memory.search(current_query, limit=5)

            # Extract key concepts from results for next iteration
            if depth < chain_depth and results:
                # Combine contents and extract key phrases
                combined_content = " ".join([r["content"] for r in results])
                key_concepts = self._extract_key_concepts(combined_content)
                current_query = " ".join(key_concepts[:3])  # Use top 3 concepts

            all_retrieved.extend(results)

        # Remove duplicates
        seen_ids = set()
        unique_results = []

        for result in all_retrieved:
            mem_id = result.get("id", result["content"])
            if mem_id not in seen_ids:
                seen_ids.add(mem_id)
                unique_results.append(result)

        return unique_results

    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""

        # Simple extraction based on noun phrases (simplified)
        words = text.lower().split()
        concepts = []

        # Look for potential concepts (capitalized words, technical terms)
        for word in words:
            word = word.strip(".,!?")
            if len(word) > 3 and word[0].isupper():
                concepts.append(word)

        return concepts[:5] if concepts else ["general"]

# Usage
advanced_retriever = AdvancedMemoryRetriever()

# Add some test memories
test_memories = [
    "User prefers dark mode in applications",
    "User works as a software engineer",
    "User is learning about artificial intelligence",
    "User attended a machine learning conference",
    "User completed a Python programming course"
]

for mem in test_memories:
    advanced_retriever.memory.add(mem)

# Test different retrieval methods
print("Contextual Retrieval:")
contextual = advanced_retriever.contextual_retrieval("machine learning")
for group in contextual:
    print(f"  Main: {group['main_memory']['content']}")
    print(f"  Context items: {group['temporal_span'] - 1}")

print("\nSemantic Similarity Search:")
semantic = advanced_retriever.semantic_similarity_search("AI and programming")
for mem in semantic[:3]:
    print(f"  {mem['content']} (similarity: {mem.get('similarity_score', 0):.2f})")

print("\nHybrid Search:")
hybrid = advanced_retriever.hybrid_search("programming")
for mem in hybrid[:3]:
    print(f"  {mem['content']}")

print("\nMemory Chain Retrieval:")
chain = advanced_retriever.memory_chain_retrieval("artificial intelligence")
for mem in chain[:3]:
    print(f"  {mem['content']}")
```

## 🔄 Updating and Managing Memories

### Memory Updates

```python
def memory_update_operations():
    """Demonstrate memory update operations"""

    memory = Memory()

    # Add initial memory
    memory_id = memory.add(
        "User prefers morning meetings",
        metadata={"preference_type": "scheduling", "confidence": 0.7}
    )

    print(f"Added memory with ID: {memory_id}")

    # Update memory content
    memory.update(
        memory_id,
        content="User strongly prefers morning meetings before 10 AM",
        metadata={
            "preference_type": "scheduling",
            "confidence": 0.9,
            "time_constraint": "before_10am",
            "updated_at": time.time()
        }
    )

    print("Memory updated with additional details")

    # Retrieve updated memory
    updated_memories = memory.search("morning meetings")
    for mem in updated_memories:
        print(f"Updated memory: {mem['content']}")
        print(f"Metadata: {mem.get('metadata', {})}")

def memory_metadata_management():
    """Manage memory metadata"""

    memory = Memory()

    # Add memory with initial metadata
    memory_id = memory.add(
        "User is proficient in Python programming",
        metadata={
            "skill_category": "programming",
            "language": "python",
            "proficiency_level": "intermediate",
            "years_experience": 3,
            "last_assessed": "2024-01-01"
        }
    )

    # Update specific metadata fields
    updated_metadata = {
        "proficiency_level": "advanced",
        "years_experience": 4,
        "certifications": ["Python Developer Certification"],
        "last_assessed": "2024-01-15",
        "updated_at": time.time()
    }

    memory.update(memory_id, metadata=updated_metadata)

    print("Memory metadata updated")

    # Add usage tracking metadata
    usage_metadata = {
        "access_count": 0,
        "last_accessed": None,
        "usefulness_score": 0.8,
        "context_usage": []
    }

    memory.update(memory_id, metadata=usage_metadata)

    print("Usage tracking metadata added")

def batch_memory_updates():
    """Update multiple memories in batch"""

    memory = Memory()

    # Add multiple memories
    memory_ids = []
    initial_memories = [
        "User likes action movies",
        "User prefers Italian food",
        "User enjoys hiking",
        "User reads mystery novels"
    ]

    for mem_content in initial_memories:
        mem_id = memory.add(mem_content)
        memory_ids.append(mem_id)

    # Batch update with additional metadata
    batch_updates = [
        {
            "id": memory_ids[0],
            "metadata": {"category": "entertainment", "genre": "action", "frequency": "weekly"}
        },
        {
            "id": memory_ids[1],
            "metadata": {"category": "food", "cuisine": "italian", "dietary_restrictions": None}
        },
        {
            "id": memory_ids[2],
            "metadata": {"category": "activities", "type": "outdoor", "difficulty": "moderate"}
        },
        {
            "id": memory_ids[3],
            "metadata": {"category": "entertainment", "genre": "mystery", "format": "novels"}
        }
    ]

    for update in batch_updates:
        memory.update(update["id"], metadata=update["metadata"])

    print(f"Batch updated {len(batch_updates)} memories")

    # Verify updates
    all_memories = memory.search("")  # Get all
    for mem in all_memories:
        metadata = mem.get("metadata", {})
        category = metadata.get("category", "uncategorized")
        print(f"Category: {category} - {mem['content']}")

# Usage
memory_update_operations()
memory_metadata_management()
batch_memory_updates()
```

### Memory Deletion and Cleanup

```python
def memory_deletion_operations():
    """Demonstrate memory deletion operations"""

    memory = Memory()

    # Add test memories
    memory_ids = []
    test_memories = [
        "Temporary session data",
        "Outdated user preference",
        "Completed task information",
        "Important user profile data"
    ]

    for mem_content in test_memories:
        mem_id = memory.add(mem_content)
        memory_ids.append(mem_id)

    print(f"Added {len(memory_ids)} test memories")

    # Delete specific memory
    memory_to_delete = memory_ids[0]  # Delete first memory
    memory.delete(memory_to_delete)
    print(f"Deleted memory: {memory_to_delete}")

    # Delete memories by criteria
    all_memories = memory.search("")  # Get all memories

    memories_to_delete = []
    for mem in all_memories:
        content = mem["content"].lower()
        if "temporary" in content or "outdated" in content:
            memories_to_delete.append(mem["id"])

    for mem_id in memories_to_delete:
        memory.delete(mem_id)
        print(f"Deleted memory by criteria: {mem_id}")

    # Verify remaining memories
    remaining_memories = memory.search("")
    print(f"Remaining memories: {len(remaining_memories)}")

    for mem in remaining_memories:
        print(f"  - {mem['content']}")

def memory_cleanup_strategies():
    """Implement memory cleanup strategies"""

    memory = Memory()

    # Add memories with different ages and importance
    import time
    base_time = time.time()

    cleanup_memories = [
        {
            "content": "Very old and unimportant memory",
            "metadata": {
                "importance": 0.1,
                "created_at": base_time - (365 * 24 * 3600),  # 1 year old
                "last_accessed": base_time - (300 * 24 * 3600)  # 300 days ago
            }
        },
        {
            "content": "Recent but low importance memory",
            "metadata": {
                "importance": 0.2,
                "created_at": base_time - (7 * 24 * 3600),  # 1 week old
                "last_accessed": base_time - (5 * 24 * 3600)  # 5 days ago
            }
        },
        {
            "content": "Old but very important memory",
            "metadata": {
                "importance": 0.9,
                "created_at": base_time - (180 * 24 * 3600),  # 6 months old
                "last_accessed": base_time - (30 * 24 * 3600)  # 30 days ago
            }
        },
        {
            "content": "Recent and important memory",
            "metadata": {
                "importance": 0.8,
                "created_at": base_time - (1 * 24 * 3600),  # 1 day old
                "last_accessed": base_time - (0.5 * 24 * 3600)  # 12 hours ago
            }
        }
    ]

    memory_ids = []
    for mem_data in cleanup_memories:
        mem_id = memory.add(mem_data["content"], metadata=mem_data["metadata"])
        memory_ids.append(mem_id)

    print(f"Added {len(memory_ids)} memories for cleanup testing")

    # Implement cleanup strategy
    def cleanup_memories_strategy(max_age_days: int = 90, min_importance: float = 0.3):
        """Clean up memories based on age and importance"""

        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 3600

        all_memories = memory.search("")  # Get all memories
        memories_to_delete = []

        for mem in all_memories:
            metadata = mem.get("metadata", {})
            created_at = metadata.get("created_at", current_time)
            importance = metadata.get("importance", 0.5)

            age_seconds = current_time - created_at

            # Delete if too old AND not important enough
            if age_seconds > max_age_seconds and importance < min_importance:
                memories_to_delete.append(mem["id"])

        # Delete identified memories
        for mem_id in memories_to_delete:
            memory.delete(mem_id)

        return len(memories_to_delete)

    # Run cleanup
    deleted_count = cleanup_memories_strategy(max_age_days=30, min_importance=0.5)
    print(f"Cleaned up {deleted_count} memories")

    # Show remaining memories
    remaining = memory.search("")
    print(f"Remaining memories: {len(remaining)}")

    for mem in remaining:
        metadata = mem.get("metadata", {})
        importance = metadata.get("importance", 0.5)
        age_days = (time.time() - metadata.get("created_at", time.time())) / (24 * 3600)
        print(".1f"
def memory_archival_system():
    """Implement memory archival system"""

    memory = Memory()

    # Create archival metadata structure
    archival_metadata = {
        "archival_status": "active",  # active, archived, deleted
        "archival_date": None,
        "archival_reason": None,
        "restoration_possible": True,
        "backup_location": None
    }

    # Add memory with archival metadata
    memory_id = memory.add(
        "Important user preference that should be archived",
        metadata={
            "importance": 0.9,
            "category": "preference",
            **archival_metadata
        }
    )

    def archive_memory(mem_id: str, reason: str = "age_based"):
        """Archive a memory instead of deleting it"""

        archival_update = {
            "archival_status": "archived",
            "archival_date": time.time(),
            "archival_reason": reason,
            "restoration_possible": True,
            "backup_location": f"archive/{mem_id}.json"
        }

        memory.update(mem_id, metadata=archival_update)

        # In practice, you would also save to archival storage
        print(f"Archived memory {mem_id} for reason: {reason}")

    def restore_memory(mem_id: str):
        """Restore an archived memory"""

        restoration_update = {
            "archival_status": "active",
            "archival_date": None,
            "archival_reason": None,
            "restored_at": time.time()
        }

        memory.update(mem_id, metadata=restoration_update)
        print(f"Restored memory {mem_id}")

    # Archive the memory
    archive_memory(memory_id, "testing_archival")

    # Check archival status
    archived_memories = memory.search("")  # Get all
    for mem in archived_memories:
        if mem["id"] == memory_id:
            status = mem.get("metadata", {}).get("archival_status")
            print(f"Memory {memory_id} status: {status}")

    # Restore the memory
    restore_memory(memory_id)

    print("Memory archival system demonstrated")

# Usage
memory_deletion_operations()
memory_cleanup_strategies()
memory_archival_system()
```

## 📊 Memory Analytics and Insights

### Memory Usage Analytics

```python
class MemoryAnalytics:
    """Analyze memory usage patterns and insights"""

    def __init__(self):
        self.memory = Memory()

    def generate_memory_report(self, user_id: str = None) -> Dict[str, Any]:
        """Generate comprehensive memory usage report"""

        all_memories = self.memory.search("", user_id=user_id)

        report = {
            "total_memories": len(all_memories),
            "categories": self._analyze_categories(all_memories),
            "temporal_distribution": self._analyze_temporal_distribution(all_memories),
            "importance_distribution": self._analyze_importance_distribution(all_memories),
            "usage_patterns": self._analyze_usage_patterns(all_memories),
            "quality_metrics": self._analyze_quality_metrics(all_memories)
        }

        return report

    def _analyze_categories(self, memories) -> Dict[str, int]:
        """Analyze memory categories"""

        categories = {}
        for mem in memories:
            category = mem.get("metadata", {}).get("category", "uncategorized")
            categories[category] = categories.get(category, 0) + 1

        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))

    def _analyze_temporal_distribution(self, memories) -> Dict[str, int]:
        """Analyze memory creation over time"""

        current_time = time.time()
        distribution = {
            "last_24h": 0,
            "last_week": 0,
            "last_month": 0,
            "last_3months": 0,
            "older": 0
        }

        for mem in memories:
            created_at = mem.get("metadata", {}).get("created_at", current_time)
            age_hours = (current_time - created_at) / 3600

            if age_hours <= 24:
                distribution["last_24h"] += 1
            elif age_hours <= 168:  # 7 days
                distribution["last_week"] += 1
            elif age_hours <= 720:  # 30 days
                distribution["last_month"] += 1
            elif age_hours <= 2160:  # 90 days
                distribution["last_3months"] += 1
            else:
                distribution["older"] += 1

        return distribution

    def _analyze_importance_distribution(self, memories) -> Dict[str, int]:
        """Analyze memory importance distribution"""

        distribution = {
            "critical": 0,  # > 0.8
            "high": 0,      # 0.6 - 0.8
            "medium": 0,    # 0.4 - 0.6
            "low": 0        # < 0.4
        }

        for mem in memories:
            importance = mem.get("metadata", {}).get("importance_score", 0.5)

            if importance > 0.8:
                distribution["critical"] += 1
            elif importance > 0.6:
                distribution["high"] += 1
            elif importance > 0.4:
                distribution["medium"] += 1
            else:
                distribution["low"] += 1

        return distribution

    def _analyze_usage_patterns(self, memories) -> Dict[str, Any]:
        """Analyze memory usage patterns"""

        patterns = {
            "avg_content_length": 0,
            "most_common_words": {},
            "memory_types": {},
            "access_patterns": {}
        }

        total_length = 0
        word_counts = {}
        memory_types = {}
        access_counts = []

        for mem in memories:
            # Content analysis
            content = mem["content"]
            total_length += len(content)

            words = content.lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    word_counts[word] = word_counts.get(word, 0) + 1

            # Type analysis
            mem_type = mem.get("metadata", {}).get("memory_type", "general")
            memory_types[mem_type] = memory_types.get(mem_type, 0) + 1

            # Access pattern analysis
            access_count = mem.get("metadata", {}).get("access_count", 0)
            access_counts.append(access_count)

        patterns["avg_content_length"] = total_length / len(memories) if memories else 0
        patterns["most_common_words"] = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        patterns["memory_types"] = memory_types
        patterns["avg_access_count"] = sum(access_counts) / len(access_counts) if access_counts else 0

        return patterns

    def _analyze_quality_metrics(self, memories) -> Dict[str, Any]:
        """Analyze memory quality metrics"""

        quality = {
            "avg_metadata_completeness": 0,
            "memories_with_metadata": 0,
            "memories_with_timestamps": 0,
            "memories_with_importance": 0
        }

        for mem in memories:
            metadata = mem.get("metadata", {})

            if metadata:
                quality["memories_with_metadata"] += 1

                if "created_at" in metadata or "timestamp" in metadata:
                    quality["memories_with_timestamps"] += 1

                if "importance_score" in metadata or "importance" in metadata:
                    quality["memories_with_importance"] += 1

        total_memories = len(memories)
        if total_memories > 0:
            quality["avg_metadata_completeness"] = quality["memories_with_metadata"] / total_memories

        return quality

    def get_memory_insights(self, user_id: str = None) -> Dict[str, Any]:
        """Generate actionable insights from memory analysis"""

        report = self.generate_memory_report(user_id)

        insights = {
            "recommendations": [],
            "warnings": [],
            "opportunities": []
        }

        # Category balance insights
        categories = report["categories"]
        total_memories = report["total_memories"]

        if categories:
            dominant_category = max(categories.items(), key=lambda x: x[1])
            if dominant_category[1] / total_memories > 0.7:
                insights["warnings"].append(
                    f"Memory heavily skewed toward '{dominant_category[0]}' category ({dominant_category[1]} items)"
                )

        # Temporal insights
        temporal = report["temporal_distribution"]
        recent_memories = temporal["last_24h"] + temporal["last_week"]

        if recent_memories < total_memories * 0.3:
            insights["recommendations"].append(
                "Consider adding more recent memories to improve context awareness"
            )

        # Importance insights
        importance = report["importance_distribution"]
        low_importance = importance.get("low", 0)

        if low_importance > total_memories * 0.5:
            insights["opportunities"].append(
                f"Consider reviewing {low_importance} low-importance memories for cleanup or enhancement"
            )

        # Quality insights
        quality = report["quality_metrics"]
        metadata_completeness = quality["avg_metadata_completeness"]

        if metadata_completeness < 0.5:
            insights["recommendations"].append(
                ".1f"
            )

        return {
            "report": report,
            "insights": insights
        }

# Usage
analytics = MemoryAnalytics()

# Add some test memories for analysis
test_memories = [
    {
        "content": "User prefers morning coffee",
        "metadata": {"category": "preference", "importance_score": 0.8, "created_at": time.time()}
    },
    {
        "content": "User works as a software engineer",
        "metadata": {"category": "professional", "importance_score": 0.9, "created_at": time.time() - 86400}
    },
    {
        "content": "User likes Python programming",
        "metadata": {"category": "technical", "importance_score": 0.7, "created_at": time.time() - 172800}
    },
    {
        "content": "User has a meeting on Tuesday",
        "metadata": {"category": "schedule", "importance_score": 0.3, "created_at": time.time() - 259200}
    }
]

for mem_data in test_memories:
    analytics.memory.add(mem_data["content"], metadata=mem_data["metadata"])

# Generate insights
insights_result = analytics.get_memory_insights()
report = insights_result["report"]
insights = insights_result["insights"]

print("Memory Analytics Report:")
print(f"Total memories: {report['total_memories']}")
print(f"Categories: {report['categories']}")
print(f"Temporal distribution: {report['temporal_distribution']}")

print(f"\nInsights and Recommendations:")
for rec in insights["recommendations"]:
    print(f"💡 {rec}")
for warning in insights["warnings"]:
    print(f"⚠️  {warning}")
for opp in insights["opportunities"]:
    print(f"🎯 {opp}")
```

## 🎯 Best Practices

### Memory Management Guidelines

1. **Content Quality**: Ensure memories contain accurate, relevant information
2. **Metadata Richness**: Include comprehensive metadata for better organization
3. **Regular Cleanup**: Implement automated cleanup of outdated memories
4. **User Context**: Consider user preferences and context when managing memories
5. **Performance Monitoring**: Track memory operations and optimize bottlenecks

### Operational Best Practices

1. **Batch Operations**: Use batch operations for bulk memory management
2. **Error Handling**: Implement robust error handling for memory operations
3. **Backup Strategy**: Regular backups of critical memory data
4. **Access Control**: Implement proper access controls for memory operations
5. **Audit Logging**: Maintain logs of memory operations for compliance

## 📈 Next Steps

With core memory operations mastered, you're ready to:

- **[Chapter 4: Advanced Memory Features](04-advanced-features.md)** - Semantic search, memory consolidation, and optimization
- **[Chapter 5: Integrating with LLMs](05-llm-integration.md)** - Connecting Mem0 with various language models
- **[Chapter 6: Building Memory-Enabled Applications](06-memory-applications.md)** - Real-world use cases and implementation patterns

---

**Ready to explore advanced memory features? Continue to [Chapter 4: Advanced Memory Features](04-advanced-features.md)!** 🚀