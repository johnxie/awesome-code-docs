---
layout: default
title: "Chapter 5: Pipelines & Workflows"
parent: "Haystack Tutorial"
nav_order: 5
---

# Chapter 5: Pipelines & Workflows

> Build complex, production-ready search workflows with Haystack pipelines.

## 🎯 Overview

This chapter covers building sophisticated search workflows using Haystack's pipeline system. You'll learn to create multi-stage pipelines, handle conditional logic, implement error handling, and build scalable search applications.

## 🔧 Pipeline Fundamentals

### Basic Pipeline Construction

```python
from haystack import Pipeline
from haystack.components.retrievers import BM25Retriever, EmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.components.joiners import DocumentJoiner

# Create a comprehensive search pipeline
def create_search_pipeline(document_store):
    """Create a complete search pipeline with multiple retrieval strategies"""

    pipeline = Pipeline()

    # Component 1: BM25 Retriever for keyword search
    bm25_retriever = BM25Retriever(document_store=document_store)
    pipeline.add_component("bm25_retriever", bm25_retriever)

    # Component 2: Embedding Retriever for semantic search
    embedding_retriever = EmbeddingRetriever(document_store=document_store)
    pipeline.add_component("embedding_retriever", embedding_retriever)

    # Component 3: Join results from both retrievers
    joiner = DocumentJoiner(join_mode="reciprocal_rank_fusion", top_k=10)
    pipeline.add_component("joiner", joiner)

    # Component 4: Build prompt with retrieved documents
    prompt_builder = PromptBuilder(
        template="""
        Answer the question based on the provided context.

        Context:
        {% for document in documents %}
        {{ document.content }}
        {% endfor %}

        Question: {{ query }}
        Answer:"""
    )
    pipeline.add_component("prompt_builder", prompt_builder)

    # Component 5: Generate answer with LLM
    generator = OpenAIGenerator(model="gpt-4o")
    pipeline.add_component("generator", generator)

    # Connect components
    pipeline.connect("bm25_retriever", "joiner")
    pipeline.connect("embedding_retriever", "joiner")
    pipeline.connect("joiner", "prompt_builder.documents")
    pipeline.connect("prompt_builder", "generator")

    return pipeline

# Usage
search_pipeline = create_search_pipeline(document_store)

# Run the pipeline
result = search_pipeline.run({
    "bm25_retriever": {"query": "machine learning algorithms"},
    "embedding_retriever": {"query": "machine learning algorithms"},
    "prompt_builder": {"query": "machine learning algorithms"}
})

print("Pipeline Result:")
print(result["generator"]["replies"][0])
```

## 🔀 Conditional Logic and Branching

### Conditional Pipelines

