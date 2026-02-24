---
layout: default
title: "Outlines Tutorial - Chapter 7: Framework Integration"
nav_order: 7
has_children: false
parent: Outlines Tutorial
---

# Chapter 7: Integration with AI Frameworks

Welcome to **Chapter 7: Integration with AI Frameworks**. In this part of **Outlines Tutorial: Structured Text Generation with LLMs**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Seamlessly integrate Outlines constrained generation with LangChain, CrewAI, LlamaIndex, and other popular AI frameworks for production-ready applications.

## LangChain Integration

### Custom LLM Class with Constraints

```python
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
from outlines import models, generate

class OutlinesConstrainedLLM(LLM):
    """LangChain LLM wrapper with Outlines constraints."""

    model: Any = None
    constraint_type: str = "text"
    constraint_config: Any = None

    def __init__(self, model_name: str, constraint_type: str = "text", constraint_config: Any = None):
        super().__init__()

        # Load Outlines model
        self.model = models.transformers(model_name)
        self.constraint_type = constraint_type
        self.constraint_config = constraint_config

        # Create constrained generator
        if constraint_type == "text":
            self.generator = generate.text(self.model, **(constraint_config or {}))
        elif constraint_type == "choice":
            self.generator = generate.choice(self.model, constraint_config)
        elif constraint_type == "json":
            self.generator = generate.json(self.model, constraint_config)
        elif constraint_type == "pydantic":
            self.generator = generate.pydantic(self.model, constraint_config)
        else:
            raise ValueError(f"Unsupported constraint type: {constraint_type}")

    @property
    def _llm_type(self) -> str:
        return "outlines_constrained"

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
        """Generate constrained output."""

        # Apply stop words if provided
        if stop:
            # This is a simplified implementation
            # In practice, you'd modify the generator to respect stop tokens
            pass

        try:
            result = self.generator(prompt)
            return str(result)
        except Exception as e:
            return f"Generation error: {e}"

# Usage with LangChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Create constrained LLM
constrained_llm = OutlinesConstrainedLLM(
    model_name="microsoft/DialoGPT-small",
    constraint_type="choice",
    constraint_config=["positive", "negative", "neutral"]
)

# Create LangChain prompt
sentiment_prompt = PromptTemplate(
    input_variables=["text"],
    template="Analyze the sentiment of this text: {text}"
)

# Create chain
sentiment_chain = LLMChain(llm=constrained_llm, prompt=sentiment_prompt)

# Run chain
result = sentiment_chain.run(text="I love this product!")
print(f"Sentiment analysis: {result}")
```

### Structured Output Chains

```python
from langchain.chains import TransformChain, SequentialChain
from pydantic import BaseModel, Field
from typing import List

# Define structured output models
class ProductReview(BaseModel):
    product_name: str
    rating: int = Field(ge=1, le=5)
    sentiment: str
    pros: List[str]
    cons: List[str]

class ReviewAnalysis(BaseModel):
    overall_sentiment: str
    average_rating: float
    key_themes: List[str]
    recommendations: List[str]

# Create structured LLM
review_llm = OutlinesConstrainedLLM(
    model_name="microsoft/DialoGPT-small",
    constraint_type="pydantic",
    constraint_config=ProductReview
)

analysis_llm = OutlinesConstrainedLLM(
    model_name="microsoft/DialoGPT-small",
    constraint_type="pydantic",
    constraint_config=ReviewAnalysis
)

# Transform chain to extract reviews
def extract_reviews(inputs: dict) -> dict:
    """Extract individual reviews from text."""
    reviews_text = inputs["reviews"]
    # In practice, you'd split reviews here
    return {"individual_reviews": reviews_text.split("\n\n")}

extract_chain = TransformChain(
    input_variables=["reviews"],
    output_variables=["individual_reviews"],
    transform=extract_reviews
)

# Analysis chain
analysis_prompt = PromptTemplate(
    input_variables=["reviews"],
    template="Analyze these product reviews and provide insights: {reviews}"
)

analysis_chain = LLMChain(llm=analysis_llm, prompt=analysis_prompt)

# Combine into sequential chain
review_analysis_chain = SequentialChain(
    chains=[extract_chain, analysis_chain],
    input_variables=["reviews"],
    output_variables=["individual_reviews", "analysis"]
)

# Run analysis
reviews = """
Great product! Fast shipping and excellent quality. Rating: 5/5
Not bad, but delivery was slow. Rating: 3/5
Terrible experience. Product broke after one day. Rating: 1/5
"""

result = review_analysis_chain({"reviews": reviews})
print("Analysis result:")
print(result["analysis"])
```

