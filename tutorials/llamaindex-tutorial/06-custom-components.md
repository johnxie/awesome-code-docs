---
layout: default
title: "Chapter 6: Custom Components"
parent: "LlamaIndex Tutorial"
nav_order: 6
---

# Chapter 6: Custom Components

Welcome to **Chapter 6: Custom Components**. In this part of **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build custom loaders, indexes, query engines, and other components for specialized LlamaIndex applications.

## 🎯 Overview

This chapter covers creating custom components in LlamaIndex to extend functionality for specific use cases, including custom data loaders, specialized indexes, query engines, and processing pipelines.

## 📥 Custom Data Loaders

### Building Custom Readers

```python
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from typing import List
import requests
import json

class GitHubIssuesReader(BaseReader):
    """Custom reader for GitHub repository issues"""

    def __init__(self, token: str = None, github_api_url: str = "https://api.github.com"):
        self.token = token
        self.base_url = github_api_url
        self.session = requests.Session()

        if token:
            self.session.headers.update({
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            })

    def load_data(self, repo_owner: str, repo_name: str, state: str = "open", limit: int = 50) -> List[Document]:
        """Load GitHub issues as documents"""

        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues"
        params = {
            "state": state,
            "per_page": min(limit, 100),
            "sort": "updated",
            "direction": "desc"
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            issues = response.json()
            documents = []

            for issue in issues:
                # Skip pull requests (they also appear in issues endpoint)
                if "pull_request" in issue:
                    continue

                # Create document text
                text_parts = [
                    f"Title: {issue['title']}",
                    f"Body: {issue.get('body', 'No description')}",
                    f"State: {issue['state']}",
                    f"Created: {issue['created_at']}",
                    f"Updated: {issue['updated_at']}",
                    f"Comments: {issue['comments']}"
                ]

                # Add labels if any
                if issue.get("labels"):
                    labels = [label["name"] for label in issue["labels"]]
                    text_parts.append(f"Labels: {', '.join(labels)}")

                text = "\n\n".join(text_parts)

                # Create document
                doc = Document(
                    text=text,
                    metadata={
                        "source": "github_issues",
                        "repo": f"{repo_owner}/{repo_name}",
                        "issue_number": issue["number"],
                        "state": issue["state"],
                        "created_at": issue["created_at"],
                        "updated_at": issue["updated_at"],
                        "author": issue["user"]["login"],
                        "labels": [label["name"] for label in issue.get("labels", [])],
                        "url": issue["html_url"]
                    },
                    id_=f"github_{repo_owner}_{repo_name}_issue_{issue['number']}"
                )

                documents.append(doc)

            print(f"Loaded {len(documents)} GitHub issues from {repo_owner}/{repo_name}")
            return documents

        except Exception as e:
            print(f"Error loading GitHub issues: {e}")
            return []

class SlackReader(BaseReader):
    """Custom reader for Slack workspace data"""

    def __init__(self, token: str):
        from slack_sdk import WebClient
        self.client = WebClient(token=token)

    def load_data(self, channel_names: List[str] = None, days_back: int = 30, limit: int = 1000) -> List[Document]:
        """Load Slack messages from specified channels"""

        import datetime

        # Get channel list
        channels_response = self.client.conversations_list()
        channels = channels_response["channels"]

        # Filter channels if specified
        if channel_names:
            channels = [c for c in channels if c["name"] in channel_names]

        documents = []
        total_messages = 0

        for channel in channels:
            channel_id = channel["id"]
            channel_name = channel["name"]

            # Calculate timestamp for days_back
            since = datetime.datetime.now() - datetime.timedelta(days=days_back)
            oldest = since.timestamp()

            try:
                # Get messages
                messages_response = self.client.conversations_history(
                    channel=channel_id,
                    oldest=oldest,
                    limit=min(limit, 200)  # Slack API limit
                )

                messages = messages_response["messages"]

                # Group messages by thread
                threads = {}
                for msg in messages:
                    thread_ts = msg.get("thread_ts", msg["ts"])
                    if thread_ts not in threads:
                        threads[thread_ts] = []
                    threads[thread_ts].append(msg)

                # Create documents for each thread
                for thread_ts, thread_messages in threads.items():
                    text = self._format_thread_messages(thread_messages)

                    # Find thread starter
                    thread_starter = next(
                        (m for m in thread_messages if m["ts"] == thread_ts),
                        thread_messages[0]
                    )

                    doc = Document(
                        text=text,
                        metadata={
                            "source": "slack",
                            "channel": channel_name,
                            "channel_id": channel_id,
                            "thread_ts": thread_ts,
                            "message_count": len(thread_messages),
                            "starter_user": thread_starter.get("user"),
                            "timestamp": thread_starter.get("ts"),
                            "has_reactions": any("reactions" in m for m in thread_messages)
                        },
                        id_=f"slack_{channel_name}_{thread_ts}"
                    )

                    documents.append(doc)

                total_messages += len(messages)
                print(f"Loaded {len(messages)} messages from #{channel_name}")

            except Exception as e:
                print(f"Error loading channel {channel_name}: {e}")

        print(f"Total: loaded {len(documents)} thread documents from Slack")
        return documents

    def _format_thread_messages(self, messages: List[dict]) -> str:
        """Format thread messages into readable text"""

        formatted = []
        messages_sorted = sorted(messages, key=lambda x: x["ts"])

        for msg in messages_sorted:
            user = msg.get("user", "Unknown")
            text = msg.get("text", "").replace("\n", " ")
            timestamp = msg.get("ts", "")

            formatted.append(f"[{user}] {text}")

        return "\n".join(formatted)

# Usage
# GitHub reader
github_reader = GitHubIssuesReader(token="your-github-token")
github_docs = github_reader.load_data("run-llama", "llama_index", state="open", limit=20)

# Slack reader
# slack_reader = SlackReader(token="your-slack-token")
# slack_docs = slack_reader.load_data(["general", "random"], days_back=7)
```

