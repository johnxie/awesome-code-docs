---
layout: default
title: "Chapter 5: Advanced RAG Patterns"
parent: "LlamaIndex Tutorial"
nav_order: 5
---

# Chapter 5: Advanced RAG Patterns

> Implement sophisticated RAG architectures with multi-modal data, agents, and hybrid approaches.

## 🎯 Overview

This chapter covers advanced Retrieval-Augmented Generation patterns including multi-modal RAG, agent-based systems, knowledge graphs, and hybrid architectures that combine multiple retrieval and generation strategies.

## 🤖 Agent-Based RAG

### LlamaIndex Agents

```python
from llama_index.core.agent import (
    ReActAgent,
    OpenAIAgent,
    CustomSimpleAgent
)
from llama_index.core.tools import QueryEngineTool, FunctionTool

def create_research_agent(indexes):
    """Create a research agent with multiple knowledge sources"""

    # Create query engines for different domains
    tools = []

    domain_indexes = {
        "technical": indexes.get("technical", vector_index),
        "business": indexes.get("business", vector_index),
        "scientific": indexes.get("scientific", vector_index)
    }

    for domain, index in domain_indexes.items():
        query_engine = index.as_query_engine(similarity_top_k=3)

        tool = QueryEngineTool.from_defaults(
            query_engine=query_engine,
            name=f"{domain}_search",
            description=f"Search {domain} documents for information"
        )
        tools.append(tool)

    # Add custom tools
    def calculate_metrics(formula: str) -> str:
        """Calculate business metrics"""
        try:
            # Simple calculation (in practice, use proper evaluation)
            result = eval(formula.replace('^', '**'))
            return f"Result: {result}"
        except:
            return "Invalid formula"

    calc_tool = FunctionTool.from_defaults(
        fn=calculate_metrics,
        name="calculator",
        description="Calculate mathematical expressions and metrics"
    )
    tools.append(calc_tool)

    # Create ReAct agent
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=OpenAI(model="gpt-4", temperature=0.1),
        verbose=True,
        max_iterations=10
    )

    return agent

def create_openai_agent(indexes):
    """Create OpenAI function calling agent"""

    # Create tools
    tools = []
    for name, index in indexes.items():
        query_engine = index.as_query_engine(similarity_top_k=5)
        tool = QueryEngineTool.from_defaults(
            query_engine=query_engine,
            name=f"search_{name}",
            description=f"Search {name} knowledge base"
        )
        tools.append(tool)

    # OpenAI agent with function calling
    agent = OpenAIAgent.from_tools(
        tools=tools,
        llm=OpenAI(model="gpt-4", temperature=0),
        verbose=True
    )

    return agent

# Usage
indexes = {
    "technical": vector_index,
    "business": summary_index
}

research_agent = create_research_agent(indexes)
openai_agent = create_openai_agent(indexes)

# Complex queries
complex_queries = [
    "Compare the technical requirements and business benefits of implementing AI in healthcare",
    "Calculate the ROI for a machine learning project costing $500K with expected annual savings of $200K"
]

for query in complex_queries:
    print(f"\nQuery: {query}")

    # Use ReAct agent
    react_response = research_agent.chat(query)
    print(f"ReAct Agent: {react_response}")

    # Use OpenAI agent
    openai_response = openai_agent.chat(query)
    print(f"OpenAI Agent: {openai_response}")
```

### Custom Agent Workflows