```python
from haystack.components.routers import ConditionalRouter
from haystack.components.builders import PromptBuilder

class ConditionalSearchPipeline:
    def __init__(self, document_store):
        self.pipeline = Pipeline()
        self.document_store = document_store
        self._build_conditional_pipeline()

    def _build_conditional_pipeline(self):
        """Build pipeline with conditional routing"""

        # Query classifier to determine search strategy
        query_classifier = self._create_query_classifier()
        self.pipeline.add_component("query_classifier", query_classifier)

        # Different retrievers for different query types
        bm25_retriever = BM25Retriever(document_store=self.document_store)
        self.pipeline.add_component("bm25_retriever", bm25_retriever)

        embedding_retriever = EmbeddingRetriever(document_store=self.document_store)
        self.pipeline.add_component("embedding_retriever", embedding_retriever)

        # Router to choose retrieval strategy
        router = ConditionalRouter([
            {
                "condition": "{{query_type == 'factual'}}",
                "output": "{{bm25_retriever}}",
                "output_name": "factual_docs",
            },
            {
                "condition": "{{query_type == 'semantic'}}",
                "output": "{{embedding_retriever}}",
                "output_name": "semantic_docs",
            }
        ])
        self.pipeline.add_component("router", router)

        # Generator for final answer
        generator = OpenAIGenerator(model="gpt-4o")
        self.pipeline.add_component("generator", generator)

        # Connect components
        self.pipeline.connect("query_classifier.query_type", "router.query_type")
        self.pipeline.connect("bm25_retriever", "router.bm25_retriever")
        self.pipeline.connect("embedding_retriever", "router.embedding_retriever")
        self.pipeline.connect("router.factual_docs", "generator")
        self.pipeline.connect("router.semantic_docs", "generator")

    def _create_query_classifier(self):
        """Create a simple query classifier component"""
        from haystack import component

        @component
        class QueryClassifier:
            @component.output_types(query_type=str)
            def run(self, query: str):
                # Simple rule-based classification
                query_lower = query.lower()

                if any(word in query_lower for word in ["what is", "how does", "explain"]):
                    query_type = "factual"
                elif any(word in query_lower for word in ["meaning", "concept", "understand"]):
                    query_type = "semantic"
                else:
                    query_type = "semantic"  # Default

                return {"query_type": query_type}

        return QueryClassifier()

    def search(self, query):
        """Run conditional search"""
        result = self.pipeline.run({
            "query_classifier": {"query": query},
            "bm25_retriever": {"query": query},
            "embedding_retriever": {"query": query}
        })

        return result

# Usage
conditional_pipeline = ConditionalSearchPipeline(document_store)

# Test different query types
queries = [
    "What is machine learning?",      # factual
    "Explain neural networks",       # factual
    "The meaning of life",           # semantic
    "Understanding consciousness"    # semantic
]

for query in queries:
    result = conditional_pipeline.search(query)
    print(f"Query: {query}")
    print(f"Generated answer available: {'generator' in result}")
    print("---")
```

### Multi-Stage Processing

```python
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.rankers import SentenceTransformersDiversityRanker

class MultiStagePipeline:
    def __init__(self, document_store):
        self.pipeline = Pipeline()
        self._build_multi_stage_pipeline()

    def _build_multi_stage_pipeline(self):
        """Build multi-stage processing pipeline"""

        # Stage 1: Multi-strategy retrieval
        bm25_retriever = BM25Retriever(document_store=document_store)
        self.pipeline.add_component("bm25_retriever", bm25_retriever)

        embedding_retriever = EmbeddingRetriever(document_store=document_store)
        self.pipeline.add_component("embedding_retriever", embedding_retriever)

        # Stage 2: Result fusion and ranking
        joiner = DocumentJoiner(join_mode="reciprocal_rank_fusion", top_k=20)
        self.pipeline.add_component("joiner", joiner)

        ranker = SentenceTransformersDiversityRanker(
            model="sentence-transformers/all-MiniLM-L6-v2",
            top_k=10
        )
        self.pipeline.add_component("ranker", ranker)

        # Stage 3: Document processing
        splitter = DocumentSplitter(split_by="sentence", split_length=3)
        self.pipeline.add_component("splitter", splitter)

        # Stage 4: Answer generation
        prompt_builder = PromptBuilder(
            template=self._get_multi_stage_template()
        )
        self.pipeline.add_component("prompt_builder", prompt_builder)

        generator = OpenAIGenerator(
            model="gpt-4o",
            generation_kwargs={"temperature": 0.1}
        )
        self.pipeline.add_component("generator", generator)

        # Connect stages
        self.pipeline.connect("bm25_retriever", "joiner")
        self.pipeline.connect("embedding_retriever", "joiner")
        self.pipeline.connect("joiner", "ranker")
        self.pipeline.connect("ranker", "splitter")
        self.pipeline.connect("splitter", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "generator")

    def _get_multi_stage_template(self):
        """Get template for multi-stage processing"""
        return """
        You are an expert at analyzing and synthesizing information from multiple sources.

        INSTRUCTIONS:
        1. Analyze the provided document chunks for relevant information
        2. Synthesize a comprehensive answer from all relevant chunks
        3. Cite specific information from the chunks when possible
        4. If information is contradictory, note the differences
        5. Provide a clear, well-structured answer

        DOCUMENT CHUNKS:
        {% for document in documents %}
        Chunk {{ loop.index }}: {{ document.content }}
        {% endfor %}

        QUESTION: {{ query }}

        ANALYSIS AND ANSWER:
        """

    def run_multi_stage_search(self, query):
        """Run the complete multi-stage pipeline"""
        result = self.pipeline.run({
            "bm25_retriever": {"query": query},
            "embedding_retriever": {"query": query},
            "prompt_builder": {"query": query}
        })

        return {
            "query": query,
            "answer": result["generator"]["replies"][0],
            "retrieved_docs": result["ranker"]["documents"],
            "processing_stages": [
                "Multi-strategy retrieval",
                "Result fusion and ranking",
                "Document chunking",
                "Answer generation"
            ]
        }

# Usage
multi_stage_pipeline = MultiStagePipeline(document_store)

result = multi_stage_pipeline.run_multi_stage_search("How do neural networks work?")

print("Multi-Stage Pipeline Result:")
print(f"Query: {result['query']}")
print(f"Answer: {result['answer']}")
print(f"Retrieved {len(result['retrieved_docs'])} documents")
print(f"Processing stages: {len(result['processing_stages'])}")
```

