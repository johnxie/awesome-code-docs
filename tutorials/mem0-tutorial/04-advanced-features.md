---
layout: default
title: "Chapter 4: Advanced Memory Features"
parent: "Mem0 Tutorial"
nav_order: 4
---

# Chapter 4: Advanced Memory Features

> Unlock the full potential of Mem0 with semantic search, memory consolidation, and advanced optimization techniques.

## 🎯 Overview

This chapter explores Mem0's advanced features including semantic search capabilities, memory consolidation algorithms, intelligent memory optimization, and adaptive learning systems that make AI agents truly intelligent and personalized.

## 🔍 Semantic Search and Retrieval

### Advanced Semantic Search

```python
from mem0 import Memory
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any

class AdvancedSemanticSearch:
    """Advanced semantic search with multiple strategies"""

    def __init__(self):
        self.memory = Memory()
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

    def semantic_search_with_reranking(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Semantic search with re-ranking"""

        # Initial retrieval (get more candidates)
        initial_results = self.memory.search(query, limit=top_k * 3)

        if not initial_results:
            return []

        # Calculate semantic similarities
        query_embedding = self.encoder.encode(query)

        reranked_results = []
        for result in initial_results:
            memory_text = result['content']
            memory_embedding = self.encoder.encode(memory_text)

            # Cosine similarity
            similarity = np.dot(query_embedding, memory_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding)
            )

            result['semantic_score'] = float(similarity)
            reranked_results.append(result)

        # Re-rank by semantic similarity
        reranked_results.sort(key=lambda x: x['semantic_score'], reverse=True)

        return reranked_results[:top_k]

    def multi_vector_search(self, query: str, aspects: List[str] = None) -> List[Dict[str, Any]]:
        """Search across multiple semantic aspects"""

        if aspects is None:
            aspects = ['factual', 'contextual', 'temporal']

        all_results = []

        # Search for each aspect
        for aspect in aspects:
            aspect_query = f"{query} {aspect}"
            results = self.memory.search(aspect_query, limit=5)

            for result in results:
                result['search_aspect'] = aspect
                result['aspect_score'] = self._calculate_aspect_relevance(result['content'], aspect)
                all_results.append(result)

        # Remove duplicates and sort by combined score
        seen_ids = set()
        unique_results = []

        for result in all_results:
            result_id = result.get('id', result['content'])
            if result_id not in seen_ids:
                seen_ids.add(result_id)

                # Combined score: semantic + aspect relevance
                combined_score = result.get('score', 0.5) + result['aspect_score']
                result['combined_score'] = combined_score
                unique_results.append(result)

        unique_results.sort(key=lambda x: x['combined_score'], reverse=True)

        return unique_results[:10]

    def _calculate_aspect_relevance(self, content: str, aspect: str) -> float:
        """Calculate how relevant content is to a specific aspect"""

        aspect_keywords = {
            'factual': ['fact', 'data', 'information', 'true', 'accurate', 'verified'],
            'contextual': ['context', 'situation', 'environment', 'background', 'setting'],
            'temporal': ['time', 'date', 'when', 'recent', 'old', 'history', 'timeline']
        }

        keywords = aspect_keywords.get(aspect, [])
        content_lower = content.lower()

        # Calculate keyword density
        word_count = len(content.split())
        keyword_count = sum(1 for keyword in keywords if keyword in content_lower)

        return keyword_count / max(word_count, 1)

    def fuzzy_semantic_search(self, query: str, fuzziness: float = 0.8) -> List[Dict[str, Any]]:
        """Fuzzy semantic search allowing for imperfect matches"""

        # Get more results than needed
        candidates = self.memory.search(query, limit=20)

        # Calculate fuzzy similarity scores
        query_embedding = self.encoder.encode(query)

        fuzzy_results = []
        for candidate in candidates:
            candidate_embedding = self.encoder.encode(candidate['content'])

            # Cosine similarity
            similarity = np.dot(query_embedding, candidate_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(candidate_embedding)
            )

            # Apply fuzziness threshold
            if similarity >= fuzziness:
                candidate['fuzzy_score'] = float(similarity)
                fuzzy_results.append(candidate)

        # Sort by fuzzy score
        fuzzy_results.sort(key=lambda x: x['fuzzy_score'], reverse=True)

        return fuzzy_results

# Usage
semantic_search = AdvancedSemanticSearch()

# Add test memories
test_memories = [
    "The user prefers morning coffee at 8 AM",
    "User's favorite programming language is Python",
    "The meeting is scheduled for Tuesday at 2 PM",
    "User has 5 years of software development experience",
    "User prefers dark mode in all applications"
]

for memory in test_memories:
    semantic_search.memory.add(memory)

# Test different search methods
query = "programming preferences"

print("Semantic Search with Re-ranking:")
reranked = semantic_search.semantic_search_with_reranking(query, top_k=3)
for result in reranked:
    print(".3f")

print("\nMulti-Vector Search:")
multi_vector = semantic_search.multi_vector_search(query)
for result in multi_vector[:3]:
    print(".3f")

print("\nFuzzy Semantic Search:")
fuzzy = semantic_search.fuzzy_semantic_search(query, fuzziness=0.6)
for result in fuzzy[:3]:
    print(".3f")
```