```python
from llama_index.core.agent import CustomSimpleAgent
from llama_index.core.workflow import Workflow, step
from llama_index.core.schema import NodeWithScore
from typing import List, Dict, Any

class ResearchWorkflow(Workflow):
    """Custom research workflow"""

    def __init__(self, indexes, **kwargs):
        super().__init__(**kwargs)
        self.indexes = indexes
        self.search_history = []

    @step()
    async def analyze_query(self, ctx, query: str) -> str:
        """Analyze query and determine research strategy"""

        # Determine which indexes to search
        query_lower = query.lower()
        relevant_indexes = []

        if any(word in query_lower for word in ["technical", "code", "implementation"]):
            relevant_indexes.append("technical")
        if any(word in query_lower for word in ["business", "cost", "roi", "strategy"]):
            relevant_indexes.append("business")
        if any(word in query_lower for word in ["science", "research", "study"]):
            relevant_indexes.append("scientific")

        if not relevant_indexes:
            relevant_indexes = ["general"]

        await ctx.set("relevant_indexes", relevant_indexes)
        await ctx.set("original_query", query)

        return f"Identified relevant domains: {', '.join(relevant_indexes)}"

    @step()
    async def gather_information(self, ctx, analysis_result: str) -> List[NodeWithScore]:
        """Gather information from relevant sources"""

        relevant_indexes = await ctx.get("relevant_indexes")
        query = await ctx.get("original_query")

        all_results = []

        for index_name in relevant_indexes:
            if index_name in self.indexes:
                retriever = self.indexes[index_name].as_retriever(similarity_top_k=3)
                results = retriever.retrieve(query)
                all_results.extend(results)

        # Sort by score and keep top results
        all_results.sort(key=lambda x: x.score or 0, reverse=True)
        top_results = all_results[:10]

        await ctx.set("search_results", top_results)

        return top_results

    @step()
    async def synthesize_answer(self, ctx, search_results: List[NodeWithScore]) -> str:
        """Synthesize comprehensive answer"""

        query = await ctx.get("original_query")

        # Extract text from results
        context_texts = [result.node.text for result in search_results[:5]]

        # Create synthesis prompt
        synthesis_prompt = f"""
        Based on the following information, provide a comprehensive answer to: {query}

        Context Information:
        {"".join(f"- {text[:200]}..." for text in context_texts)}

        Provide a well-structured answer that synthesizes the key points.
        """

        # Generate answer
        llm = OpenAI(model="gpt-4", temperature=0.1)
        response = llm.complete(synthesis_prompt)

        final_answer = str(response)

        # Store in history
        self.search_history.append({
            "query": query,
            "results_count": len(search_results),
            "answer": final_answer[:200] + "..."
        })

        return final_answer

async def run_research_workflow(query: str, indexes: dict):
    """Run the research workflow"""

    workflow = ResearchWorkflow(indexes=indexes, timeout=60)
    result = await workflow.run(query=query)

    return result

# Usage
async def demonstrate_workflow():
    indexes = {"technical": vector_index, "business": summary_index}

    research_queries = [
        "What are the technical challenges and business opportunities in AI implementation?",
        "How do machine learning models impact business decision making?"
    ]

    for query in research_queries:
        print(f"\nResearching: {query}")

        result = await run_research_workflow(query, indexes)
        print(f"Answer: {result[:300]}...")

# Run demonstration
import asyncio
asyncio.run(demonstrate_workflow())
```

## 🎨 Multi-Modal RAG

### Image and Text Integration

```python
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core.schema import ImageDocument, Document
from llama_index.core.indices.multi_modal import MultiModalVectorStoreIndex

def create_multi_modal_index():
    """Create index for multi-modal content"""

    # Sample multi-modal documents
    documents = [
        Document(
            text="A neural network diagram showing interconnected nodes in layers",
            metadata={"type": "diagram", "topic": "neural_networks"}
        ),
        Document(
            text="Machine learning workflow from data collection to deployment",
            metadata={"type": "flowchart", "topic": "ml_pipeline"}
        )
    ]

    # Add image documents (in practice, you'd have actual image paths)
    image_documents = [
        ImageDocument(
            image_path="neural_network_diagram.png",
            metadata={"description": "Neural network architecture visualization"}
        ),
        ImageDocument(
            image_path="ml_workflow.png",
            metadata={"description": "ML pipeline flowchart"}
        )
    ]

    # Create multi-modal index
    index = MultiModalVectorStoreIndex.from_documents(
        documents + image_documents,
        embed_model="clip"  # CLIP model for image-text embeddings
    )

    return index

def query_multi_modal_index(index):
    """Query multi-modal index"""

    # Multi-modal LLM
    mm_llm = OpenAIMultiModal(
        model="gpt-4-vision-preview",
        max_new_tokens=300
    )

    # Query with text
    text_query = "Explain how neural networks process information"
    query_engine = index.as_query_engine(
        multi_modal_llm=mm_llm,
        similarity_top_k=3
    )

    response = query_engine.query(text_query)
    print(f"Multi-modal response: {response}")

    return response

# Usage (requires actual images and proper setup)
# multi_modal_index = create_multi_modal_index()
# response = query_multi_modal_index(multi_modal_index)
```

### Audio and Video Processing

