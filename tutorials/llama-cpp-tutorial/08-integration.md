---
layout: default
title: "llama.cpp Tutorial - Chapter 8: Integration"
nav_order: 8
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 8: Integration

Welcome to **Chapter 8: Integration**. In this part of **llama.cpp Tutorial: Local LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Integrate llama.cpp with Python applications, web services, and production systems.

## Overview

While llama.cpp is written in C++, it provides excellent Python bindings and can be integrated into various applications. This chapter covers Python integration, web applications, and production deployment patterns.

## Python Bindings (llama-cpp-python)

### Installation

```bash
# Install llama-cpp-python
pip install llama-cpp-python

# For GPU support (choose one)
pip install llama-cpp-python[cu118]  # CUDA 11.8
pip install llama-cpp-python[cu121]  # CUDA 12.1
pip install llama-cpp-python[metal]  # Apple Metal
pip install llama-cpp-python[rocm]   # AMD ROCm
```

### Basic Usage

```python
from llama_cpp import Llama

# Load model
llm = Llama(
    model_path="model.gguf",
    n_ctx=4096,              # Context window
    n_threads=8,             # CPU threads
    n_gpu_layers=35,         # GPU layers (if available)
    verbose=False            # Reduce logging
)

# Generate text
output = llm(
    "Q: What is the capital of France? A:",
    max_tokens=100,
    temperature=0.1,
    stop=["Q:", "\n"]        # Stop sequences
)

print(output["choices"][0]["text"])
```

### Streaming Generation

```python
# Streaming output
output = llm(
    "Write a short story about AI:",
    max_tokens=500,
    temperature=0.8,
    stream=True
)

for chunk in output:
    print(chunk["choices"][0]["text"], end="", flush=True)
```

### Advanced Configuration

```python
llm = Llama(
    model_path="model.gguf",
    n_ctx=4096,
    n_batch=512,             # Batch size
    n_threads=8,
    n_gpu_layers=35,
    rope_scaling_type="yarn", # RoPE scaling
    rope_freq_base=10000,
    rope_freq_scale=2.0,
    mul_mat_q=True,          # Quantized matrix multiplication
    logits_all=False,        # Only generate logits for last token
    embedding=True,          # Enable embeddings
    offload_kqv=True,        # Offload KQV cache to GPU
    last_n_tokens_size=64,   # Repetition penalty window
    seed=42,                 # Random seed
    verbose=False
)
```

## Chat Interface

```python
class ChatBot:
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            chat_format="llama-2"  # Auto-detect chat format
        )
        self.conversation = []

    def chat(self, user_message: str, stream: bool = False):
        """Have a conversation with the model."""

        # Add user message
        self.conversation.append({"role": "user", "content": user_message})

        # Generate response
        response = self.llm.create_chat_completion(
            messages=self.conversation,
            max_tokens=200,
            temperature=0.7,
            stream=stream
        )

        if stream:
            full_response = ""
            for chunk in response:
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    content = delta["content"]
                    print(content, end="", flush=True)
                    full_response += content
            print()  # New line
        else:
            full_response = response["choices"][0]["message"]["content"]
            print(full_response)

        # Add assistant response
        self.conversation.append({"role": "assistant", "content": full_response})

        return full_response

# Usage
bot = ChatBot("llama-2-7b-chat.gguf")
bot.chat("Hello! How are you?")
bot.chat("What's the weather like?", stream=True)
```

## Embeddings and Semantic Search

```python
class EmbeddingSearch:
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            embedding=True,
            verbose=False
        )
        self.documents = []
        self.embeddings = []

    def add_document(self, text: str):
        """Add document to search index."""
        self.documents.append(text)

        # Generate embedding
        embedding = self.llm.embed(text)
        self.embeddings.append(embedding)

    def search(self, query: str, top_k: int = 5):
        """Search for similar documents."""
        import numpy as np

        query_embedding = self.llm.embed(query)

        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            # Cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append((similarity, self.documents[i]))

        # Sort by similarity
        similarities.sort(reverse=True, key=lambda x: x[0])

        return similarities[:top_k]

# Usage
search = EmbeddingSearch("model.gguf")

# Add documents
search.add_document("Python is a programming language")
search.add_document("Machine learning uses algorithms")
search.add_document("Neural networks are computational models")

# Search
results = search.search("artificial intelligence", top_k=2)
for similarity, doc in results:
    print(f"{similarity:.3f}: {doc}")
```