## 🔄 Error Handling and Resilience

### Robust Pipeline Design

```python
from haystack.components.routers import ConditionalRouter
import logging

class RobustPipeline:
    def __init__(self, document_store):
        self.pipeline = Pipeline()
        self.logger = logging.getLogger(__name__)
        self._build_robust_pipeline(document_store)

    def _build_robust_pipeline(self, document_store):
        """Build pipeline with error handling and fallbacks"""

        # Primary retriever
        primary_retriever = EmbeddingRetriever(document_store=document_store)
        self.pipeline.add_component("primary_retriever", primary_retriever)

        # Fallback retriever (BM25)
        fallback_retriever = BM25Retriever(document_store=document_store)
        self.pipeline.add_component("fallback_retriever", fallback_retriever)

        # Error detector and router
        error_router = ConditionalRouter([
            {
                "condition": "{{len(primary_results.documents) > 0}}",
                "output": "{{primary_results}}",
                "output_name": "success_path",
            },
            {
                "condition": "{{len(primary_results.documents) == 0}}",
                "output": "{{fallback_results}}",
                "output_name": "fallback_path",
            }
        ])
        self.pipeline.add_component("error_router", error_router)

        # Generator with retry logic
        generator = OpenAIGenerator(
            model="gpt-4o",
            generation_kwargs={
                "temperature": 0.1,
                "max_tokens": 300
            }
        )
        self.pipeline.add_component("generator", generator)

        # Error handler component
        error_handler = self._create_error_handler()
        self.pipeline.add_component("error_handler", error_handler)

        # Connect with error handling
        self.pipeline.connect("primary_retriever", "error_router.primary_results")
        self.pipeline.connect("fallback_retriever", "error_router.fallback_results")
        self.pipeline.connect("error_router.success_path", "generator")
        self.pipeline.connect("error_router.fallback_path", "generator")
        self.pipeline.connect("generator", "error_handler")

    def _create_error_handler(self):
        """Create error handling component"""
        from haystack import component

        @component
        class ErrorHandler:
            @component.output_types(final_result=dict)
            def run(self, replies: list, query: str):
                try:
                    if not replies or len(replies) == 0:
                        return {
                            "success": False,
                            "error": "No response generated",
                            "fallback_message": "I apologize, but I couldn't generate a response for your query."
                        }

                    response = replies[0]

                    # Validate response quality
                    if self._is_response_valid(response):
                        return {
                            "success": True,
                            "response": response,
                            "quality_score": self._calculate_quality_score(response)
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Response quality too low",
                            "fallback_message": "The generated response didn't meet quality standards. Please try rephrasing your question."
                        }

                except Exception as e:
                    self.logger.error(f"Error in response processing: {e}")
                    return {
                        "success": False,
                        "error": str(e),
                        "fallback_message": "An error occurred while processing your request. Please try again."
                    }

            def _is_response_valid(self, response):
                """Check if response meets basic quality criteria"""
                if len(response.strip()) < 10:
                    return False

                # Check for too many repetitions
                words = response.lower().split()
                if len(words) > 20 and len(set(words)) / len(words) < 0.5:
                    return False

                return True

            def _calculate_quality_score(self, response):
                """Calculate response quality score"""
                score = 0

                # Length appropriateness
                if 50 < len(response) < 1000:
                    score += 1

                # Contains structured information
                if any(word in response.lower() for word in ["because", "however", "therefore", "example"]):
                    score += 1

                # Not generic
                generic_phrases = ["i don't know", "i'm not sure", "i cannot"]
                if not any(phrase in response.lower() for phrase in generic_phrases):
                    score += 1

                return min(score / 3, 1.0)  # Normalize to 0-1

        return ErrorHandler()

    def search_with_resilience(self, query):
        """Run search with comprehensive error handling"""
        try:
            result = self.pipeline.run({
                "primary_retriever": {"query": query},
                "fallback_retriever": {"query": query},
                "error_handler": {"query": query}
            })

            final_result = result["error_handler"]["final_result"]

            return {
                "query": query,
                "success": final_result["success"],
                "response": final_result.get("response", final_result.get("fallback_message", "")),
                "quality_score": final_result.get("quality_score", 0),
                "error": final_result.get("error")
            }

        except Exception as e:
            self.logger.error(f"Pipeline execution error: {e}")
            return {
                "query": query,
                "success": False,
                "response": "A system error occurred. Please try again later.",
                "error": str(e)
            }

# Usage
robust_pipeline = RobustPipeline(document_store)

# Test with various scenarios
test_queries = [
    "What is machine learning?",  # Normal case
    "xyz123nonexistent",         # No results case
]

for query in test_queries:
    result = robust_pipeline.search_with_resilience(query)
    print(f"Query: {query}")
    print(f"Success: {result['success']}")
    print(f"Response: {result['response'][:100]}...")
    print("---")
```