### Cross-Modal Memory Search

```python
class CrossModalMemorySearch:
    """Search across different types of content (text, images, audio)"""

    def __init__(self):
        self.memory = Memory()
        self.text_encoder = SentenceTransformer('all-MiniLM-L6-v2')
        # In practice, you would initialize image/audio encoders

    def multimodal_search(self, query: str, modalities: List[str] = None) -> List[Dict[str, Any]]:
        """Search across multiple modalities"""

        if modalities is None:
            modalities = ['text', 'image', 'audio']

        results_by_modality = {}

        # Search each modality
        for modality in modalities:
            if modality == 'text':
                results_by_modality[modality] = self._search_text_memories(query)
            elif modality == 'image':
                results_by_modality[modality] = self._search_image_memories(query)
            elif modality == 'audio':
                results_by_modality[modality] = self._search_audio_memories(query)

        # Combine and rank results across modalities
        combined_results = []
        for modality, results in results_by_modality.items():
            for result in results:
                result['modality'] = modality
                result['cross_modal_score'] = self._calculate_cross_modal_score(result, query)
                combined_results.append(result)

        # Sort by cross-modal score
        combined_results.sort(key=lambda x: x['cross_modal_score'], reverse=True)

        return combined_results

    def _search_text_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search text-based memories"""
        return self.memory.search(query, limit=10)

    def _search_image_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search image-based memories (placeholder)"""
        # In practice, this would search through image memories
        # using CLIP or similar multi-modal embeddings

        # Placeholder implementation
        image_memories = [
            {
                'id': 'img_001',
                'content': 'Image memory: user profile picture',
                'modality': 'image',
                'image_description': 'A person working at a computer',
                'score': 0.8
            }
        ]

        # Filter based on query similarity
        relevant_images = []
        query_embedding = self.text_encoder.encode(query)

        for img_mem in image_memories:
            desc_embedding = self.text_encoder.encode(img_mem['image_description'])
            similarity = np.dot(query_embedding, desc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(desc_embedding)
            )

            if similarity > 0.5:
                img_mem['similarity'] = float(similarity)
                relevant_images.append(img_mem)

        return relevant_images

    def _search_audio_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search audio-based memories (placeholder)"""
        # In practice, this would search through transcribed audio memories

        audio_memories = [
            {
                'id': 'audio_001',
                'content': 'Audio memory: user voice recording',
                'modality': 'audio',
                'transcription': 'The user said they prefer working in quiet environments',
                'score': 0.7
            }
        ]

        # Filter based on transcription similarity
        relevant_audio = []
        query_embedding = self.text_encoder.encode(query)

        for audio_mem in audio_memories:
            trans_embedding = self.text_encoder.encode(audio_mem['transcription'])
            similarity = np.dot(query_embedding, trans_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(trans_embedding)
            )

            if similarity > 0.5:
                audio_mem['similarity'] = float(similarity)
                relevant_audio.append(audio_mem)

        return relevant_audio

    def _calculate_cross_modal_score(self, result: Dict[str, Any], query: str) -> float:
        """Calculate cross-modal relevance score"""

        base_score = result.get('score', 0.5)
        modality = result.get('modality', 'text')

        # Modality-specific scoring adjustments
        modality_weights = {
            'text': 1.0,      # Baseline
            'image': 0.8,     # Slightly lower due to description uncertainty
            'audio': 0.9      # Good for intent capture
        }

        modality_weight = modality_weights.get(modality, 0.5)

        # Additional semantic similarity if available
        semantic_score = result.get('similarity', 0.0)

        return (base_score * 0.7 + semantic_score * 0.3) * modality_weight

# Usage
cross_modal_search = CrossModalMemorySearch()

# Add multimodal memories
multimodal_memories = [
    "Text: User prefers quiet working environments",
    "Image: User working at desk with headphones",
    "Audio: User mentioned preferring quiet spaces for concentration"
]

for memory in multimodal_memories:
    cross_modal_search.memory.add(memory)

# Cross-modal search
query = "quiet work environment"
results = cross_modal_search.multimodal_search(query)

print("Cross-Modal Search Results:")
for result in results:
    print(f"  {result['modality']}: {result['content'][:50]}... (score: {result['cross_modal_score']:.3f})")
```