```python
from llama_index.readers.file import AudioTranscriber
from llama_index.core import Document

def process_audio_content():
    """Process audio files for RAG"""

    # Audio transcription reader
    reader = AudioTranscriber(
        model_name="openai/whisper-base",  # Whisper model
        verbose=True
    )

    # Transcribe audio files
    audio_documents = reader.load_data(
        file_paths=["lecture.mp3", "interview.wav"],
        metadata={"source": "audio_transcription"}
    )

    print(f"Transcribed {len(audio_documents)} audio files")

    # Create searchable index
    index = VectorStoreIndex.from_documents(audio_documents)

    return index

def process_video_content():
    """Process video files by extracting audio and text"""

    # For video: extract audio track, then transcribe
    import moviepy.editor as mp

    def extract_audio_from_video(video_path: str, audio_path: str):
        """Extract audio from video file"""
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        return audio_path

    # Process video files
    video_files = ["presentation.mp4", "tutorial.webm"]

    all_documents = []

    for video_file in video_files:
        # Extract audio
        audio_file = video_file.replace('.mp4', '.wav').replace('.webm', '.wav')
        extract_audio_from_video(video_file, audio_file)

        # Transcribe audio
        reader = AudioTranscriber()
        docs = reader.load_data([audio_file])

        # Add video metadata
        for doc in docs:
            doc.metadata.update({
                "source": "video_transcription",
                "original_video": video_file,
                "duration": "extracted_from_video"
            })

        all_documents.extend(docs)

    # Create index
    index = VectorStoreIndex.from_documents(all_documents)

    return index

# Usage (requires audio/video files and proper libraries)
# audio_index = process_audio_content()
# video_index = process_video_content()
```

## 🕸️ Knowledge Graph RAG

### Graph-Based Retrieval

```python
from llama_index.core.indices.knowledge_graph import KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.llms.openai import OpenAI

def create_knowledge_graph_index(documents):
    """Create knowledge graph index"""

    # Knowledge graph index with graph store
    graph_store = SimpleGraphStore()

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    index = KnowledgeGraphIndex.from_documents(
        documents,
        max_triplets_per_chunk=10,
        include_triplets_in_response=True,
        graph_store=graph_store,
        llm=llm
    )

    return index

def query_knowledge_graph(index):
    """Query knowledge graph with relationships"""

    query_engine = index.as_query_engine(
        include_text=True,
        response_mode="tree_summarize",
        embedding_mode="hybrid",  # Use both graph and vector search
        similarity_top_k=5
    )

    # Graph-aware queries
    graph_queries = [
        "What are the relationships between machine learning and artificial intelligence?",
        "How does neural network connect to deep learning?",
        "What technologies are related to data science?"
    ]

    for query in graph_queries:
        response = query_engine.query(query)
        print(f"Graph Query: {query}")
        print(f"Response: {response}")
        print("---")

    return query_engine

# Usage
kg_index = create_knowledge_graph_index(documents)
kg_query_engine = query_knowledge_graph(kg_index)
```

## 🔄 Hybrid Architectures

### Ensemble RAG