## FastAPI Web Service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from llama_cpp import Llama

app = FastAPI(title="Llama.cpp API")

# Global model (load once)
model = None

def get_model():
    global model
    if model is None:
        model = Llama(
            model_path="model.gguf",
            n_ctx=4096,
            n_threads=8,
            n_gpu_layers=35
        )
    return model

class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7
    max_tokens: int = 200
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    usage: Optional[dict] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        llm = get_model()

        response = llm(
            request.message,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=request.stream
        )

        if request.stream:
            # For streaming, we'd need SSE implementation
            # This is simplified
            full_response = ""
            for chunk in response:
                full_response += chunk["choices"][0]["text"]
        else:
            full_response = response["choices"][0]["text"]

        return ChatResponse(
            response=full_response,
            usage=response.get("usage")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class EmbedRequest(BaseModel):
    texts: List[str]

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]

@app.post("/embed", response_model=EmbedResponse)
async def embed(request: EmbedRequest):
    try:
        llm = get_model()

        embeddings = []
        for text in request.texts:
            embedding = llm.embed(text)
            embeddings.append(embedding)

        return EmbedResponse(embeddings=embeddings)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Gradio Web Interface

```python
import gradio as gr
from llama_cpp import Llama

def create_chat_interface(model_path: str):
    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        chat_format="llama-2"
    )

    def chat(message, history):
        # Format conversation
        messages = []
        for human, assistant in history:
            messages.extend([
                {"role": "user", "content": human},
                {"role": "assistant", "content": assistant}
            ])
        messages.append({"role": "user", "content": message})

        # Generate response
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )

        bot_message = response["choices"][0]["message"]["content"]
        history.append((message, bot_message))

        return "", history

    # Create interface
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="Type your message here...")
        clear = gr.Button("Clear")

        msg.submit(chat, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    return demo

# Launch
interface = create_chat_interface("llama-2-7b-chat.gguf")
interface.launch(server_name="0.0.0.0", server_port=7860)
```

## LangChain Integration

```python
from langchain.llms import LlamaCpp
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Create LlamaCpp LLM
llm = LlamaCpp(
    model_path="model.gguf",
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=35,
    temperature=0.7,
    max_tokens=200,
    verbose=False
)

# Basic chain
template = "Question: {question}\nAnswer: Let's think step by step."
prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run(question="What is the capital of France?")
print(result)

# Conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory(),
    verbose=False
)

print(conversation.predict(input="Hi, I'm Alex!"))
print(conversation.predict(input="What's my name?"))
```

## LlamaIndex Integration

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import LlamaCPP
from llama_index.embeddings import LlamaCPPEmbedding

# Set up LLM
llm = LlamaCPP(
    model_path="model.gguf",
    temperature=0.1,
    max_new_tokens=256,
    context_window=3900,
    model_kwargs={"n_gpu_layers": 35},
    verbose=False
)

# Set up embeddings
embed_model = LlamaCPPEmbedding(
    model_path="model.gguf",
    verbose=False
)

# Create service context
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model
)

# Load documents and create index
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(
    documents,
    service_context=service_context
)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is machine learning?")
print(response)
```

## CrewAI Integration

```python
from crewai import Agent, Task, Crew
from llama_cpp import Llama

class LlamaCPPLLM:
    """Custom LLM wrapper for CrewAI."""

    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            temperature=0.7,
            verbose=False
        )

    def call(self, prompt: str, **kwargs) -> str:
        """CrewAI-compatible call method."""
        response = self.llm(
            prompt,
            max_tokens=kwargs.get("max_tokens", 200),
            temperature=kwargs.get("temperature", 0.7)
        )
        return response["choices"][0]["text"]

# Create agents
llm = LlamaCPPLLM("model.gguf")

researcher = Agent(
    role="Research Analyst",
    goal="Analyze market trends and provide insights",
    backstory="You are an expert market researcher with 10 years experience.",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging articles based on research",
    backstory="You are a skilled writer who creates compelling content.",
    llm=llm,
    verbose=True
)

# Create tasks
research_task = Task(
    description="Research the latest trends in AI technology",
    agent=researcher
)

write_task = Task(
    description="Write a 500-word article about AI trends",
    agent=writer
)