## CrewAI Integration

### Constrained AI Agents

```python
from crewai import Agent, Task, Crew
from outlines import models, generate
from pydantic import BaseModel, Field

# Define structured output for agents
class TaskResult(BaseModel):
    task_name: str
    status: str = Field(enum=["completed", "failed", "in_progress"])
    result: str
    confidence: float = Field(ge=0.0, le=1.0)
    next_steps: List[str] = Field(default_factory=list)

class OutlinesAgent(Agent):
    """CrewAI agent with Outlines constraints."""

    def __init__(self, role: str, goal: str, backstory: str, model_name: str, **kwargs):
        super().__init__(role=role, goal=goal, backstory=backstory, **kwargs)

        # Add Outlines model
        self.outlines_model = models.transformers(model_name)
        self.structured_generator = generate.pydantic(self.outlines_model, TaskResult)

    def perform_task(self, task: Task) -> TaskResult:
        """Perform task with structured output."""

        # Create prompt for the task
        prompt = f"""
        Role: {self.role}
        Goal: {self.goal}
        Backstory: {self.backstory}

        Task: {task.description}
        Context: {task.context if hasattr(task, 'context') else ''}

        Provide a structured response about completing this task.
        """

        # Generate structured result
        result = self.structured_generator(prompt)

        return result

# Create agents
researcher = OutlinesAgent(
    role="Research Analyst",
    goal="Analyze market trends and provide insights",
    backstory="You are an experienced market research analyst with 10 years of experience.",
    model_name="microsoft/DialoGPT-small"
)

writer = OutlinesAgent(
    role="Content Writer",
    goal="Create engaging content based on research",
    backstory="You are a skilled content writer who creates compelling articles.",
    model_name="microsoft/DialoGPT-small"
)

# Create tasks
research_task = Task(
    description="Research the latest trends in AI for 2024",
    agent=researcher
)

writing_task = Task(
    description="Write a blog post about AI trends based on the research",
    agent=writer,
    context="Use the research findings to create an engaging article"
)

# Create crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

# Execute crew
result = crew.kickoff()
print("Crew execution result:")
print(result)
```

### Multi-Agent Collaboration with Constraints

```python
from crewai import Agent, Task, Crew, Process
from typing import Dict, List
import json

# Define collaboration schema
class AgentMessage(BaseModel):
    sender: str
    receiver: str
    message_type: str = Field(enum=["request", "response", "update", "question"])
    content: str
    priority: str = Field(enum=["low", "medium", "high"])
    requires_response: bool = True

class CollaborationResult(BaseModel):
    participants: List[str]
    messages: List[AgentMessage]
    final_outcome: str
    consensus_reached: bool
    action_items: List[str]

class CollaborativeAgent(OutlinesAgent):
    """Agent that can collaborate with structured communication."""

    def __init__(self, *args, collaborators: List[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.collaborators = collaborators or []
        self.message_generator = generate.pydantic(self.outlines_model, AgentMessage)

    def send_message(self, receiver: str, message_type: str, content: str, priority: str = "medium") -> AgentMessage:
        """Send structured message to another agent."""

        prompt = f"""
        Create a professional message to {receiver} about: {content}

        Message type: {message_type}
        Priority: {priority}
        """

        message = self.message_generator(prompt)
        message.sender = self.role
        message.receiver = receiver

        return message

    def collaborate_on_task(self, task: Task, collaborators: List['CollaborativeAgent']) -> CollaborationResult:
        """Collaborate with other agents on a task."""

        messages = []
        participants = [self.role] + [agent.role for agent in collaborators]

        # Initial task analysis
        initial_analysis = self.perform_task(task)
        messages.append(AgentMessage(
            sender=self.role,
            receiver="all",
            message_type="update",
            content=f"Initial analysis: {initial_analysis.result}",
            priority="high"
        ))

        # Simulate collaboration rounds
        for round_num in range(3):
            for collaborator in collaborators:
                # Each collaborator responds
                response_prompt = f"""
                Task: {task.description}
                Previous messages: {json.dumps([msg.model_dump() for msg in messages[-3:]])}

                Provide your perspective or ask questions about this task.
                """

                response = collaborator.message_generator(response_prompt)
                response.sender = collaborator.role
                response.receiver = self.role
                messages.append(response)

        # Final synthesis
        synthesis_prompt = f"""
        Synthesize all the collaboration messages and provide a final outcome.

        Task: {task.description}
        Messages: {json.dumps([msg.model_dump() for msg in messages])}

        Provide a comprehensive result with action items.
        """

        final_result = self.structured_generator(synthesis_prompt)

        return CollaborationResult(
            participants=participants,
            messages=messages,
            final_outcome=final_result.result,
            consensus_reached=True,  # Simplified
            action_items=["Implement findings", "Schedule follow-up", "Document process"]
        )

# Create collaborative agents
product_manager = CollaborativeAgent(
    role="Product Manager",
    goal="Define product requirements and prioritize features",
    backstory="You are a seasoned product manager who excels at understanding user needs.",
    model_name="microsoft/DialoGPT-small",
    collaborators=["developer", "designer"]
)

developer = CollaborativeAgent(
    role="Senior Developer",
    goal="Provide technical implementation insights",
    backstory="You are an experienced developer who focuses on scalable solutions.",
    model_name="microsoft/DialoGPT-small",
    collaborators=["product_manager", "designer"]
)

designer = CollaborativeAgent(
    role="UX Designer",
    goal="Ensure excellent user experience",
    backstory="You are a creative designer who prioritizes user needs.",
    model_name="microsoft/DialoGPT-small",
    collaborators=["product_manager", "developer"]
)

# Collaborative task
feature_task = Task(
    description="Design and implement a new user onboarding flow for our SaaS platform"
)

# Execute collaboration
collaboration_result = product_manager.collaborate_on_task(feature_task, [developer, designer])

print("Collaboration result:")
print(f"Participants: {collaboration_result.participants}")
print(f"Messages exchanged: {len(collaboration_result.messages)}")
print(f"Final outcome: {collaboration_result.final_outcome}")
```