## 🔄 Asynchronous and Streaming Pipelines

### Async Pipeline Execution

```python
import asyncio
from haystack import AsyncPipeline

class AsyncSearchPipeline:
    def __init__(self, document_store):
        self.pipeline = AsyncPipeline()  # Use async pipeline
        self._build_async_pipeline(document_store)

    def _build_async_pipeline(self, document_store):
        """Build asynchronous pipeline"""

        # Async retriever
        retriever = EmbeddingRetriever(document_store=document_store)
        self.pipeline.add_component("retriever", retriever)

        # Async generator with streaming
        generator = OpenAIGenerator(
            model="gpt-4o",
            generation_kwargs={
                "temperature": 0.7,
                "stream": True  # Enable streaming
            }
        )
        self.pipeline.add_component("generator", generator)

        # Connect components
        self.pipeline.connect("retriever", "generator")

    async def search_async(self, query):
        """Run async search with streaming response"""
        print(f"Starting async search for: {query}")

        # Run pipeline asynchronously
        result = await self.pipeline.run_async({
            "retriever": {"query": query}
        })

        return result

    async def stream_search(self, query):
        """Stream search results as they become available"""
        print(f"Streaming search for: {query}")

        # For streaming, we need to handle the generator's streaming output
        # This is a simplified example - actual streaming implementation
        # would depend on the specific generator's streaming capabilities

        result = await self.pipeline.run_async({
            "retriever": {"query": query}
        })

        # Simulate streaming by yielding partial results
        response = result["generator"]["replies"][0]

        # Split response into chunks for streaming effect
        words = response.split()
        for i in range(0, len(words), 3):
            chunk = " ".join(words[i:i+3])
            yield chunk
            await asyncio.sleep(0.1)  # Simulate streaming delay

# Usage
async def run_async_search():
    async_pipeline = AsyncSearchPipeline(document_store)

    # Run async search
    result = await async_pipeline.search_async("What is AI?")
    print("Async search result:")
    print(result["generator"]["replies"][0])

    # Stream results
    print("\nStreaming results:")
    async for chunk in async_pipeline.stream_search("Explain neural networks"):
        print(chunk, end=" ", flush=True)
    print("\n")

# Run async example
asyncio.run(run_async_search())
```

### Pipeline Orchestration