```python
from llama_index.core.query_engine import EnsembleQueryEngine
from llama_index.core.selectors import LLMSingleSelector

class EnsembleRAG:
    """Ensemble of multiple RAG approaches"""

    def __init__(self, indexes, llm=None):
        self.indexes = indexes
        self.llm = llm or OpenAI(model="gpt-4")

        # Create different query engines
        self.query_engines = self._create_query_engines()

    def _create_query_engines(self):
        """Create diverse query engines"""

        engines = []

        # Vector-based engine
        vector_engine = self.indexes["vector"].as_query_engine(
            response_mode="refine",
            similarity_top_k=3
        )
        engines.append(vector_engine)

        # Summary-based engine
        summary_engine = self.indexes["summary"].as_query_engine(
            response_mode="tree_summarize",
            similarity_top_k=5
        )
        engines.append(summary_engine)

        # Keyword-based engine (if available)
        if "keyword" in self.indexes:
            keyword_engine = self.indexes["keyword"].as_query_engine(
                response_mode="simple_summarize",
                similarity_top_k=2
            )
            engines.append(keyword_engine)

        return engines

    def create_ensemble_engine(self):
        """Create ensemble query engine"""

        # Selector chooses which engine to use
        selector = LLMSingleSelector.from_defaults(llm=self.llm)

        ensemble_engine = EnsembleQueryEngine(
            query_engines=self.query_engines,
            selector=selector,
            query_transform=None  # Can add query transformation
        )

        return ensemble_engine

    def query_with_confidence(self, query):
        """Query with confidence scores from multiple engines"""

        responses = []

        # Get responses from all engines
        for i, engine in enumerate(self.query_engines):
            try:
                response = engine.query(query)
                responses.append({
                    "engine_id": i,
                    "response": str(response),
                    "confidence": getattr(response, 'score', 0.5),
                    "source_nodes": len(getattr(response, 'source_nodes', []))
                })
            except Exception as e:
                responses.append({
                    "engine_id": i,
                    "error": str(e),
                    "response": "",
                    "confidence": 0
                })

        # Select best response based on confidence
        best_response = max(responses, key=lambda x: x["confidence"])

        # Combine insights from all responses
        combined_insights = self._combine_insights(responses)

        return {
            "best_response": best_response["response"],
            "confidence": best_response["confidence"],
            "all_responses": responses,
            "combined_insights": combined_insights
        }

    def _combine_insights(self, responses):
        """Combine insights from multiple responses"""

        # Extract key points from each response
        all_points = []
        for response in responses:
            if response["response"]:
                # Simple sentence splitting (could use NLP)
                sentences = response["response"].split('.')
                key_sentences = [s.strip() for s in sentences if len(s.strip()) > 20][:2]
                all_points.extend(key_sentences)

        # Remove duplicates and combine
        unique_points = list(set(all_points))
        combined = '. '.join(unique_points[:5])  # Top 5 unique points

        return combined

# Usage
indexes = {
    "vector": vector_index,
    "summary": summary_index,
    "keyword": keyword_index
}

ensemble_rag = EnsembleRAG(indexes)
ensemble_engine = ensemble_rag.create_ensemble_engine()

# Ensemble query
query = "Explain the differences between various machine learning approaches"
response = ensemble_engine.query(query)
print(f"Ensemble response: {response}")

# Confidence-based query
confident_response = ensemble_rag.query_with_confidence(query)
print(f"Best response (confidence: {confident_response['confidence']:.3f}): {confident_response['best_response']}")
```

### Adaptive RAG