## LlamaIndex Integration

### Structured Document Indexing

```python
from llama_index import VectorStoreIndex, Document
from llama_index.llms import CustomLLM
from outlines import models, generate
from pydantic import BaseModel, Field
from typing import List

class StructuredAnswer(BaseModel):
    question: str
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)
    related_questions: List[str] = Field(default_factory=list)

class OutlinesLLM(CustomLLM):
    """LlamaIndex LLM with Outlines constraints."""

    model_name: str = "microsoft/DialoGPT-small"
    constraint_type: str = "text"
    constraint_config: Any = None

    def __init__(self, model_name: str, constraint_type: str = "text", constraint_config: Any = None):
        super().__init__()
        self.model_name = model_name
        self.constraint_type = constraint_type
        self.constraint_config = constraint_config

        # Load Outlines model
        self.outlines_model = models.transformers(model_name)

        # Create generator
        if constraint_type == "pydantic":
            self.generator = generate.pydantic(self.outlines_model, constraint_config)
        elif constraint_type == "json":
            self.generator = generate.json(self.outlines_model, constraint_config)
        else:
            self.generator = generate.text(self.outlines_model, max_tokens=100)

    @property
    def metadata(self):
        return {
            "model_name": self.model_name,
            "constraint_type": self.constraint_type
        }

    def complete(self, prompt: str, **kwargs) -> str:
        """Complete prompt with constraints."""
        return self.generator(prompt)

    async def acomplete(self, prompt: str, **kwargs) -> str:
        """Async completion."""
        # In practice, implement async generation
        return self.generator(prompt)

# Create structured LLM
structured_llm = OutlinesLLM(
    model_name="microsoft/DialoGPT-small",
    constraint_type="pydantic",
    constraint_config=StructuredAnswer
)

# Create documents
documents = [
    Document(text="Outlines is a Python library for constrained text generation with LLMs."),
    Document(text="It supports JSON Schema, regular expressions, and context-free grammars."),
    Document(text="Outlines can generate structured data with guaranteed compliance."),
    Document(text="The library works with Transformers, llama.cpp, and vLLM backends.")
]

# Create index
index = VectorStoreIndex.from_documents(documents)

# Create query engine with structured output
query_engine = index.as_query_engine(
    llm=structured_llm,
    response_mode="tree_summarize"
)

# Query with structured response
response = query_engine.query("What is Outlines and what does it support?")

print("Structured query response:")
print(f"Question: {response.question}")
print(f"Answer: {response.answer}")
print(f"Confidence: {response.confidence}")
print(f"Sources: {response.sources}")
```

### RAG with Constrained Generation