## 🗂️ Custom Indexes

### Specialized Index Implementation

```python
from llama_index.core.indices.base import BaseIndex
from llama_index.core.schema import BaseNode, IndexNode
from llama_index.core.storage import StorageContext
from llama_index.core.retrievers import BaseRetriever
from typing import List, Dict, Any, Optional
import numpy as np

class TimeWeightedIndex(BaseIndex):
    """Index that considers document recency in retrieval"""

    index_name: str = "time_weighted"

    def __init__(
        self,
        nodes: Optional[List[BaseNode]] = None,
        storage_context: Optional[StorageContext] = None,
        time_decay_factor: float = 0.1,
        **kwargs
    ):
        super().__init__(
            nodes=nodes,
            storage_context=storage_context,
            **kwargs
        )
        self.time_decay_factor = time_decay_factor

    def _build_index_from_nodes(self, nodes: List[BaseNode]) -> Dict[str, Any]:
        """Build index structure from nodes"""

        # Store nodes with timestamps
        index_structure = {}

        for node in nodes:
            # Extract timestamp from metadata
            timestamp = node.metadata.get("created_at", time.time())
            if isinstance(timestamp, str):
                # Parse timestamp (simplified)
                timestamp = time.time() - 86400  # Default to 1 day ago

            index_structure[node.node_id] = {
                "node": node,
                "timestamp": timestamp,
                "embedding": getattr(node, 'embedding', None)
            }

        return {"nodes": index_structure}

    def as_retriever(self, **kwargs) -> BaseRetriever:
        """Return retriever for this index"""
        return TimeWeightedRetriever(
            index=self,
            time_decay_factor=self.time_decay_factor,
            **kwargs
        )

class TimeWeightedRetriever(BaseRetriever):
    """Retriever that applies time weighting"""

    def __init__(self, index: TimeWeightedIndex, time_decay_factor: float = 0.1, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.time_decay_factor = time_decay_factor

    def _retrieve(self, query_bundle):
        """Retrieve with time weighting"""

        # Get all nodes (simplified - in practice, use proper similarity search)
        all_nodes = []
        for node_id, node_data in self.index.index_struct["nodes"].items():
            score = self._calculate_similarity(query_bundle, node_data["node"])
            all_nodes.append({
                "node": node_data["node"],
                "base_score": score,
                "timestamp": node_data["timestamp"]
            })

        # Apply time weighting
        current_time = time.time()
        weighted_nodes = []

        for node_info in all_nodes:
            time_diff_days = (current_time - node_info["timestamp"]) / 86400
            time_weight = 1.0 / (1.0 + self.time_decay_factor * time_diff_days)

            weighted_score = node_info["base_score"] * (0.7 + 0.3 * time_weight)

            node_info["weighted_score"] = weighted_score
            weighted_nodes.append(node_info)

        # Sort by weighted score
        weighted_nodes.sort(key=lambda x: x["weighted_score"], reverse=True)

        # Convert to NodeWithScore
        from llama_index.core.schema import NodeWithScore
        results = [
            NodeWithScore(node=node["node"], score=node["weighted_score"])
            for node in weighted_nodes[:self._similarity_top_k]
        ]

        return results

    def _calculate_similarity(self, query_bundle, node):
        """Calculate similarity between query and node (simplified)"""
        # This is a placeholder - in practice, use proper embedding similarity
        query_terms = set(query_bundle.query_str.lower().split())
        node_terms = set(node.text.lower().split())

        overlap = len(query_terms & node_terms)
        total = len(query_terms | node_terms)

        return overlap / total if total > 0 else 0

class DomainSpecificIndex(BaseIndex):
    """Index optimized for specific domains with custom scoring"""

    index_name: str = "domain_specific"

    def __init__(
        self,
        nodes: Optional[List[BaseNode]] = None,
        storage_context: Optional[StorageContext] = None,
        domain_keywords: Dict[str, List[str]] = None,
        **kwargs
    ):
        super().__init__(
            nodes=nodes,
            storage_context=storage_context,
            **kwargs
        )
        self.domain_keywords = domain_keywords or {}

    def _build_index_from_nodes(self, nodes: List[BaseNode]) -> Dict[str, Any]:
        """Build domain-aware index structure"""

        index_structure = {"nodes": {}, "domain_stats": {}}

        for node in nodes:
            node_id = node.node_id

            # Calculate domain relevance
            domain_scores = self._calculate_domain_relevance(node)

            index_structure["nodes"][node_id] = {
                "node": node,
                "domain_scores": domain_scores,
                "embedding": getattr(node, 'embedding', None)
            }

            # Update domain statistics
            for domain, score in domain_scores.items():
                if domain not in index_structure["domain_stats"]:
                    index_structure["domain_stats"][domain] = []
                index_structure["domain_stats"][domain].append(score)

        return index_structure

    def _calculate_domain_relevance(self, node) -> Dict[str, float]:
        """Calculate relevance scores for different domains"""

        text_lower = node.text.lower()
        domain_scores = {}

        for domain, keywords in self.domain_keywords.items():
            score = 0.0
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 0.1

            # Normalize score
            domain_scores[domain] = min(score, 1.0)

        return domain_scores

    def as_retriever(self, domain_filter: str = None, **kwargs):
        """Return domain-aware retriever"""
        return DomainSpecificRetriever(
            index=self,
            domain_filter=domain_filter,
            **kwargs
        )

class DomainSpecificRetriever(BaseRetriever):
    """Domain-aware retriever"""

    def __init__(self, index: DomainSpecificIndex, domain_filter: str = None, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.domain_filter = domain_filter

    def _retrieve(self, query_bundle):
        """Retrieve with domain filtering"""

        candidates = []
        query_domains = self._identify_query_domains(query_bundle.query_str)

        for node_id, node_data in self.index.index_struct["nodes"].items():
            node = node_data["node"]
            domain_scores = node_data["domain_scores"]

            # Calculate base similarity
            base_score = self._calculate_similarity(query_bundle, node)

            # Apply domain boosting
            domain_boost = 1.0
            if self.domain_filter and self.domain_filter in domain_scores:
                domain_boost = 1.0 + domain_scores[self.domain_filter]

            # Boost for query-relevant domains
            for query_domain in query_domains:
                if query_domain in domain_scores:
                    domain_boost *= (1.0 + domain_scores[query_domain])

            final_score = base_score * domain_boost

            candidates.append({
                "node": node,
                "score": final_score,
                "domain_scores": domain_scores
            })

        # Sort by final score
        candidates.sort(key=lambda x: x["score"], reverse=True)

        # Convert to NodeWithScore
        from llama_index.core.schema import NodeWithScore
        results = [
            NodeWithScore(node=candidate["node"], score=candidate["score"])
            for candidate in candidates[:self._similarity_top_k]
        ]

        return results

    def _identify_query_domains(self, query: str) -> List[str]:
        """Identify relevant domains for the query"""
        query_lower = query.lower()
        relevant_domains = []

        for domain, keywords in self.index.domain_keywords.items():
            if any(keyword.lower() in query_lower for keyword in keywords):
                relevant_domains.append(domain)

        return relevant_domains

    def _calculate_similarity(self, query_bundle, node):
        """Calculate similarity (simplified implementation)"""
        query_terms = set(query_bundle.query_str.lower().split())
        node_terms = set(node.text.lower().split())

        overlap = len(query_terms & node_terms)
        total = len(query_terms | node_terms)

        return overlap / total if total > 0 else 0

# Usage
# Time-weighted index
time_index = TimeWeightedIndex.from_documents(documents, time_decay_factor=0.05)
time_retriever = time_index.as_retriever(similarity_top_k=3)

# Domain-specific index
domain_keywords = {
    "technical": ["algorithm", "implementation", "code", "api", "framework"],
    "business": ["strategy", "revenue", "market", "growth", "profit"],
    "research": ["study", "analysis", "findings", "methodology", "results"]
}

domain_index = DomainSpecificIndex.from_documents(
    documents,
    domain_keywords=domain_keywords
)
domain_retriever = domain_index.as_retriever(domain_filter="technical", similarity_top_k=3)
```