## 🧠 Memory Consolidation and Optimization

### Intelligent Memory Consolidation

```python
from sklearn.cluster import KMeans
import networkx as nx
from collections import defaultdict
import time

class IntelligentMemoryConsolidator:
    """Intelligent memory consolidation using clustering and graph analysis"""

    def __init__(self):
        self.memory = Memory()
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

    def consolidate_similar_memories(self, similarity_threshold: float = 0.85) -> Dict[str, Any]:
        """Consolidate similar memories into consolidated representations"""

        # Get all memories
        all_memories = self.memory.search("", limit=1000)  # Get all

        if len(all_memories) < 2:
            return {"consolidated": 0, "message": "Not enough memories to consolidate"}

        # Generate embeddings for clustering
        contents = [mem['content'] for mem in all_memories]
        embeddings = self.encoder.encode(contents)

        # Perform clustering to find similar memories
        n_clusters = min(len(all_memories) // 3, 10)  # Adaptive cluster count
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(embeddings)

        # Group memories by cluster
        cluster_groups = defaultdict(list)
        for i, cluster_id in enumerate(clusters):
            cluster_groups[cluster_id].append(all_memories[i])

        # Consolidate each cluster
        consolidated_count = 0
        for cluster_id, memories_in_cluster in cluster_groups.items():
            if len(memories_in_cluster) > 1:
                self._consolidate_cluster(memories_in_cluster)
                consolidated_count += len(memories_in_cluster) - 1  # -1 because we keep one consolidated version

        return {
            "consolidated": consolidated_count,
            "clusters_found": len(cluster_groups),
            "message": f"Consolidated {consolidated_count} similar memories into {len(cluster_groups)} clusters"
        }

    def _consolidate_cluster(self, memories: List[Dict[str, Any]]):
        """Consolidate a cluster of similar memories"""

        if len(memories) < 2:
            return

        # Find the most representative memory (highest score or most recent)
        best_memory = max(memories, key=lambda x: (
            x.get('metadata', {}).get('importance_score', 0.5),
            x.get('metadata', {}).get('created_at', 0)
        ))

        # Combine information from all memories
        combined_content = self._merge_memory_contents([mem['content'] for mem in memories])

        # Merge metadata
        combined_metadata = self._merge_memory_metadata([mem.get('metadata', {}) for mem in memories])

        # Update the best memory with consolidated information
        self.memory.update(
            best_memory['id'],
            content=combined_content,
            metadata={
                **combined_metadata,
                'consolidated_from': len(memories),
                'consolidation_date': time.time(),
                'original_memories': [mem['id'] for mem in memories if mem['id'] != best_memory['id']]
            }
        )

        # Mark other memories for archival (don't delete immediately)
        for mem in memories:
            if mem['id'] != best_memory['id']:
                self.memory.update(
                    mem['id'],
                    metadata={
                        **mem.get('metadata', {}),
                        'consolidated_into': best_memory['id'],
                        'archival_status': 'consolidated_duplicate'
                    }
                )

    def _merge_memory_contents(self, contents: List[str]) -> str:
        """Merge multiple memory contents intelligently"""

        if len(contents) == 1:
            return contents[0]

        # Simple merging strategy - combine unique information
        all_sentences = []
        for content in contents:
            sentences = content.split('.')
            all_sentences.extend([s.strip() for s in sentences if s.strip()])

        # Remove duplicates (simple approach)
        unique_sentences = []
        seen_sentences = set()

        for sentence in all_sentences:
            sentence_lower = sentence.lower()
            if sentence_lower not in seen_sentences and len(sentence) > 10:
                seen_sentences.add(sentence_lower)
                unique_sentences.append(sentence)

        # Combine into consolidated content
        consolidated = '. '.join(unique_sentences[:5])  # Limit to top 5 sentences

        return f"Consolidated information: {consolidated}"

    def _merge_memory_metadata(self, metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge metadata from multiple memories"""

        merged = {}

        # Collect all keys
        all_keys = set()
        for metadata in metadata_list:
            all_keys.update(metadata.keys())

        # Merge each key
        for key in all_keys:
            values = [metadata.get(key) for metadata in metadata_list if key in metadata]

            if not values:
                continue

            # Type-specific merging
            if isinstance(values[0], (int, float)):
                merged[key] = sum(values) / len(values)  # Average
            elif isinstance(values[0], list):
                # Combine lists
                combined = []
                for value_list in values:
                    combined.extend(value_list)
                merged[key] = list(set(combined))  # Remove duplicates
            elif isinstance(values[0], dict):
                # Deep merge dictionaries (simplified)
                merged[key] = {**values[0]}  # Take first one
            else:
                # For strings and other types, take the most common
                from collections import Counter
                most_common = Counter(values).most_common(1)[0][0]
                merged[key] = most_common

        return merged

    def optimize_memory_network(self) -> Dict[str, Any]:
        """Optimize memory network using graph analysis"""

        # Get all memories
        all_memories = self.memory.search("", limit=500)

        if len(all_memories) < 3:
            return {"optimized": 0, "message": "Not enough memories for network optimization"}

        # Build memory relationship graph
        G = nx.Graph()

        # Add nodes
        for mem in all_memories:
            G.add_node(mem['id'], content=mem['content'][:50])

        # Add edges based on semantic similarity
        embeddings = self.encoder.encode([mem['content'] for mem in all_memories])

        for i in range(len(all_memories)):
            for j in range(i + 1, len(all_memories)):
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )

                if similarity > 0.7:  # Strong relationship
                    G.add_edge(all_memories[i]['id'], all_memories[j]['id'], weight=similarity)

        # Analyze graph for optimization opportunities
        optimization_ops = 0

        # Find densely connected components (potential consolidation)
        components = list(nx.connected_components(G))
        large_components = [comp for comp in components if len(comp) > 3]

        for component in large_components:
            component_memories = [mem for mem in all_memories if mem['id'] in component]

            if len(component_memories) > 1:
                self._consolidate_cluster(component_memories)
                optimization_ops += len(component_memories) - 1

        # Find isolated memories (potential cleanup candidates)
        isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]

        for isolated_id in isolated_nodes[:10]:  # Limit cleanup
            # Mark for potential cleanup if low importance
            mem = next((m for m in all_memories if m['id'] == isolated_id), None)
            if mem:
                importance = mem.get('metadata', {}).get('importance_score', 0.5)
                if importance < 0.3:
                    self.memory.update(
                        isolated_id,
                        metadata={
                            **mem.get('metadata', {}),
                            'network_isolated': True,
                            'cleanup_candidate': True
                        }
                    )
                    optimization_ops += 1

        return {
            "optimized": optimization_ops,
            "components_found": len(components),
            "large_components": len(large_components),
            "isolated_nodes": len(isolated_nodes),
            "message": f"Optimized {optimization_ops} memories through network analysis"
        }

# Usage
consolidator = IntelligentMemoryConsolidator()

# Add test memories for consolidation
test_memories = [
    "User prefers morning coffee",
    "User likes coffee in the morning",
    "User enjoys morning coffee time",
    "User works as a software engineer",
    "User is a software developer",
    "User develops software applications",
    "User prefers dark mode",
    "User likes dark themes in applications"
]

for memory in test_memories:
    consolidator.memory.add(memory)

# Perform consolidation
consolidation_result = consolidator.consolidate_similar_memories()
print(f"Consolidation: {consolidation_result}")

# Network optimization
network_result = consolidator.optimize_memory_network()
print(f"Network Optimization: {network_result}")
```