```python
from haystack.components.routers import ConditionalRouter
from haystack.components.joiners import DocumentJoiner

class OrchestratedPipeline:
    def __init__(self):
        self.pipelines = {}
        self.orchestrator = Pipeline()
        self._build_orchestrator()

    def _build_orchestrator(self):
        """Build pipeline orchestrator"""

        # Query analyzer
        query_analyzer = self._create_query_analyzer()
        self.orchestrator.add_component("query_analyzer", query_analyzer)

        # Pipeline router
        pipeline_router = ConditionalRouter([
            {
                "condition": "{{query_type == 'technical'}}",
                "output": "tech_pipeline",
                "output_name": "tech_route",
            },
            {
                "condition": "{{query_type == 'general'}}",
                "output": "general_pipeline",
                "output_name": "general_route",
            },
            {
                "condition": "{{query_type == 'creative'}}",
                "output": "creative_pipeline",
                "output_name": "creative_route",
            }
        ])
        self.orchestrator.add_component("pipeline_router", pipeline_router)

        # Result aggregator
        aggregator = self._create_result_aggregator()
        self.orchestrator.add_component("aggregator", aggregator)

        # Connect orchestrator components
        self.orchestrator.connect("query_analyzer.query_type", "pipeline_router.query_type")
        self.orchestrator.connect("pipeline_router.tech_route", "aggregator")
        self.orchestrator.connect("pipeline_router.general_route", "aggregator")
        self.orchestrator.connect("pipeline_router.creative_route", "aggregator")

    def _create_query_analyzer(self):
        """Create query type analyzer"""
        from haystack import component

        @component
        class QueryAnalyzer:
            @component.output_types(query_type=str)
            def run(self, query: str):
                # Analyze query type
                query_lower = query.lower()

                if any(word in query_lower for word in ["code", "api", "function", "class", "algorithm"]):
                    return {"query_type": "technical"}
                elif any(word in query_lower for word in ["write", "create", "design", "imagine"]):
                    return {"query_type": "creative"}
                else:
                    return {"query_type": "general"}

        return QueryAnalyzer()

    def _create_result_aggregator(self):
        """Create result aggregation component"""
        from haystack import component

        @component
        class ResultAggregator:
            @component.output_types(final_result=dict)
            def run(self, tech_route=None, general_route=None, creative_route=None):
                # Aggregate results from different pipelines
                results = []

                if tech_route:
                    results.append({"type": "technical", "result": tech_route})
                if general_route:
                    results.append({"type": "general", "result": general_route})
                if creative_route:
                    results.append({"type": "creative", "result": creative_route})

                # Combine results (simplified)
                if results:
                    # Return the most appropriate result
                    best_result = results[0]["result"]  # In practice, you'd rank them
                    return {"final_result": best_result}
                else:
                    return {"final_result": {"error": "No pipeline executed"}}

        return ResultAggregator()

    def add_specialized_pipeline(self, name, pipeline):
        """Add a specialized pipeline"""
        self.pipelines[name] = pipeline

    def orchestrate_search(self, query):
        """Run orchestrated search across multiple pipelines"""
        # First, analyze query
        analysis_result = self.orchestrator.run({
            "query_analyzer": {"query": query}
        })

        query_type = analysis_result["pipeline_router"]["query_type"]

        # Run appropriate specialized pipeline
        if query_type in self.pipelines:
            pipeline_result = self.pipelines[query_type].run({
                "retriever": {"query": query},
                "prompt_builder": {"query": query}
            })

            return {
                "query": query,
                "query_type": query_type,
                "result": pipeline_result["generator"]["replies"][0]
            }
        else:
            return {
                "query": query,
                "error": f"No pipeline available for query type: {query_type}"
            }

# Usage
orchestrator = OrchestratedPipeline()

# Add specialized pipelines (simplified examples)
tech_pipeline = create_search_pipeline(document_store)  # Reuse earlier function
orchestrator.add_specialized_pipeline("technical", tech_pipeline)

# Run orchestrated search
result = orchestrator.orchestrate_search("How do I implement a REST API?")
print(f"Query type: {result['query_type']}")
print(f"Result: {result['result'][:200]}...")
```

## 📊 Pipeline Monitoring and Optimization

### Performance Monitoring