```python
from llama_index import ServiceContext, set_global_service_context
from llama_index.embeddings import HuggingFaceEmbedding

# Set up embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create service context with constrained LLM
service_context = ServiceContext.from_defaults(
    llm=structured_llm,
    embed_model=embed_model
)

set_global_service_context(service_context)

# Create RAG system
rag_index = VectorStoreIndex.from_documents(documents)

# Custom RAG prompt with constraints
from llama_index.prompts import PromptTemplate

qa_prompt = PromptTemplate(
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query with structured information.\n"
    "Query: {query_str}\n"
    "Answer:"
)

# Create RAG query engine
rag_engine = rag_index.as_query_engine(
    text_qa_template=qa_prompt,
    similarity_top_k=3
)

# Query with RAG
rag_response = rag_engine.query("How does Outlines ensure output compliance?")

print("RAG response:")
print(f"Answer: {rag_response.answer}")
print(f"Confidence: {rag_response.confidence}")
print(f"Related questions: {rag_response.related_questions}")
```

## FastAPI Integration

### Structured API Endpoints

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from outlines import models, generate
import asyncio
import time

app = FastAPI(title="Outlines API", version="1.0.0")

# Load model globally
model = models.transformers("microsoft/DialoGPT-small")

# Request/Response models
class GenerationRequest(BaseModel):
    prompt: str
    constraint_type: str = Field(enum=["text", "choice", "json", "pydantic"])
    constraint_config: Optional[Dict[str, Any]] = None
    max_tokens: int = 100
    temperature: float = 0.7

class GenerationResponse(BaseModel):
    result: Any
    generation_time: float
    model_name: str = "microsoft/DialoGPT-small"
    constraint_type: str

class BatchGenerationRequest(BaseModel):
    requests: List[GenerationRequest]
    max_concurrent: int = 3

class BatchGenerationResponse(BaseModel):
    results: List[GenerationResponse]
    total_time: float
    successful_generations: int

# Generation cache
generation_cache = {}