### Memory Compression and Summarization

```python
class MemoryCompressor:
    """Compress and summarize memories to save space and improve retrieval"""

    def __init__(self):
        self.memory = Memory()

    def compress_memory_content(self, compression_ratio: float = 0.5) -> Dict[str, Any]:
        """Compress memory content using summarization"""

        all_memories = self.memory.search("", limit=1000)
        compressed_count = 0

        for mem in all_memories:
            content = mem['content']
            original_length = len(content)

            # Only compress long memories
            if original_length > 100:
                compressed_content = self._summarize_content(content, compression_ratio)

                if len(compressed_content) < original_length * 0.8:  # Only update if significantly compressed
                    self.memory.update(
                        mem['id'],
                        content=compressed_content,
                        metadata={
                            **mem.get('metadata', {}),
                            'original_length': original_length,
                            'compressed': True,
                            'compression_ratio': len(compressed_content) / original_length,
                            'compression_date': time.time()
                        }
                    )
                    compressed_count += 1

        return {
            "compressed": compressed_count,
            "total_processed": len(all_memories),
            "compression_ratio": compression_ratio
        }

    def _summarize_content(self, content: str, ratio: float) -> str:
        """Summarize content to reduce length"""

        # Simple extractive summarization
        sentences = content.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 2:
            return content

        # Keep most important sentences
        target_length = max(1, int(len(sentences) * ratio))

        # Simple importance scoring (sentence position and length)
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            # Score based on position (first and last sentences more important)
            position_score = 1.0 if i == 0 or i == len(sentences) - 1 else 0.5

            # Score based on length (longer sentences may be more informative)
            length_score = min(len(sentence.split()) / 20, 1.0)  # Normalize

            # Score based on keywords
            keyword_score = sum(1 for word in ['important', 'key', 'main', 'primary', 'essential'] if word in sentence.lower())
            keyword_score = min(keyword_score, 1.0)

            total_score = position_score * 0.4 + length_score * 0.4 + keyword_score * 0.2
            scored_sentences.append((total_score, sentence))

        # Sort by score and select top sentences
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        selected_sentences = [sentence for _, sentence in scored_sentences[:target_length]]

        # Sort back to original order for coherence
        original_order = []
        sentence_set = set(selected_sentences)
        for sentence in sentences:
            if sentence in sentence_set:
                original_order.append(sentence)

        return '. '.join(original_order)

    def deduplicate_memories(self) -> Dict[str, Any]:
        """Remove exact and near-duplicate memories"""

        all_memories = self.memory.search("", limit=1000)
        duplicates_removed = 0

        # Group by normalized content
        content_groups = defaultdict(list)

        for mem in all_memories:
            # Normalize content for comparison
            normalized = mem['content'].lower().strip()
            normalized = ' '.join(normalized.split())  # Normalize whitespace

            content_groups[normalized].append(mem)

        # Process duplicates
        for normalized_content, memories in content_groups.items():
            if len(memories) > 1:
                # Keep the most important/recent memory
                best_memory = max(memories, key=lambda x: (
                    x.get('metadata', {}).get('importance_score', 0.5),
                    x.get('metadata', {}).get('created_at', 0)
                ))

                # Mark others as duplicates
                for mem in memories:
                    if mem['id'] != best_memory['id']:
                        self.memory.update(
                            mem['id'],
                            metadata={
                                **mem.get('metadata', {}),
                                'duplicate_of': best_memory['id'],
                                'marked_for_cleanup': True
                            }
                        )
                        duplicates_removed += 1

        return {
            "duplicates_removed": duplicates_removed,
            "unique_groups": len(content_groups),
            "total_processed": len(all_memories)
        }

    def optimize_memory_storage(self) -> Dict[str, Any]:
        """Comprehensive memory storage optimization"""

        results = {
            "compression": self.compress_memory_content(),
            "deduplication": self.deduplicate_memories(),
            "cleanup": self._cleanup_optimized_memories()
        }

        # Calculate overall impact
        total_optimized = (
            results["compression"]["compressed"] +
            results["deduplication"]["duplicates_removed"] +
            results["cleanup"]["cleaned_up"]
        )

        results["summary"] = {
            "total_optimized": total_optimized,
            "optimization_date": time.time(),
            "estimated_space_saved": f"{total_optimized * 0.1:.1f}KB"  # Rough estimate
        }

        return results

    def _cleanup_optimized_memories(self) -> Dict[str, int]:
        """Clean up memories marked for optimization"""

        all_memories = self.memory.search("", limit=1000)
        cleaned_up = 0

        for mem in all_memories:
            metadata = mem.get('metadata', {})

            # Remove memories marked for cleanup that are old enough
            if metadata.get('marked_for_cleanup') and metadata.get('duplicate_of'):
                created_at = metadata.get('created_at', time.time())
                age_days = (time.time() - created_at) / (24 * 3600)

                # Only cleanup if duplicate is more than 7 days old
                if age_days > 7:
                    self.memory.delete(mem['id'])
                    cleaned_up += 1

        return {"cleaned_up": cleaned_up}

# Usage
compressor = MemoryCompressor()

# Add test memories
test_memories = [
    "This is a very long memory content that contains a lot of information about user preferences and behaviors. It includes details about how the user likes to work, their preferred tools, and their daily routines. This memory has been written to be quite lengthy for testing compression algorithms.",
    "This is a shorter memory about user preferences.",
    "This is another long memory that discusses user behavior in detail. It covers various aspects of how the user interacts with different systems and applications. The content is quite verbose and contains redundant information that could potentially be compressed.",
    "This is a duplicate memory about user preferences.",  # Duplicate
    "This is another duplicate memory about user preferences."  # Duplicate
]

for memory in test_memories:
    compressor.memory.add(memory)

# Optimize storage
optimization_results = compressor.optimize_memory_storage()

print("Memory Optimization Results:")
for operation, result in optimization_results.items():
    if operation != "summary":
        print(f"  {operation}: {result}")
    else:
        print(f"  Summary: {result}")
```