## 🔍 Custom Query Engines

### Specialized Query Engine

```python
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.schema import QueryBundle
from llama_index.core.response.schema import Response
from typing import Any, List

class ConversationalQueryEngine(CustomQueryEngine):
    """Query engine that maintains conversation context"""

    def __init__(self, base_retriever, llm, memory_size: int = 5):
        self.base_retriever = base_retriever
        self.llm = llm
        self.memory_size = memory_size
        self.conversation_history = []

    def custom_query(self, query_str: str) -> Response:
        """Process query with conversation context"""

        # Add current query to history
        self.conversation_history.append(f"User: {query_str}")

        # Keep only recent messages
        if len(self.conversation_history) > self.memory_size * 2:  # *2 for user/assistant pairs
            self.conversation_history = self.conversation_history[-self.memory_size * 2:]

        # Retrieve relevant documents
        query_bundle = QueryBundle(query_str=query_str)
        retrieved_nodes = self.base_retriever.retrieve(query_bundle)

        # Build context with conversation history
        context_parts = []

        # Add conversation history (recent first)
        if self.conversation_history:
            context_parts.append("Recent conversation:")
            for msg in self.conversation_history[-4:]:  # Last 4 messages
                context_parts.append(msg)
            context_parts.append("")

        # Add retrieved documents
        context_parts.append("Relevant information:")
        for i, node in enumerate(retrieved_nodes[:3]):
            context_parts.append(f"Document {i+1}: {node.node.text[:300]}...")
        context_parts.append("")

        context = "\n".join(context_parts)

        # Generate response
        prompt = f"""
        You are a helpful AI assistant. Use the provided context to answer the user's question.
        Maintain the conversation flow and reference previous exchanges when relevant.

        Context:
        {context}

        Current question: {query_str}

        Answer:"""

        response_text = self.llm.complete(prompt)

        # Add assistant response to history
        self.conversation_history.append(f"Assistant: {response_text}")

        return Response(
            response=str(response_text),
            source_nodes=retrieved_nodes,
            metadata={"conversation_length": len(self.conversation_history)}
        )

class MultiPerspectiveQueryEngine(CustomQueryEngine):
    """Query engine that provides multiple perspectives on a topic"""

    def __init__(self, retrievers, llm, perspectives: List[str] = None):
        self.retrievers = retrievers  # Dict of named retrievers
        self.llm = llm
        self.perspectives = perspectives or [
            "technical", "business", "ethical", "practical"
        ]

    def custom_query(self, query_str: str) -> Response:
        """Generate multi-perspective response"""

        perspectives_responses = {}

        # Get different perspectives
        for perspective in self.perspectives:
            if perspective in self.retrievers:
                retriever = self.retrievers[perspective]

                # Retrieve relevant documents
                query_bundle = QueryBundle(query_str=query_str)
                retrieved_nodes = retriever.retrieve(query_bundle)

                # Generate perspective-specific response
                context = "\n".join([
                    f"Document {i+1}: {node.node.text[:200]}..."
                    for i, node in enumerate(retrieved_nodes[:2])
                ])

                prompt = f"""
                Answer the question from a {perspective} perspective:

                Question: {query_str}
                Context: {context}

                {perspective.capitalize()} perspective:"""

                response = self.llm.complete(prompt)
                perspectives_responses[perspective] = {
                    "response": str(response),
                    "source_nodes": retrieved_nodes
                }

        # Combine perspectives
        combined_response = self._combine_perspectives(perspectives_responses, query_str)

        # Collect all source nodes
        all_source_nodes = []
        for persp_data in perspectives_responses.values():
            all_source_nodes.extend(persp_data["source_nodes"])

        return Response(
            response=combined_response,
            source_nodes=all_source_nodes,
            metadata={
                "perspectives": list(perspectives_responses.keys()),
                "perspective_count": len(perspectives_responses)
            }
        )

    def _combine_perspectives(self, perspectives_responses, original_query):
        """Combine multiple perspectives into coherent response"""

        combination_prompt = f"""
        Synthesize the following perspectives on the question: "{original_query}"

        {"".join([f"{persp.title()} perspective: {data['response'][:200]}..." for persp, data in perspectives_responses.items()])}

        Provide a comprehensive answer that integrates all perspectives:"""

        combined_response = self.llm.complete(combination_prompt)

        return str(combined_response)

# Usage
# Conversational query engine
conversational_engine = ConversationalQueryEngine(
    base_retriever=vector_index.as_retriever(),
    llm=OpenAI(model="gpt-4")
)

# Multi-perspective query engine
perspective_retrievers = {
    "technical": vector_index.as_retriever(),
    "business": summary_index.as_retriever(),
    "ethical": keyword_index.as_retriever()
}

multi_perspective_engine = MultiPerspectiveQueryEngine(
    retrievers=perspective_retrievers,
    llm=OpenAI(model="gpt-4")
)

# Test conversational
response1 = conversational_engine.custom_query("What is machine learning?")
response2 = conversational_engine.custom_query("How does it relate to AI?")
print(f"Conversational response 1: {response1.response[:200]}...")
print(f"Conversational response 2: {response2.response[:200]}...")

# Test multi-perspective
perspective_response = multi_perspective_engine.custom_query("Should companies use AI?")
print(f"Multi-perspective response: {perspective_response.response[:300]}...")
```