```python
class AdaptiveRAG:
    """RAG system that adapts based on query complexity and user feedback"""

    def __init__(self, indexes):
        self.indexes = indexes
        self.query_history = []
        self.performance_stats = {}

    def adaptive_query(self, query, user_context=None):
        """Adapt query strategy based on context and history"""

        # Analyze query complexity
        complexity = self._analyze_query_complexity(query)

        # Get user preferences from context
        preferences = self._extract_user_preferences(user_context)

        # Choose optimal strategy
        strategy = self._select_optimal_strategy(complexity, preferences)

        # Execute query with chosen strategy
        response = self._execute_strategy(query, strategy)

        # Store for learning
        self._store_query_result(query, strategy, response)

        return {
            "response": response,
            "strategy_used": strategy,
            "complexity_score": complexity
        }

    def _analyze_query_complexity(self, query):
        """Analyze query complexity on multiple dimensions"""

        complexity = {
            "length": len(query.split()),
            "technical_terms": 0,
            "comparative": 0,
            "temporal": 0,
            "causal": 0
        }

        query_lower = query.lower()

        # Technical terms
        technical_terms = ["algorithm", "neural", "optimization", "gradient", "convolution"]
        complexity["technical_terms"] = sum(1 for term in technical_terms if term in query_lower)

        # Comparative queries
        if any(word in query_lower for word in ["compare", "versus", "vs", "difference"]):
            complexity["comparative"] = 1

        # Temporal queries
        if any(word in query_lower for word in ["history", "evolution", "timeline", "before", "after"]):
            complexity["temporal"] = 1

        # Causal queries
        if any(word in query_lower for word in ["why", "because", "cause", "effect", "reason"]):
            complexity["causal"] = 1

        # Overall complexity score
        overall_score = (
            complexity["length"] * 0.2 +
            complexity["technical_terms"] * 0.3 +
            (complexity["comparative"] + complexity["temporal"] + complexity["causal"]) * 0.5
        )

        return min(overall_score, 1.0)  # Normalize to 0-1

    def _extract_user_preferences(self, user_context):
        """Extract user preferences for response style"""

        preferences = {
            "detail_level": "balanced",  # brief, balanced, detailed
            "technical_level": "intermediate",  # beginner, intermediate, advanced
            "response_format": "explanatory"  # factual, explanatory, comparative
        }

        if user_context:
            if user_context.get("expertise") == "beginner":
                preferences.update({
                    "detail_level": "brief",
                    "technical_level": "beginner",
                    "response_format": "explanatory"
                })
            elif user_context.get("expertise") == "expert":
                preferences.update({
                    "detail_level": "detailed",
                    "technical_level": "advanced",
                    "response_format": "factual"
                })

        return preferences

    def _select_optimal_strategy(self, complexity, preferences):
        """Select optimal retrieval/generation strategy"""

        # Strategy selection logic
        if complexity > 0.7:  # High complexity
            if preferences["detail_level"] == "detailed":
                return "multi_index_deep_dive"
            else:
                return "ensemble_reasoning"
        elif complexity > 0.4:  # Medium complexity
            return "hybrid_retrieval"
        else:  # Low complexity
            return "direct_retrieval"

    def _execute_strategy(self, query, strategy):
        """Execute query using selected strategy"""

        if strategy == "direct_retrieval":
            engine = self.indexes["vector"].as_query_engine(similarity_top_k=3)
            return engine.query(query)

        elif strategy == "hybrid_retrieval":
            # Use hybrid retriever
            hybrid_retriever = HybridRetriever(self.indexes["vector"])
            engine = RetrieverQueryEngine.from_args(hybrid_retriever)
            return engine.query(query)

        elif strategy == "ensemble_reasoning":
            # Use ensemble approach
            ensemble = EnsembleRAG(self.indexes)
            result = ensemble.query_with_confidence(query)
            return result["best_response"]

        elif strategy == "multi_index_deep_dive":
            # Use multi-index agent
            agent = create_research_agent(self.indexes)
            return agent.chat(query)

        else:
            # Default fallback
            engine = self.indexes["vector"].as_query_engine()
            return engine.query(query)

    def _store_query_result(self, query, strategy, response):
        """Store query result for future learning"""

        result = {
            "query": query,
            "strategy": strategy,
            "response_length": len(str(response)),
            "timestamp": time.time(),
            "success": True  # Could add error detection
        }

        self.query_history.append(result)

        # Update performance stats
        if strategy not in self.performance_stats:
            self.performance_stats[strategy] = []

        self.performance_stats[strategy].append({
            "response_length": result["response_length"],
            "timestamp": result["timestamp"]
        })

    def get_strategy_performance(self):
        """Get performance statistics for different strategies"""

        stats = {}
        for strategy, results in self.performance_stats.items():
            if results:
                avg_length = sum(r["response_length"] for r in results) / len(results)
                usage_count = len(results)

                stats[strategy] = {
                    "average_response_length": avg_length,
                    "usage_count": usage_count,
                    "total_queries": len(self.query_history)
                }

        return stats

# Usage
adaptive_rag = AdaptiveRAG(indexes)

# Test adaptive querying
test_queries = [
    "What is AI?",  # Simple query
    "Compare different machine learning algorithms",  # Complex comparative
    "Why do neural networks use backpropagation?"  # Complex causal
]

for query in test_queries:
    result = adaptive_rag.adaptive_query(query)
    print(f"Query: {query}")
    print(f"Strategy: {result['strategy_used']}")
    print(f"Complexity: {result['complexity_score']:.2f}")
    print("---")

# Check strategy performance
performance = adaptive_rag.get_strategy_performance()
print("Strategy Performance:", performance)
```

## 🎯 Best Practices

### Multi-Modal RAG

1. **Choose appropriate models** for different modalities (CLIP for images, Whisper for audio)
2. **Implement proper preprocessing** for each data type
3. **Use modality-specific embeddings** and similarity measures
4. **Combine modalities effectively** in response generation
5. **Handle missing modalities** gracefully

### Agent-Based Systems

1. **Design clear tool boundaries** to avoid conflicts
2. **Implement proper error handling** in agent workflows
3. **Use appropriate prompting** for different agent types
4. **Monitor agent performance** and adjust parameters
5. **Implement safety measures** for agent actions

### Knowledge Graphs

1. **Design meaningful relationships** between entities
2. **Implement proper entity extraction** and linking
3. **Use graph queries effectively** for complex relationships
4. **Maintain graph consistency** and update mechanisms
5. **Balance graph and vector approaches** based on use case

## 📈 Next Steps

With advanced RAG patterns mastered, you're ready to:

- **[Chapter 6: Custom Components](06-custom-components.md)** - Building custom loaders, indexes, and query engines
- **[Chapter 7: Production Deployment](07-production-deployment.md)** - Scaling LlamaIndex applications for production
- **[Chapter 8: Monitoring & Optimization](08-monitoring-optimization.md)** - Performance tuning and observability

---

**Ready to build custom LlamaIndex components? Continue to [Chapter 6: Custom Components](06-custom-components.md)!** 🚀