def get_cached_generator(constraint_type: str, constraint_config: Any):
    """Get cached generator."""
    cache_key = f"{constraint_type}:{str(constraint_config)}"

    if cache_key not in generation_cache:
        if constraint_type == "text":
            generator = generate.text(model, max_tokens=constraint_config.get("max_tokens", 100))
        elif constraint_type == "choice":
            generator = generate.choice(model, constraint_config["choices"])
        elif constraint_type == "json":
            generator = generate.json(model, constraint_config["schema"])
        elif constraint_type == "pydantic":
            # Import the model class dynamically
            generator = generate.pydantic(model, constraint_config["model_class"])
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported constraint type: {constraint_type}")

        generation_cache[cache_key] = generator

    return generation_cache[cache_key]

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    """Generate text with constraints."""
    try:
        start_time = time.time()

        # Get generator
        generator = get_cached_generator(request.constraint_type, request.constraint_config)

        # Generate
        result = generator(request.prompt)

        generation_time = time.time() - start_time

        return GenerationResponse(
            result=result,
            generation_time=generation_time,
            constraint_type=request.constraint_type
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate/batch", response_model=BatchGenerationResponse)
async def generate_batch(request: BatchGenerationRequest):
    """Generate multiple texts with constraints."""
    start_time = time.time()
    results = []
    successful = 0

    # Semaphore for concurrency control
    semaphore = asyncio.Semaphore(request.max_concurrent)

    async def generate_single(req: GenerationRequest):
        async with semaphore:
            try:
                gen_start = time.time()
                generator = get_cached_generator(req.constraint_type, req.constraint_config)
                result = generator(req.prompt)
                gen_time = time.time() - gen_start

                return GenerationResponse(
                    result=result,
                    generation_time=gen_time,
                    constraint_type=req.constraint_type
                ), True
            except Exception as e:
                # Return error response
                return GenerationResponse(
                    result=f"Error: {str(e)}",
                    generation_time=0.0,
                    constraint_type=req.constraint_type
                ), False

    # Generate all concurrently
    tasks = [generate_single(req) for req in request.requests]
    task_results = await asyncio.gather(*tasks)

    # Process results
    for response, success in task_results:
        results.append(response)
        if success:
            successful += 1

    total_time = time.time() - start_time

    return BatchGenerationResponse(
        results=results,
        total_time=total_time,
        successful_generations=successful
    )

@app.get("/models")
async def list_models():
    """List available models and constraints."""
    return {
        "models": ["microsoft/DialoGPT-small"],
        "constraint_types": ["text", "choice", "json", "pydantic"],
        "cache_size": len(generation_cache)
    }

@app.post("/cache/clear")
async def clear_cache():
    """Clear generation cache."""
    generation_cache.clear()
    return {"message": "Cache cleared"}

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": True,
        "cache_entries": len(generation_cache)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Testing the API

```python
import requests
import json

# Test single generation
response = requests.post("http://localhost:8000/generate", json={
    "prompt": "What is the capital of France?",
    "constraint_type": "choice",
    "constraint_config": {"choices": ["Paris", "London", "Berlin", "Madrid"]}
})

print("Single generation result:")
print(json.dumps(response.json(), indent=2))

# Test batch generation
batch_response = requests.post("http://localhost:8000/generate/batch", json={
    "requests": [
        {
            "prompt": "Choose a color",
            "constraint_type": "choice",
            "constraint_config": {"choices": ["red", "blue", "green"]}
        },
        {
            "prompt": "Rate this tutorial",
            "constraint_type": "choice",
            "constraint_config": {"choices": ["excellent", "good", "average", "poor"]}
        }
    ],
    "max_concurrent": 2
})

print("\nBatch generation results:")
for i, result in enumerate(batch_response.json()["results"]):
    print(f"Request {i+1}: {result['result']}")
```

## Custom Integration Patterns

### Plugin System for Outlines

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Type

class OutlinesPlugin(ABC):
    """Base class for Outlines plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration."""
        pass

    @abstractmethod
    def get_generator(self, constraint_config: Any) -> Any:
        """Get configured generator."""
        pass

    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass

class LangChainPlugin(OutlinesPlugin):
    """Plugin for LangChain integration."""

    @property
    def name(self) -> str:
        return "langchain"

    def initialize(self, config: Dict[str, Any]) -> None:
        self.model_name = config.get("model_name", "microsoft/DialoGPT-small")
        self.model = models.transformers(self.model_name)

    def get_generator(self, constraint_config: Any) -> 'OutlinesConstrainedLLM':
        return OutlinesConstrainedLLM(
            model_name=self.model_name,
            constraint_type=constraint_config.get("type", "text"),
            constraint_config=constraint_config.get("config")
        )

class CrewAIPlugin(OutlinesPlugin):
    """Plugin for CrewAI integration."""

    @property
    def name(self) -> str:
        return "crewai"

    def initialize(self, config: Dict[str, Any]) -> None:
        self.model_name = config.get("model_name", "microsoft/DialoGPT-small")

    def get_generator(self, constraint_config: Any) -> Type['OutlinesAgent']:
        return lambda **kwargs: OutlinesAgent(
            model_name=self.model_name,
            constraint_config=constraint_config,
            **kwargs
        )

class PluginManager:
    """Manage Outlines plugins."""

    def __init__(self):
        self.plugins: Dict[str, OutlinesPlugin] = {}

    def register_plugin(self, plugin: OutlinesPlugin) -> None:
        """Register a plugin."""
        self.plugins[plugin.name] = plugin

    def initialize_plugin(self, name: str, config: Dict[str, Any]) -> None:
        """Initialize a plugin."""
        if name not in self.plugins:
            raise ValueError(f"Plugin {name} not registered")

        self.plugins[name].initialize(config)

    def get_plugin_generator(self, plugin_name: str, constraint_config: Any):
        """Get generator from plugin."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} not found")

        return self.plugins[plugin_name].get_generator(constraint_config)

# Usage
plugin_manager = PluginManager()

# Register plugins
plugin_manager.register_plugin(LangChainPlugin())
plugin_manager.register_plugin(CrewAIPlugin())

# Initialize plugins
plugin_manager.initialize_plugin("langchain", {"model_name": "microsoft/DialoGPT-small"})
plugin_manager.initialize_plugin("crewai", {"model_name": "microsoft/DialoGPT-small"})

# Use plugins
langchain_llm = plugin_manager.get_plugin_generator("langchain", {
    "type": "choice",
    "config": ["yes", "no", "maybe"]
})

crewai_agent_class = plugin_manager.get_plugin_generator("crewai", TaskResult)

# Create agent instance
agent = crewai_agent_class(
    role="Assistant",
    goal="Help users with constrained generation",
    backstory="You are an AI assistant specialized in structured outputs."
)
```

This comprehensive integration chapter shows how Outlines can be seamlessly integrated with popular AI frameworks, enabling structured generation in complex applications. The next chapter covers production deployment and scaling. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `constraint_type`, `constraint_config` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Integration with AI Frameworks` as an operating subsystem inside **Outlines Tutorial: Structured Text Generation with LLMs**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `model_name`, `result`, `generator` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Integration with AI Frameworks` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `constraint_type` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `constraint_config`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/outlines-dev/outlines)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `constraint_type` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Advanced Features & Performance Optimization](06-advanced-features.md)
- [Next Chapter: Chapter 8: Production Deployment & Scaling](08-production.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