## 🤖 Adaptive Memory Systems

### Learning from User Interactions

```python
class AdaptiveMemoryLearner:
    """Memory system that learns and adapts from user interactions"""

    def __init__(self):
        self.memory = Memory()
        self.interaction_history = []
        self.learning_model = {
            'query_patterns': defaultdict(int),
            'successful_retrievals': defaultdict(int),
            'user_feedback': defaultdict(float),
            'context_importance': defaultdict(float)
        }

    def record_interaction(self, query: str, retrieved_memories: List[Dict[str, Any]],
                          user_feedback: float = None, selected_memories: List[str] = None):
        """Record a user interaction for learning"""

        interaction = {
            'timestamp': time.time(),
            'query': query,
            'retrieved_count': len(retrieved_memories),
            'user_feedback': user_feedback,
            'selected_memories': selected_memories or [],
            'query_length': len(query.split()),
            'query_type': self._classify_query_type(query)
        }

        self.interaction_history.append(interaction)

        # Update learning model
        self._update_learning_model(interaction)

        # Keep only recent interactions
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]

    def _classify_query_type(self, query: str) -> str:
        """Classify query type for better learning"""

        query_lower = query.lower()

        if any(word in query_lower for word in ['what', 'how', 'explain', 'describe']):
            return 'informational'
        elif any(word in query_lower for word in ['remember', 'recall', 'think']):
            return 'recollection'
        elif any(word in query_lower for word in ['schedule', 'meeting', 'appointment']):
            return 'planning'
        else:
            return 'general'

    def _update_learning_model(self, interaction):
        """Update the learning model based on interaction"""

        query_type = interaction['query_type']
        feedback = interaction.get('user_feedback')

        # Update query patterns
        self.learning_model['query_patterns'][query_type] += 1

        # Update successful retrievals
        if feedback and feedback > 0.7:
            self.learning_model['successful_retrievals'][query_type] += 1

        # Update user feedback scores
        if feedback is not None:
            current_avg = self.learning_model['user_feedback'][query_type]
            count = self.learning_model['query_patterns'][query_type]
            self.learning_model['user_feedback'][query_type] = (
                (current_avg * (count - 1)) + feedback
            ) / count

        # Update context importance
        if interaction['selected_memories']:
            for mem_id in interaction['selected_memories']:
                self.learning_model['context_importance'][mem_id] += 1

    def adapt_retrieval_strategy(self, query: str) -> Dict[str, Any]:
        """Adapt retrieval strategy based on learned patterns"""

        query_type = self._classify_query_type(query)

        # Get learned preferences for this query type
        preferences = {
            'top_k': self._calculate_optimal_k(query_type),
            'search_strategy': self._choose_search_strategy(query_type),
            'reranking': self._should_use_reranking(query_type),
            'context_expansion': self._calculate_context_expansion(query_type)
        }

        return preferences

    def _calculate_optimal_k(self, query_type: str) -> int:
        """Calculate optimal number of results based on learning"""

        base_k = 5

        # Adjust based on successful retrievals
        success_rate = self.learning_model['successful_retrievals'][query_type] / \
                      max(self.learning_model['query_patterns'][query_type], 1)

        if success_rate > 0.8:
            return max(3, base_k - 1)  # More precise
        elif success_rate < 0.3:
            return min(10, base_k + 2)  # More results

        return base_k

    def _choose_search_strategy(self, query_type: str) -> str:
        """Choose optimal search strategy"""

        strategies = {
            'informational': 'semantic',  # Better for detailed queries
            'recollection': 'hybrid',     # Combine keyword and semantic
            'planning': 'temporal',       # Focus on time-based memories
            'general': 'balanced'         # Standard approach
        }

        return strategies.get(query_type, 'balanced')

    def _should_use_reranking(self, query_type: str) -> bool:
        """Determine if reranking should be used"""

        feedback_score = self.learning_model['user_feedback'][query_type]

        # Use reranking if feedback is generally positive (indicating quality matters)
        return feedback_score > 0.6

    def _calculate_context_expansion(self, query_type: str) -> float:
        """Calculate how much to expand context"""

        # More context for complex queries
        expansion_factors = {
            'informational': 1.5,  # More context for detailed answers
            'recollection': 1.2,   # Some expansion for memory recall
            'planning': 1.0,       # Minimal expansion for planning
            'general': 1.1         # Slight expansion
        }

        return expansion_factors.get(query_type, 1.0)

    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learning model"""

        insights = {
            'most_common_query_type': max(
                self.learning_model['query_patterns'].items(),
                key=lambda x: x[1],
                default=('unknown', 0)
            ),
            'best_performing_query_type': max(
                self.learning_model['user_feedback'].items(),
                key=lambda x: x[1],
                default=('unknown', 0.0)
            ),
            'learning_progress': {
                'interactions_learned': len(self.interaction_history),
                'query_types_learned': len(self.learning_model['query_patterns']),
                'feedback_accuracy': sum(self.learning_model['user_feedback'].values()) /
                                   max(len(self.learning_model['user_feedback']), 1)
            }
        }

        return insights

# Usage
adaptive_learner = AdaptiveMemoryLearner()

# Simulate learning from interactions
interactions = [
    {
        'query': 'What are my work preferences?',
        'feedback': 0.8,
        'selected_memories': ['mem_1', 'mem_2']
    },
    {
        'query': 'How do I usually start my day?',
        'feedback': 0.6,
        'selected_memories': ['mem_3']
    },
    {
        'query': 'What meetings do I have today?',
        'feedback': 0.9,
        'selected_memories': ['mem_4']
    }
]

for interaction in interactions:
    # Simulate retrieved memories
    retrieved = [{'id': f'mem_{i}', 'content': f'Memory {i}'} for i in range(1, 6)]
    adaptive_learner.record_interaction(
        interaction['query'],
        retrieved,
        interaction['feedback'],
        interaction['selected_memories']
    )

# Get adaptation recommendations
test_query = "What are my typical work habits?"
adaptation = adaptive_learner.adapt_retrieval_strategy(test_query)

print("Adaptive Retrieval Strategy:")
for param, value in adaptation.items():
    print(f"  {param}: {value}")

# Get learning insights
insights = adaptive_learner.get_learning_insights()
print(f"\nLearning Insights: {insights}")
```