## 🔧 Custom Post-Processors

### Advanced Post-Processing

```python
from llama_index.core.postprocessor import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore
from typing import List, Optional
import numpy as np

class DiversityPostprocessor(BaseNodePostprocessor):
    """Post-processor that ensures result diversity"""

    def __init__(self, similarity_threshold: float = 0.8, max_nodes: int = 5):
        self.similarity_threshold = similarity_threshold
        self.max_nodes = max_nodes

    def _postprocess_nodes(self, nodes: List[NodeWithScore], query_bundle=None) -> List[NodeWithScore]:
        """Filter nodes to ensure diversity"""

        if len(nodes) <= self.max_nodes:
            return nodes

        selected_nodes = [nodes[0]]  # Always keep the top result

        for node in nodes[1:]:
            # Check similarity with already selected nodes
            is_diverse = True

            for selected_node in selected_nodes:
                similarity = self._calculate_similarity(node.node, selected_node.node)

                if similarity > self.similarity_threshold:
                    is_diverse = False
                    break

            if is_diverse:
                selected_nodes.append(node)

                if len(selected_nodes) >= self.max_nodes:
                    break

        return selected_nodes

    def _calculate_similarity(self, node1, node2) -> float:
        """Calculate similarity between two nodes"""
        # Simple text overlap similarity (could use embeddings)
        text1_words = set(node1.text.lower().split())
        text2_words = set(node2.text.lower().split())

        intersection = len(text1_words & text2_words)
        union = len(text1_words | text2_words)

        return intersection / union if union > 0 else 0

class RelevancePostprocessor(BaseNodePostprocessor):
    """Post-processor that boosts relevance based on query analysis"""

    def __init__(self, boost_factor: float = 0.2):
        self.boost_factor = boost_factor

    def _postprocess_nodes(self, nodes: List[NodeWithScore], query_bundle=None) -> List[NodeWithScore]:
        """Boost scores based on query relevance"""

        if not query_bundle:
            return nodes

        query_terms = self._extract_key_terms(query_bundle.query_str)

        boosted_nodes = []

        for node in nodes:
            boost_score = self._calculate_relevance_boost(node.node, query_terms)
            new_score = node.score * (1.0 + boost_score * self.boost_factor)

            boosted_node = NodeWithScore(
                node=node.node,
                score=min(new_score, 1.0)  # Cap at 1.0
            )
            boosted_nodes.append(boosted_node)

        # Re-sort by boosted scores
        boosted_nodes.sort(key=lambda x: x.score, reverse=True)

        return boosted_nodes

    def _extract_key_terms(self, query: str) -> List[str]:
        """Extract key terms from query"""
        # Simple extraction - could use NLP for better results
        words = query.lower().split()
        # Filter out common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        key_terms = [word for word in words if word not in stop_words and len(word) > 2]

        return key_terms

    def _calculate_relevance_boost(self, node, query_terms: List[str]) -> float:
        """Calculate relevance boost for a node"""

        node_text_lower = node.text.lower()
        boost = 0.0

        for term in query_terms:
            if term in node_text_lower:
                boost += 0.1  # Base boost for term presence

                # Additional boost for term frequency
                term_count = node_text_lower.count(term)
                boost += min(term_count * 0.05, 0.2)  # Cap frequency boost

        # Boost for exact phrase matches
        query_phrase = " ".join(query_terms[:3])  # First 3 terms as phrase
        if query_phrase in node_text_lower:
            boost += 0.3

        return min(boost, 1.0)  # Cap total boost

class TimeDecayPostprocessor(BaseNodePostprocessor):
    """Post-processor that applies time-based decay to scores"""

    def __init__(self, decay_factor: float = 0.1, current_time: Optional[float] = None):
        self.decay_factor = decay_factor
        self.current_time = current_time or time.time()

    def _postprocess_nodes(self, nodes: List[NodeWithScore], query_bundle=None) -> List[NodeWithScore]:
        """Apply time decay to node scores"""

        decayed_nodes = []

        for node in nodes:
            # Extract timestamp from node metadata
            timestamp = self._extract_timestamp(node.node)

            if timestamp:
                # Calculate time difference in days
                time_diff_days = (self.current_time - timestamp) / (24 * 3600)

                # Apply decay factor
                decay_multiplier = 1.0 / (1.0 + self.decay_factor * time_diff_days)

                # Apply decay to score
                decayed_score = node.score * decay_multiplier

                decayed_node = NodeWithScore(
                    node=node.node,
                    score=max(decayed_score, 0.0)  # Don't go below 0
                )
                decayed_nodes.append(decayed_node)
            else:
                # No timestamp available, keep original score
                decayed_nodes.append(node)

        # Re-sort by decayed scores
        decayed_nodes.sort(key=lambda x: x.score, reverse=True)

        return decayed_nodes

    def _extract_timestamp(self, node) -> Optional[float]:
        """Extract timestamp from node metadata"""

        # Check various timestamp fields
        timestamp_fields = ["created_at", "timestamp", "date", "published_at"]

        for field in timestamp_fields:
            if field in node.metadata:
                timestamp = node.metadata[field]

                # Handle different timestamp formats
                if isinstance(timestamp, str):
                    try:
                        # Try to parse ISO format
                        from datetime import datetime
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        return dt.timestamp()
                    except:
                        # If parsing fails, try to convert to float
                        try:
                            return float(timestamp)
                        except:
                            continue
                elif isinstance(timestamp, (int, float)):
                    return float(timestamp)

        return None

# Usage
# Diversity post-processor
diversity_processor = DiversityPostprocessor(similarity_threshold=0.7, max_nodes=3)

# Relevance post-processor
relevance_processor = RelevancePostprocessor(boost_factor=0.3)

# Time decay post-processor
time_decay_processor = TimeDecayPostprocessor(decay_factor=0.05)

# Apply post-processors to query engine
query_engine = vector_index.as_query_engine(
    similarity_top_k=10,
    node_postprocessors=[
        diversity_processor,
        relevance_processor,
        time_decay_processor
    ]
)

# Query with post-processing
response = query_engine.query("recent developments in AI")
print(f"Post-processed response: {response}")

# Check source nodes (should be diverse and relevant)
for i, node in enumerate(response.source_nodes[:3]):
    print(f"Node {i+1} score: {node.score:.3f}")
    print(f"Node {i+1} preview: {node.node.text[:100]}...")
    print("---")
```