# Create and run crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

## Docker Integration

```dockerfile
# Dockerfile.python
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install llama-cpp-python with CUDA support
RUN pip install llama-cpp-python[cu118] fastapi uvicorn

# Copy application
COPY app.py /app/
WORKDIR /app

# Download model (or mount volume)
# RUN wget -O model.gguf https://example.com/model.gguf

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  llama-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models:ro
    environment:
      - MODEL_PATH=/models/model.gguf
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G
```

## Production Considerations

### Model Loading Optimization

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

class ModelManager:
    def __init__(self):
        self.models = {}
        self.executor = ThreadPoolExecutor(max_workers=4)

    def load_model(self, model_name: str, model_path: str):
        """Load model asynchronously."""
        def _load():
            start_time = time.time()
            llm = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_threads=8,
                n_gpu_layers=35,
                verbose=False
            )
            load_time = time.time() - start_time
            print(f"Loaded {model_name} in {load_time:.2f}s")
            return llm

        future = self.executor.submit(_load)
        self.models[model_name] = future

    def get_model(self, model_name: str):
        """Get loaded model."""
        future = self.models.get(model_name)
        if future and future.done():
            return future.result()
        return None

    async def generate(self, model_name: str, prompt: str, **kwargs):
        """Generate with specified model."""
        model = self.get_model(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not loaded")

        # Run generation in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            lambda: model(prompt, **kwargs)
        )

# Usage
manager = ModelManager()

# Load models
manager.load_model("llama-7b", "llama-7b.gguf")
manager.load_model("mistral-7b", "mistral-7b.gguf")

# Generate
response = await manager.generate(
    "llama-7b",
    "Hello, world!",
    max_tokens=100
)
```

### Caching and Optimization

```python
from cachetools import TTLCache
import hashlib

class CachedLlama:
    def __init__(self, model_path: str, cache_ttl: int = 3600):
        self.llm = Llama(model_path=model_path, verbose=False)
        self.cache = TTLCache(maxsize=1000, ttl=cache_ttl)

    def generate_cached(self, prompt: str, **kwargs):
        """Generate with caching for identical prompts."""
        # Create cache key
        key_data = f"{prompt}_{str(sorted(kwargs.items()))}"
        cache_key = hashlib.md5(key_data.encode()).hexdigest()

        # Check cache
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Generate and cache
        response = self.llm(prompt, **kwargs)
        self.cache[cache_key] = response

        return response

# Usage
llm = CachedLlama("model.gguf")
response1 = llm.generate_cached("What is AI?", temperature=0.1)
response2 = llm.generate_cached("What is AI?", temperature=0.1)  # Cached
```

## Error Handling and Resilience

```python
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class ResilientLlama:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.llm = None

    def _ensure_model_loaded(self):
        """Ensure model is loaded."""
        if self.llm is None:
            try:
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=4096,
                    verbose=False
                )
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    def generate_with_retry(self, prompt: str, **kwargs):
        """Generate with automatic retry on failure."""
        try:
            self._ensure_model_loaded()
            return self.llm(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            # Reset model on failure
            self.llm = None
            raise

# Usage
llm = ResilientLlama("model.gguf")

try:
    response = llm.generate_with_retry(
        "Tell me a joke",
        max_tokens=100,
        temperature=0.8
    )
    print(response["choices"][0]["text"])
except Exception as e:
    print(f"Failed after retries: {e}")
```

## Best Practices

1. **Resource Management**: Pre-load models and manage memory carefully
2. **Async Processing**: Use async for concurrent requests
3. **Caching**: Cache frequent queries to improve performance
4. **Error Handling**: Implement comprehensive error handling and retries
5. **Monitoring**: Track performance metrics and usage patterns
6. **Security**: Validate inputs and limit resource usage
7. **Updates**: Keep llama-cpp-python updated for latest features

These integration patterns enable seamless incorporation of llama.cpp into Python applications, from simple scripts to complex production systems. The combination of C++ performance and Python flexibility makes llama.cpp a powerful choice for local LLM deployment.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `model`, `model_path` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Integration` as an operating subsystem inside **llama.cpp Tutorial: Local LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `gguf`, `llama` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `model` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `model_path`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ggerganov/llama.cpp)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `model` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Advanced Features](07-advanced.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