## 🎯 Best Practices

### Advanced Memory Management

1. **Semantic Search**: Use embedding-based search for better relevance
2. **Memory Consolidation**: Regularly consolidate similar memories
3. **Adaptive Learning**: Learn from user interactions to improve retrieval
4. **Multi-Modal Support**: Handle different types of content and memories
5. **Quality Optimization**: Implement compression and deduplication

### Performance Optimization

1. **Batch Processing**: Process multiple operations together
2. **Caching Strategies**: Cache frequent queries and embeddings
3. **Index Optimization**: Maintain efficient search indexes
4. **Resource Monitoring**: Track memory usage and performance metrics
5. **Scalable Architecture**: Design for horizontal scaling

### Learning and Adaptation

1. **User Feedback Integration**: Use feedback to improve memory quality
2. **Pattern Recognition**: Learn from successful retrieval patterns
3. **Dynamic Optimization**: Adapt strategies based on performance
4. **Context Awareness**: Consider user context and preferences
5. **Continuous Improvement**: Regularly update and refine memory systems

## 📈 Next Steps

With advanced memory features mastered, you're ready to:

- **[Chapter 5: Integrating with LLMs](05-llm-integration.md)** - Connecting Mem0 with various language models
- **[Chapter 6: Building Memory-Enabled Applications](06-memory-applications.md)** - Real-world use cases and implementation patterns
- **[Chapter 7: Performance Optimization](07-performance-optimization.md)** - Scaling memory systems for production workloads

---

**Ready to integrate Mem0 with LLMs? Continue to [Chapter 5: Integrating with LLMs](05-llm-integration.md)!** 🚀