## 🎯 Best Practices

### Component Design

1. **Follow LlamaIndex patterns** for compatibility and consistency
2. **Implement proper serialization** for pipeline persistence
3. **Add comprehensive error handling** and validation
4. **Document component interfaces** and usage examples
5. **Write unit tests** for component functionality

### Performance Optimization

1. **Implement efficient algorithms** for custom operations
2. **Use async operations** where appropriate
3. **Cache expensive computations** when possible
4. **Profile and optimize** bottleneck operations
5. **Handle large datasets** with streaming or batching

### Integration Guidelines

1. **Ensure compatibility** with existing LlamaIndex components
2. **Follow naming conventions** and interface patterns
3. **Provide configuration options** for flexibility
4. **Handle edge cases** gracefully
5. **Support both sync and async** operations when applicable

## 📈 Next Steps

With custom components mastered, you're ready to:

- **[Chapter 7: Production Deployment](07-production-deployment.md)** - Scaling LlamaIndex applications for production
- **[Chapter 8: Monitoring & Optimization](08-monitoring-optimization.md)** - Performance tuning and observability

---

**Ready for production deployment? Continue to [Chapter 7: Production Deployment](07-production-deployment.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `node`, `nodes` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Custom Components` as an operating subsystem inside **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `timestamp`, `response`, `score` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Custom Components` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `node` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `nodes`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/run-llama/llama_index)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `node` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Advanced RAG Patterns](05-advanced-rag.md)
- [Next Chapter: Chapter 7: Production Deployment](07-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