```python
import time
import psutil
from functools import wraps

class PipelineMonitor:
    def __init__(self):
        self.metrics = {
            "execution_times": [],
            "memory_usage": [],
            "component_times": {},
            "error_counts": {}
        }

    def monitor_pipeline(self, pipeline_func):
        """Decorator to monitor pipeline execution"""
        @wraps(pipeline_func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

            try:
                result = pipeline_func(*args, **kwargs)
                success = True
            except Exception as e:
                self.metrics["error_counts"][pipeline_func.__name__] = \
                    self.metrics["error_counts"].get(pipeline_func.__name__, 0) + 1
                raise e
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024

                execution_time = end_time - start_time
                memory_used = end_memory - start_memory

                self.metrics["execution_times"].append(execution_time)
                self.metrics["memory_usage"].append(memory_used)

            return result

        return wrapper

    def monitor_component(self, component_name):
        """Decorator to monitor individual components"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    component_time = end_time - start_time

                    if component_name not in self.metrics["component_times"]:
                        self.metrics["component_times"][component_name] = []

                    self.metrics["component_times"][component_name].append(component_time)

            return wrapper
        return decorator

    def get_performance_report(self):
        """Generate performance report"""
        report = {
            "overall_performance": {
                "avg_execution_time": sum(self.metrics["execution_times"]) / len(self.metrics["execution_times"]) if self.metrics["execution_times"] else 0,
                "max_execution_time": max(self.metrics["execution_times"]) if self.metrics["execution_times"] else 0,
                "avg_memory_usage": sum(self.metrics["memory_usage"]) / len(self.metrics["memory_usage"]) if self.metrics["memory_usage"] else 0,
                "total_executions": len(self.metrics["execution_times"])
            },
            "component_performance": {},
            "error_analysis": self.metrics["error_counts"]
        }

        # Component performance
        for component, times in self.metrics["component_times"].items():
            report["component_performance"][component] = {
                "avg_time": sum(times) / len(times),
                "max_time": max(times),
                "call_count": len(times)
            }

        return report

# Usage
monitor = PipelineMonitor()

@monitor.monitor_pipeline
def run_search_pipeline(query):
    """Monitored search pipeline"""
    result = search_pipeline.run({
        "bm25_retriever": {"query": query},
        "embedding_retriever": {"query": query},
        "prompt_builder": {"query": query}
    })
    return result

# Run monitored searches
for query in ["What is AI?", "How do neural networks work?", "Explain machine learning"]:
    result = run_search_pipeline(query)
    print(f"Processed: {query}")

# Get performance report
report = monitor.get_performance_report()
print("\nPerformance Report:")
print(f"Average execution time: {report['overall_performance']['avg_execution_time']:.3f}s")
print(f"Average memory usage: {report['overall_performance']['avg_memory_usage']:.1f}MB")
```

## 🎯 Best Practices

### Pipeline Design
1. **Modular components** - Break complex workflows into reusable components
2. **Clear data flow** - Ensure predictable data flow between components
3. **Error boundaries** - Implement proper error handling at each stage
4. **Configuration management** - Externalize pipeline configuration
5. **Version control** - Track pipeline versions and changes

### Performance Optimization
1. **Async execution** - Use async components for I/O operations
2. **Caching strategies** - Cache expensive operations and frequent queries
3. **Batch processing** - Process multiple requests together when possible
4. **Resource management** - Monitor and limit resource usage
5. **Load balancing** - Distribute load across multiple pipeline instances

### Monitoring and Maintenance
1. **Comprehensive logging** - Log all pipeline activities and errors
2. **Performance metrics** - Track execution times, memory usage, success rates
3. **Health checks** - Implement pipeline health monitoring
4. **Automated testing** - Test pipelines with various inputs and scenarios
5. **Regular maintenance** - Update components and fix issues proactively

## 📈 Next Steps

With advanced pipelines mastered, you're ready to:

- **[Chapter 6: Evaluation & Optimization](06-evaluation-optimization.md)** - Measure and improve search quality
- **[Chapter 7: Custom Components](07-custom-components.md)** - Extend Haystack with custom functionality
- **[Chapter 8: Production Deployment](08-production-deployment.md)** - Deploy pipelines at scale

---

**Ready to evaluate and optimize your search systems? Continue to [Chapter 6: Evaluation & Optimization](06-evaluation-optimization.md)!** 🚀